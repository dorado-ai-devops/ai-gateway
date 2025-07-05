# 🔁 ai-gateway

> Microservicio Flask que actúa como gateway inteligente entre Jenkins, los microservicios IA (`ai-log-analyzer`, `ai-helm-linter`, `ai-pipeline-gen`) y los modelos LLM locales (Ollama) o remotos (OpenAI). Este componente organiza el flujo de información, dirige las peticiones y establece fallback entre motores de IA.

---

## 🚪 Función Principal

Centraliza las llamadas desde Jenkins y despacha las peticiones a los microservicios AI del entorno `devops-ai-lab`, utilizando como backend modelos de lenguaje (LLMs) para:

- 📊 Análisis de logs
- 🧪 Validación de Helm Charts
- ⚙️ Generación de pipelines desde texto
- 🧠 Registro automático de mensajes MCP para trazabilidad (vía `ai-mcp-server`)

---

## 🌐 Endpoints

### `POST /analyze-log`

Analiza registros CI/CD con LLMs.

**Payload:**
```json
{
  "log": "contenido del log",
  "mode": "ollama"
}
```
→ Redirige internamente a `ai-log-analyzer`.  
→ Si hay `prompt_path` y `response_path`, registra mensaje MCP.

---

### `POST /lint-chart`

Valida un Helm Chart mediante IA.

**Payload (multipart/form-data):**
- `chart`: archivo `.tgz` del Helm Chart
- `mode`: `"ollama"` o `"openai"`
- `strict`: `"true"` o `"false"` (opcional)

→ Redirige a `ai-helm-linter`  
→ MCP registrado automáticamente si se genera respuesta con prompt.

---

### `POST /generate-pipeline`

Convierte lenguaje natural en definición de pipeline CI/CD.

**Payload:**
```json
{
  "description": "Pipeline con test y despliegue usando Helm",
  "mode": "ollama"
}
```
→ Llama a `ai-pipeline-gen`  
→ MCP registrado automáticamente.

---

### `GET /health`

Respuesta: `200 OK`  
Sirve para verificar que el gateway está operativo.

---

## 📦 Estructura del Proyecto

```
ai-gateway/
├── app.py                 # Servidor Flask principal
├── routes/                # Endpoints organizados por dominio
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Módulos de comunicación
│   ├── service_dispatcher.py  # Redirección + registro MCP
│   └── mcp_client.py         # Envío directo al ai-mcp-server
├── config.py              # Configuración centralizada
├── requirements.txt       # Dependencias
├── Makefile               # Automatización de despliegue
├── Dockerfile             # Imagen de contenedor
└── run_*.sh               # Scripts de test locales
```

---

## ⚙️ Ejecutar localmente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🔁 Integración con Jenkins

```groovy
def jsonPayload = '''
{
  "description": "Pipeline básico para test y deploy",
  "mode": "ollama"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🧠 Inteligencia Adaptativa + MCP

- Primero intenta con **Ollama local** (modelo `mistral`)
- Si falla, redirige automáticamente a **OpenAI GPT-4o**
- Si hay `prompt_path` y `response_path`, se registra un mensaje MCP en `ai-mcp-server`
- MCP incluye `uuid`, `timestamp`, `tags`, `summary`, etc.

---

## 🔐 Seguridad y Futuro

- Autenticación por token (pendiente)
- Validación de entradas y sanitización
- Logging estructurado pendiente de mejorar

---

## 🔮 Futuros módulos

- `/explain-error`: análisis de tracebacks
- `/summarize-pipeline`: resumen de definiciones CI/CD
- `/compare-logs`: comparación entre logs

---

## 👨‍💻 Autor

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0