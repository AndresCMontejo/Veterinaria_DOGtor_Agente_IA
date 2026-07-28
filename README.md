# 🐶 Dokky AI – Agente Inteligente para Veterinaria DOGtor

Dokky AI es un asistente virtual basado en Inteligencia Artificial Generativa y Retrieval-Augmented Generation (RAG), desarrollado como proyecto académico para demostrar la construcción completa de un agente conversacional capaz de responder preguntas utilizando documentación interna de una organización.

El proyecto simula el funcionamiento de un asistente virtual para la clínica ficticia **Veterinaria DOGtor**, respondiendo consultas relacionadas con:

- 🩺 Servicios veterinarios
- 📅 Citas y agendamientos
- 🔄 Cancelaciones y reprogramaciones
- 📄 Convenios
- 🔐 Políticas de privacidad
- 🐾 Instrucciones pre y postconsulta

El asistente responde exclusivamente utilizando la información contenida en los documentos indexados, evitando generar respuestas inventadas.

---

# 🚀 Demostración del proyecto

## 🌐 Aplicación desplegada

**Enlace al proyecto:**

> 🔗 **Pegar aquí la URL del proyecto desplegado en OCI**

Ejemplo:

```
http://123.123.123.123:7860
```

---

## 🎥 Video demostrativo

En el siguiente video se muestra el funcionamiento completo del agente, incluyendo consultas reales, recuperación de documentos mediante RAG y generación de respuestas utilizando Gemini.

📺 **Video:**

> 🔗 https://www.youtube.com/watch?v=5_SRpZWngtU

---

# 📚 Arquitectura del proyecto

```
Usuario
     │
     ▼
Interfaz Gradio
     │
     ▼
Pipeline RAG
     │
     ▼
Embedding de la consulta
     │
     ▼
ChromaDB
(Búsqueda semántica)
     │
     ▼
Documentos relevantes
     │
     ▼
Construcción del Prompt
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Respuesta final
```

---

# 🗂️ Estructura del proyecto

```
veterinaria_dogtor_app/

│
├── app.py
├── requirements.txt
│
├── chroma_db/
│
├── documentos/
│   ├── servicios_veterinaria_dogtor.docx
│   ├── politica_privacidad_datos_paciente.docx
│   ├── politica_cancelaciones_reprogramacion.docx
│   ├── instrucciones_pre_postconsulta.docx
│   ├── guia_convenios.docx
│   └── citas_agendamientos.docx
│
└── prompt/
    └── system_prompt.docx
```

---

# ⚙️ Tecnologías utilizadas

- Python
- Google Gemini API
- Gemini Embedding API
- ChromaDB
- LangChain
- Gradio
- python-docx
- Google Colab
- Oracle Cloud Infrastructure (OCI)

---

# 🧠 Flujo de funcionamiento

1. El usuario escribe una pregunta.
2. La consulta se transforma en un embedding mediante Gemini.
3. ChromaDB realiza una búsqueda semántica.
4. Se recuperan los fragmentos más relevantes.
5. Se construye un prompt utilizando:
   - System Prompt
   - Contexto recuperado
   - Pregunta del usuario
6. Gemini genera la respuesta.
7. Se muestran las fuentes utilizadas.

---

# 📖 Base de conocimiento

El agente utiliza documentos DOCX indexados previamente.

Los documentos no son enviados completos al modelo de lenguaje.

El proceso consiste en:

- extracción del texto
- conservación de tablas
- creación de metadatos
- división en chunks
- generación de embeddings
- almacenamiento en ChromaDB

Durante una consulta únicamente se recuperan los fragmentos más relevantes.

---

# 🏗️ Despliegue

El proyecto fue desarrollado inicialmente en Google Colab para la construcción y validación del pipeline RAG.

Posteriormente fue adaptado para ejecutarse como una aplicación independiente utilizando:

- Gradio
- ChromaDB persistente
- Gemini API

Finalmente fue desplegado utilizando servicios de Oracle Cloud Infrastructure (OCI).

---

# ▶️ Instalación

Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

Entrar al proyecto

```bash
cd veterinaria_dogtor_app
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Configurar la variable de entorno

```bash
GEMINI_API_KEY=TU_API_KEY
```

Ejecutar

```bash
python app.py
```

---

# 📌 Características

- Respuestas basadas en documentos.
- Recuperación semántica mediante embeddings.
- Búsqueda vectorial con ChromaDB.
- Conservación de tablas de Word.
- Citas de los documentos utilizados.
- Interfaz web con Gradio.
- Arquitectura RAG.
- Base vectorial persistente.

---

# 👨‍💻 Autor

**Luis Andrés Contreras Montejo**

Ingeniero en Telecomunicaciones y Electrónica

Ingeniero de Audio en Producción Musical

Apasionado por:

- Inteligencia Artificial
- Machine Learning
- Ciencia de Datos
- NLP
- Desarrollo de Software
- Audio Profesional
- Grabación, Mezcla, Mastering, Dolby Atmos
- 
GitHub:

https://github.com/AndresCMontejo

LinkedIn:

https://www.linkedin.com/in/andrescmontejo/

---

# 📄 Licencia

Proyecto desarrollado con fines académicos y demostrativos.
