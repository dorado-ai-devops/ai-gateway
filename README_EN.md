# 🔁 ai-gateway

> Flask microservice acting as an intelligent gateway between Jenkins, AI microservices (`ai-logs-analyze`, `ai-helm-linter`, `ai-pipeline-gen`), and LLM engines, either local (Ollama) or remote (OpenAI). It orchestrates the flow of information, dispatches requests, and establishes fallbacks between AI engines.

---

## 🚪 Main Function

Centralizes Jenkins requests and delegates them to the corresponding AI microservices within the `DEVOPS-AI-LAB` environment, leveraging LLMs to:

- 📊 Analyze logs
- 🧪 Validate and lint Helm Charts
- ⚙️ Generate CI/CD pipelines from natural language

---

## 🌐 Endpoints

### `POST /analyze-log`

Analyzes CI/CD logs using LLMs.

**Payload:**
```json
{
  "logfile": "logs/build.log",
  "model": "mistral",
  "prompt_template": "log_analysis"
}
```

→ Internally forwards to the `ai-logs-analyze` microservice.

---

### `POST /lint-chart`

Validates a Helm Chart using AI.

**Payload (multipart/form-data):**
- `chart`: Helm `.tgz` file
- `mode`: `"ollama"` or `"openai"`
- `ruleset`: `"default"` (optional)

→ Redirects to `ai-helm-linter`.

---

### `POST /generate-pipeline`

Converts natural language into a CI/CD pipeline definition.

**Payload:**
```json
{
  "description": "Create a pipeline that builds, tests and deploys to Kubernetes using Helm",
  "target": "jenkins"
}
```

→ Calls `ai-pipeline-gen`.

---

### `GET /health`

Response: `200 OK`  
Checks if the gateway is running.

---

## 🧠 Adaptive Intelligence

- Defaults to **local Ollama models** (e.g., Mistral 7b)
- Automatically falls back to **OpenAI GPT-4o** (if configured)
- All routing, fallback and coordination logic is managed in `ai-gateway`

---

## 📦 Project Structure

```
ai-gateway/
├── app.py                 # Flask server with all endpoints
├── routes/                # Endpoint-specific modules
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Interfaces to microservices and models
│   ├── ollama_client.py
│   ├── openai_client.py
│   └── service_dispatcher.py
├── config/                # Parameters, paths, fallbacks
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🧩 Jenkins Integration

From Jenkins you can directly trigger AI-powered tasks via the gateway:

```groovy
def jsonPayload = '''
{
  "description": "Build + deploy to K8s pipeline",
  "target": "jenkins"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🧠 System Role

- Single entry point to the AI backend
- Will be deployed as a Flask microservice in Kubernetes
- Managed via GitOps using ArgoCD
- Requires pre-deployment of `ai-logs-analyze`, `ai-helm-linter` and `ai-pipeline-gen`

---

## 🔒 Future Security

- Token-based authentication (optional)
- Input validation and sanitization
- Structured logging with adjustable verbosity

---

## 🔮 Potential Future Modules

- `/explain-error`: explain tracebacks or error messages
- `/summarize-pipeline`: CI/CD summary for auditing
- `/compare-logs`: log diffing across executions

---

## 👨‍💻 Author

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0