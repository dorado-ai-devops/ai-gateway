# 🔁 ai-gateway

> Microservicio Flask que actúa como gateway inteligente entre Jenkins, los microservicios IA (`ai-logs-analyze`, `ai-helm-linter`, `ai-pipeline-gen`) y los modelos LLM locales (Ollama) o remotos (OpenAI). Este componente organiza el flujo de información, dirige las peticiones y establece fallback entre motores de IA.

---

## 🚪 Función Principal

Centraliza las llamadas desde Jenkins y despacha las peticiones a los microservicios AI del entorno `DEVOPS-AI-LAB`, utilizando como backend modelos de lenguaje (LLMs) para:

- 📊 Análisis de logs
- 🧪 Validación y linting de Helm Charts
- ⚙️ Generación automática de pipelines CI/CD desde lenguaje natural

---

## 🌐 Endpoints

### `POST /analyze-log`

Analiza registros CI/CD con LLMs.

**Payload:**
```json
{
  "logfile": "logs/build.log",
  "model": "mistral",
  "prompt_template": "log_analysis"
}
```

→ Redirige internamente al microservicio `ai-logs-analyze`.

---

### `POST /lint-chart`

Valida un Helm Chart mediante IA.

**Payload (multipart/form-data):**

- `chart`: archivo `.tgz` del Helm Chart
- `mode`: `"ollama"` o `"openai"`
- `ruleset`: `"default"` (opcional)

→ Redirige a `ai-helm-linter`.

---

### `POST /generate-pipeline`

Convierte lenguaje natural en definición de pipeline CI/CD.

**Payload:**
```json
{
  "description": "Crea un pipeline que construya, testee y despliegue en Kubernetes con Helm",
  "target": "jenkins"
}
```

→ Llama a `ai-pipeline-gen`.

---

### `GET /health`

Respuesta: `200 OK`  
Sirve para verificar que el gateway está operativo.

---

## 🧠 Inteligencia Adaptativa

- Utiliza por defecto **modelos locales en Ollama** (por ejemplo, Mistral 7b)
- Si falla Ollama, hace fallback automático a **OpenAI GPT-4o** (si está configurado)
- Toda la lógica de redirección, autenticación y enrutamiento ocurre en `ai-gateway`

---

## 📦 Estructura del Proyecto

```
ai-gateway/
├── app.py                 # Servidor Flask con todos los endpoints
├── routes/                # Módulos específicos de cada endpoint
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Conexiones con microservicios y modelos
│   ├── ollama_client.py
│   ├── openai_client.py
│   └── service_dispatcher.py
├── config/                # Parámetros, paths, fallbacks
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ Ejecutar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🧩 Integración con Jenkins

Desde Jenkins puedes llamar directamente al gateway para despachar tareas:

```groovy
def jsonPayload = '''
{
  "description": "Quiero un pipeline para test + deploy en K8s",
  "target": "jenkins"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🧠 Rol en el sistema

- Es la entrada única al backend de IA
- Se desplegará como microservicio Flask en Kubernetes
- Todo lo expuesto será gestionado por ArgoCD vía manifiestos GitOps
- Requiere los microservicios `ai-logs-analyze`, `ai-helm-linter` y `ai-pipeline-gen` desplegados previamente

---

## 🔒 Seguridad futura

- Autenticación por token si se publica
- Validación de entradas y sanitización
- Logging estructurado con nivel de detalle ajustable

---

## 🔮 Futuros módulos posibles

- `/explain-error`: analizar traceback o errores y devolver explicación
- `/summarize-pipeline`: resumen de CI/CD para auditoría
- `/compare-logs`: diff de logs entre dos ejecuciones

---

## 👨‍💻 Autor

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0