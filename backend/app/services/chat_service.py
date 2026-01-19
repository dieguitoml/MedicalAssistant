"""
Servicio de chat con LLM y RAG
Integra LangChain, Ollama y ChromaDB
"""
import json
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..config import CHAT_MODEL, EMBEDDING_MODEL, DATABASE_LOCATION


class ChatService:
    """
    Servicio para el chat médico con RAG
    """

    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.agent_executor = None
        self.messages_history = []

        self._initialize()

    def _clean_llm_output(self, text: str) -> str:
        """
        Si el modelo devuelve JSON, lo convertimos a texto natural.
        """
        if not text:
            return text

        t = text.strip()
        if not (t.startswith("{") or t.startswith("[")):
            return text

        try:
            parsed = json.loads(t)

            if isinstance(parsed, dict):
                # casos típicos
                for key in ["answer", "respuesta", "output", "text", "content", "message"]:
                    if key in parsed and isinstance(parsed[key], str):
                        return parsed[key].strip()

                # caso: {"texto largo": "Fuente: ..."}
                if len(parsed) == 1:
                    k, v = next(iter(parsed.items()))
                    if isinstance(k, str) and len(k) > 20:
                        if isinstance(v, str) and v.strip():
                            return f"{k.strip()}\n\n{v.strip()}"
                        return k.strip()

                # fallback genérico
                return "\n".join([f"{k}: {v}" for k, v in parsed.items()]).strip()

            if isinstance(parsed, list):
                return "\n".join([str(x) for x in parsed]).strip()

            return str(parsed).strip()

        except Exception:
            return text

    def _initialize(self):
        """Inicializar componentes de LangChain"""
        try:
            print("[CHAT] Inicializando embeddings...")
            self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

            print(f"[CHAT] Cargando vectorstore desde: {DATABASE_LOCATION}")
            self.vectorstore = Chroma(
                collection_name="respiratory_docs",
                embedding_function=self.embeddings,
                persist_directory=DATABASE_LOCATION,
            )

            print(f"[CHAT] Inicializando LLM: {CHAT_MODEL}")
            self.llm = ChatOllama(model=CHAT_MODEL)

            # ✅ Tool retrieval con filtrado por L2 < 1
            @tool
            def retrieve(query: str) -> str:
                """Recupera información médica relevante desde la base vectorial."""
                SIMILARITY_THRESHOLD = 1.0  # L2 menor = más similar
                SEARCH_K = 25              # buscar varios
                MAX_RETURN = 10            # para no saturar al LLM
                MAX_CHARS_PER_DOC = 1200   # recorte por documento (evita context overflow)

                results = self.vectorstore.similarity_search_with_score(query, k=SEARCH_K)

                # Filtrar por score (L2)
                filtered = [(doc, score) for doc, score in results if score <= SIMILARITY_THRESHOLD]

                if not filtered:
                    return "No se encontró información relevante en la base de datos médica."

                # (opcional) ordenar por score ascendente (más similar primero)
                filtered.sort(key=lambda x: x[1])

                # limitar cantidad por seguridad
                filtered = filtered[:MAX_RETURN]

                output = f"\n=== Resultados de búsqueda ({len(filtered)} documentos relevantes) ===\n"
                for doc, score in filtered:
                    source = doc.metadata.get("source", "desconocida")
                    content = (doc.page_content or "")[:MAX_CHARS_PER_DOC]
                    output += f"\nFuente: {source} (L2: {score:.2f})\n{content}\n"
                output += "\n=== Fin de resultados ===\n"
                return output

            # Configurar prompt
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=(
                    "Eres un asistente médico experto en enfermedades respiratorias.\n"
                    "Tu objetivo es ayudar a los usuarios a entender síntomas, causas y tratamientos.\n\n"
                    "INSTRUCCIONES:\n"
                    "- Usa la herramienta 'retrieve' para buscar información médica.\n"
                    "- No inventes respuestas.\n"
                    "- Cita las fuentes al final con el formato: Fuente: nombre_archivo.txt\n"
                    "- Responde SIEMPRE en español claro y profesional.\n"
                    "- Si el usuario dice algo general como 'Hola', responde brevemente y luego indícale "
                    "que puede hacer preguntas relacionadas con enfermedades respiratorias.\n"
                )),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            # Crear agente
            tools = [retrieve]
            llm_with_tools = self.llm.bind_tools(tools)
            agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
            self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

            print("[CHAT] ✓ Chat service inicializado correctamente")

        except Exception as e:
            print(f"[CHAT] ✗ Error inicializando: {e}")
            import traceback
            traceback.print_exc()

    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self.agent_executor is not None

    def process_message(self, message: str) -> str:
        """Procesar un mensaje del usuario"""
        if not self.is_available():
            return "Error: El servicio de chat no está disponible."

        try:
            self.messages_history.append(HumanMessage(content=message))

            response = self.agent_executor.invoke({
                "input": message,
                "chat_history": self.messages_history
            })

            ai_reply = response["output"]

            # ✅ limpiar JSON si aparece
            ai_reply = self._clean_llm_output(ai_reply)

            self.messages_history.append(AIMessage(content=ai_reply))
            return ai_reply

        except Exception as e:
            print(f"[CHAT] ✗ Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()
            return f"Error al procesar tu consulta: {str(e)}"

    def clear_history(self):
        self.messages_history = []
        print("[CHAT] Historial limpiado")
