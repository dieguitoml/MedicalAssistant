import os
import shutil
from uuid import uuid4
import chardet
from dotenv import load_dotenv
# Importa esto al principio
from langchain_text_splitters import MarkdownTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# === CONFIG ===
load_dotenv()

DATASET_FOLDER = "./dataset_respiratorio_es"
CHROMA_DIR = "./chunks"
EMBEDDING_MODEL = "all-minilm:22m"  # También puedes usar os.getenv("EMBEDDING_MODEL")

# === ELIMINAR DB ANTERIOR ===
if os.path.exists(CHROMA_DIR):
    shutil.rmtree(CHROMA_DIR)
    print(f"🗑️ Eliminado ChromaDB previo: {CHROMA_DIR}")

# === INICIALIZAR EMBEDDINGS ===
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

# === INICIALIZAR VECTORSTORE CHROMA ===
vectorstore = Chroma(
    collection_name="respiratory_docs",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)

# === CONFIGURAR TEXT SPLITTER ===
# Usamos MarkdownTextSplitter para que respete los encabezados y listas
# Reducimos chunk_size para evitar exceder el límite de contexto del modelo de embeddings
splitter = MarkdownTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

# === INGESTA DE ARCHIVOS TXT ===
total_chunks = 0

for filename in os.listdir(DATASET_FOLDER):
    if filename.endswith(".txt"):
        path = os.path.join(DATASET_FOLDER, filename)

        try:
            with open(path, "rb") as f:
                raw = f.read()
                encoding = chardet.detect(raw)["encoding"]
                text = raw.decode(encoding)

            chunks = splitter.create_documents(
                [text],
                metadatas=[{
                    "source": filename.replace(".txt", ""),
                    "title": filename.replace(".txt", "").replace("_", " ").title()
                }]
            )

            # Intentar añadir todos los chunks a la vez
            try:
                uuids = [str(uuid4()) for _ in chunks]
                vectorstore.add_documents(documents=chunks, ids=uuids)
                print(f"✅ {filename}: {len(chunks)} chunks añadidos.")
                total_chunks += len(chunks)
            except Exception as batch_error:
                # Si falla el batch, intentar añadir chunk por chunk
                print(f"⚠️ Error batch en {filename}, procesando chunk por chunk...")
                chunks_added = 0
                for i, chunk in enumerate(chunks):
                    try:
                        vectorstore.add_documents(documents=[chunk], ids=[str(uuid4())])
                        chunks_added += 1
                    except Exception as chunk_error:
                        print(f"   ❌ Chunk {i+1}/{len(chunks)} demasiado largo, omitido.")

                if chunks_added > 0:
                    print(f"✅ {filename}: {chunks_added}/{len(chunks)} chunks añadidos.")
                    total_chunks += chunks_added
                else:
                    print(f"❌ {filename}: No se pudo añadir ningún chunk.")

        except Exception as e:
            print(f"❌ Error en {filename}: {e}")

print(f"✅ Ingesta completa: {total_chunks} chunks añadidos.")
