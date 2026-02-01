"""
Servicio de chat con LLM y RAG
Integra LangChain, Ollama y ChromaDB
"""
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..config import CHAT_MODEL, EMBEDDING_MODEL, DATABASE_LOCATION

# Configuración de retrieval
SIMILARITY_THRESHOLD = 1.0  # L2 menor = más similar
SEARCH_K = 25
MAX_RETURN = 10
MAX_CHARS_PER_DOC = 1200

SYSTEM_PROMPT = """Eres un asistente médico especializado ÚNICAMENTE en enfermedades respiratorias.

INSTRUCCIONES:
- SOLO puedes responder preguntas relacionadas con enfermedades respiratorias (asma, EPOC, neumonía, bronquitis, COVID-19, tuberculosis, etc.).
- Si la pregunta NO es sobre enfermedades respiratorias, responde educadamente que solo puedes ayudar con temas respiratorios.
- Usa el contexto proporcionado para responder. No inventes información.
- Cita las fuentes al final con el formato: Fuente: nombre_archivo.txt
- Responde en español claro y profesional.
- Para saludos generales ('Hola', '¿Cómo estás?'), responde brevemente y menciona que puedes ayudar con preguntas sobre enfermedades respiratorias."""

NO_CONTEXT_RESPONSE = """Lo siento, solo puedo ayudarte con preguntas relacionadas con enfermedades respiratorias como:
- Asma
- EPOC (Enfermedad Pulmonar Obstructiva Crónica)
- Neumonía
- Bronquitis
- COVID-19
- Tuberculosis
- Otras afecciones del sistema respiratorio

¿Tienes alguna pregunta sobre estos temas?"""


class ChatService:
    """
    Servicio para el chat médico con RAG
    """

    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.messages_history = []

        self._initialize()

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

            print("[CHAT] ✓ Chat service inicializado correctamente")

        except Exception as e:
            print(f"[CHAT] ✗ Error inicializando: {e}")
            import traceback
            traceback.print_exc()

    def _retrieve(self, query: str) -> tuple[str, bool]:
        """
        Recupera información médica relevante desde la base vectorial.
        Retorna (contexto, es_relevante) donde es_relevante indica si se encontró información.
        """
        results = self.vectorstore.similarity_search_with_score(query, k=SEARCH_K)

        # Filtrar por score (L2)
        filtered = [(doc, score) for doc, score in results if score <= SIMILARITY_THRESHOLD]

        if not filtered:
            return "", False

        # Ordenar por score ascendente (más similar primero)
        filtered.sort(key=lambda x: x[1])

        # Limitar cantidad
        filtered = filtered[:MAX_RETURN]

        output = f"=== Contexto médico ({len(filtered)} documentos) ===\n"
        for doc, score in filtered:
            source = doc.metadata.get("source", "desconocida")
            content = (doc.page_content or "")[:MAX_CHARS_PER_DOC]
            output += f"\n[Fuente: {source}]\n{content}\n"
        output += "\n=== Fin del contexto ===\n"
        return output, True

    def is_available(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self.llm is not None and self.vectorstore is not None

    def process_message(self, message: str) -> str:
        """Procesar un mensaje del usuario"""
        if not self.is_available():
            return "Error: El servicio de chat no está disponible."

        try:
            # 1. Recuperar contexto relevante
            context, is_relevant = self._retrieve(message)

            # 2. Si no hay contexto relevante, verificar si es saludo o rechazar
            if not is_relevant:
                # Permitir saludos básicos
                greetings = ['hola', 'buenos días', 'buenas tardes', 'buenas noches', 'hey', 'hi', 'hello']
                if any(g in message.lower() for g in greetings):
                    ai_reply = "¡Hola! Soy un asistente especializado en enfermedades respiratorias. ¿En qué puedo ayudarte? Puedo responder preguntas sobre asma, EPOC, neumonía, bronquitis, COVID-19, tuberculosis y otras afecciones del sistema respiratorio."
                else:
                    ai_reply = NO_CONTEXT_RESPONSE

                self.messages_history.append(HumanMessage(content=message))
                self.messages_history.append(AIMessage(content=ai_reply))
                return ai_reply

            # 3. Construir mensajes para el LLM con contexto
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                *self.messages_history,
                HumanMessage(content=f"CONTEXTO:\n{context}\n\nPREGUNTA DEL USUARIO:\n{message}")
            ]

            # 4. Generar respuesta
            response = self.llm.invoke(messages)
            ai_reply = response.content

            # 4. Guardar en historial (sin el contexto, solo la pregunta original)
            self.messages_history.append(HumanMessage(content=message))
            self.messages_history.append(AIMessage(content=ai_reply))

            return ai_reply

        except Exception as e:
            print(f"[CHAT] ✗ Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()
            return f"Error al procesar tu consulta: {str(e)}"

    def clear_history(self):
        """Limpiar historial de conversación"""
        self.messages_history = []
        print("[CHAT] Historial limpiado")
