import os
from pathlib import Path

import chromadb
import gradio as gr
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from google import genai

BASE_DIR = Path(__file__).resolve().parent
PROMPT_DIR = BASE_DIR / "prompt"
CHROMA_DIR = BASE_DIR / "chroma_db"

NOMBRE_COLECCION = "veterinaria_dogtor"
MODELO_EMBEDDING = "gemini-embedding-001"
MODELO_GENERACION = "gemini-2.5-flash"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "No se encontró la variable de entorno GEMINI_API_KEY."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


def extraer_texto_docx(ruta_archivo: Path) -> str:
    documento = Document(ruta_archivo)
    partes = []

    for elemento in documento.iter_inner_content():
        if isinstance(elemento, Paragraph):
            texto = elemento.text.strip()
            if texto:
                partes.append(texto)

        elif isinstance(elemento, Table):
            partes.append("[INICIO DE TABLA]")

            for fila in elemento.rows:
                celdas = []

                for celda in fila.cells:
                    texto_celda = " ".join(
                        parrafo.text.strip()
                        for parrafo in celda.paragraphs
                        if parrafo.text.strip()
                    )
                    celdas.append(texto_celda)

                if any(celdas):
                    partes.append(" | ".join(celdas))

            partes.append("[FIN DE TABLA]")

    return "\n".join(partes)


archivos_prompt = list(PROMPT_DIR.glob("*.docx"))

if len(archivos_prompt) != 1:
    raise ValueError(
        "Debe existir exactamente un archivo DOCX en la carpeta prompt."
    )

SYSTEM_PROMPT = extraer_texto_docx(archivos_prompt[0])

if not CHROMA_DIR.exists():
    raise FileNotFoundError(
        f"No se encontró la base Chroma en: {CHROMA_DIR}"
    )

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name=NOMBRE_COLECCION)


def generar_embedding_consulta(pregunta: str) -> list[float]:
    respuesta = client.models.embed_content(
        model=MODELO_EMBEDDING,
        contents=pregunta
    )
    return respuesta.embeddings[0].values


def buscar_contexto(pregunta: str, top_k: int = 4):
    embedding = generar_embedding_consulta(pregunta)

    return collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )


def construir_contexto(resultados) -> str:
    documentos = resultados["documents"][0]
    metadatos = resultados["metadatas"][0]
    contexto = []

    for i in range(len(documentos)):
        bloque = f"""
DOCUMENTO {i + 1}

Archivo:
{metadatos[i]["nombre_archivo"]}

Categoría:
{metadatos[i]["Categoria"]}

Contenido:
{documentos[i]}
"""
        contexto.append(bloque.strip())

    return "\n\n".join(contexto)


def construir_prompt(pregunta: str, contexto: str) -> str:
    return f"""
{SYSTEM_PROMPT}

================================================
INFORMACIÓN RECUPERADA
================================================

{contexto}

================================================
PREGUNTA DEL USUARIO
================================================

{pregunta}

Responde únicamente utilizando la información proporcionada.
Si la respuesta no aparece en los documentos, indícalo claramente.
""".strip()


def responder_con_fuentes(pregunta: str, top_k: int = 4) -> str:
    if not pregunta or not pregunta.strip():
        return "Por favor, escribe una pregunta."

    resultados = buscar_contexto(
        pregunta=pregunta.strip(),
        top_k=top_k
    )

    contexto = construir_contexto(resultados)
    prompt = construir_prompt(
        pregunta=pregunta.strip(),
        contexto=contexto
    )

    respuesta = client.models.generate_content(
        model=MODELO_GENERACION,
        contents=prompt
    )

    texto_respuesta = (
        respuesta.text
        if respuesta.text
        else "No fue posible generar una respuesta."
    )

    fuentes = []

    for metadata in resultados["metadatas"][0]:
        nombre_archivo = metadata.get(
            "nombre_archivo",
            "Documento sin nombre"
        )

        if nombre_archivo not in fuentes:
            fuentes.append(nombre_archivo)

    fuentes_formateadas = "\n".join(
        f"- `{fuente}`"
        for fuente in fuentes
    )

    return f"""
{texto_respuesta}

---

### Fuentes consultadas

{fuentes_formateadas}
""".strip()


def chat_dokky(mensaje: str, historial: list) -> str:
    try:
        return responder_con_fuentes(
            pregunta=mensaje,
            top_k=4
        )

    except Exception as error:
        print("Error interno:", repr(error))

        return (
            "Lo siento, ocurrió un error al procesar tu pregunta. "
            "Revisa el registro del servidor para más detalles."
        )


demo = gr.ChatInterface(
    fn=chat_dokky,
    title="🐶 Dokky AI",
    description=(
        "Hola, soy un asistente virtual de Veterinaria DOGtor. "
        "Consulta información sobre servicios, citas, convenios, "
        "cancelaciones e instrucciones pre y postconsulta."
    ),
    examples=[
        "¿Qué servicios ofrece la veterinaria?",
        "¿Cómo puedo reprogramar una cita?",
        "¿Qué debo hacer antes de una cirugía?",
        "¿Aceptan convenios o aseguradoras?",
        "¿Qué ocurre si cancelo una cita con poca anticipación?"
    ],
    textbox=gr.Textbox(
        placeholder=(
            "Escribe aquí tu pregunta sobre Veterinaria DOGtor..."
        ),
        container=False,
        scale=7
    ),
    chatbot=gr.Chatbot(
        height=500,
        placeholder=(
            "<h2>🐾 Hola, soy Dokky</h2>"
            "<p>Pregunta sobre los servicios y políticas "
            "de Veterinaria DOGtor.</p>"
            "<p>Creado por Andrés Contreras</p>"
        )
    )
)


if __name__ == "__main__":
    print("Iniciando Dokky AI...")
    print("Colección:", collection.name)
    print("Registros en Chroma:", collection.count())

#    demo.launch(
#        server_name="0.0.0.0",
#        server_port=7860,
#        share=True,
#        show_error=True
#)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
       show_error=True
    )
