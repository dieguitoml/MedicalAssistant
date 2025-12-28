"""
Servicio de chat con LLM y RAG
Integra LangChain, Ollama y ChromaDB
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional

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
            
            # Crear tool de retrieval
            @tool
            def retrieve(query: str) -> str:
                """Recupera información médica relevante desde la base vectorial."""
                docs = self.vectorstore.similarity_search(query, k=3)
                if not docs:
                    return "No se encontró información relevante en la base de datos médica."
                
                output = "\n=== Resultados de búsqueda ===\n"
                for doc in docs:
                    source = doc.metadata.get("source", "desconocida")
                    output += f"\nFuente: {source}\n{doc.page_content}\n"
                output += "\n=== Fin de resultados ===\n"
                return output
            
            # Configurar prompt
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=(
                    "Eres un asistente médico experto en enfermedades respiratorias.\n"
                    "Tu objetivo es ayudar a los usuarios a entender síntomas, causas y tratamientos.\n"
                    "- Usa la herramienta 'retrieve' para información médica.\n"
                    "- No inventes respuestas.\n"
                    "- Cita las fuentes: Fuente: nombre_archivo.txt\n"
                    "- Responde en español claro y profesional.\n"
                    "- Si el usuario pregunta algo general como 'Hola', responde brevemente y luego "
                    "indícale que puede hacer preguntas médicas relacionadas con enfermedades respiratorias."
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
        """
        Procesar un mensaje del usuario
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Respuesta del asistente
        """
        if not self.is_available():
            return "Error: El servicio de chat no está disponible."
        
        try:
            # Añadir mensaje del usuario al historial
            self.messages_history.append(HumanMessage(content=message))
            
            # Invocar agente
            response = self.agent_executor.invoke({
                "input": message,
                "chat_history": self.messages_history
            })
            
            ai_reply = response["output"]
            
            # Añadir respuesta al historial
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