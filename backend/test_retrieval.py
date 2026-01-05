"""
Script de prueba para verificar que ChromaDB retrieval funciona correctamente
"""
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# === CONFIGURACIÓN ===
CHROMA_DIR = "./chunks"
EMBEDDING_MODEL = "nomic-embed-text"

# === INICIALIZAR ===
print("🔄 Inicializando ChromaDB...")
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="respiratory_docs",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)

# === CONSULTAS DE PRUEBA ===
test_queries = [
    "¿Cuáles son los síntomas del asma?",
    "¿Cómo se trata la neumonía?",
    "¿Qué es la EPOC y cuáles son sus causas?",
    "Síntomas de COVID-19",
    "¿Cuándo debo vacunarme contra la gripe?"
]

print("\n" + "="*80)
print("🧪 PRUEBAS DE RETRIEVAL")
print("="*80 + "\n")

for i, query in enumerate(test_queries, 1):
    print(f"\n📝 Consulta {i}: {query}")
    print("-" * 80)

    # Buscar los 3 documentos más relevantes
    results = vectorstore.similarity_search(query, k=3)

    for j, doc in enumerate(results, 1):
        print(f"\n   Resultado {j}:")
        print(f"   📄 Fuente: {doc.metadata.get('source', 'Unknown')}")
        print(f"   📋 Título: {doc.metadata.get('title', 'Unknown')}")
        print(f"   📖 Contenido (primeros 200 chars):")
        print(f"   {doc.page_content[:200]}...")

    print("\n" + "-" * 80)

print("\n" + "="*80)
print("✅ Pruebas completadas!")
print("="*80)

# === ESTADÍSTICAS ===
print("\n📊 ESTADÍSTICAS DE LA BASE DE DATOS:")
collection = vectorstore._collection
print(f"   Total de chunks: {collection.count()}")
print(f"   Modelo de embeddings: {EMBEDDING_MODEL}")
print(f"   Directorio: {CHROMA_DIR}")
