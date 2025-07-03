# 🔁 ai-gateway

> Flask microservice acting as an intelligent gateway between Jenkins, AI microservices (`ai-logs-analyze`, `ai-helm-linter`, `ai-pipeline-gen`), and local (Ollama) or remote (OpenAI) LLMs. This component organizes the information flow, routes requests, and manages fallback between AI engines.

---

## 🚪 Main Function

Centralizes Jenkins requests and dispatches them to the AI microservices inside `DEVOPS-AI-LAB`, using language models (LLMs) for:

- 📊 Log analysis
- 🧪 Helm Charts validation and linting
- ⚙️ Automatic CI/CD pipeline generation from natural language

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

→ Internally redirects to `ai-logs-analyze` microservice.

---

### `POST /lint-chart`

Validates a Helm Chart via AI.

**Payload:**
```json
{
  "chart_path": "./charts/myservice",
  "ruleset": "default"
}
```

→ Redirects to `ai-helm-linter`.

---

### `POST /generate-pipeline`

Converts natural language into a CI/CD pipeline definition.

**Payload:**
```json
{
  "description": "Create a pipeline to build, test, and deploy to Kubernetes with Helm",
  "target": "jenkins"
}
```

→ Calls `ai-pipeline-gen`.

---

### `GET /health`

Response: `200 OK`  
Used to verify that the gateway is running.

---

## 🧠 Adaptive Intelligence

- Defaults to **local models via Ollama** (e.g., Mistral 7b)
- If Ollama fails, automatically falls back to **OpenAI GPT-4o** (if configured)
- All routing, fallback logic, and auth is managed by `ai-gateway`

---

## 📦 Project Structure

```
ai-gateway/
├── app.py                 # Flask server with all endpoints
├── routes/                # Endpoint-specific logic modules
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Microservices and model clients
│   ├── ollama_client.py
│   ├── openai_client.py
│   └── service_dispatcher.py
├── config/                # Parameters, paths, fallback logic
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

You can call the gateway directly from Jenkins to dispatch tasks:

```groovy
def jsonPayload = '''
{
  "description": "I want a pipeline for test + deploy on K8s",
  "target": "jenkins"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🧠 System Role

- Serves as the unique entry point to the AI backend
- Deployed as a Flask microservice in Kubernetes
- Fully managed by ArgoCD using GitOps manifests
- Requires `ai-logs-analyze`, `ai-helm-linter`, and `ai-pipeline-gen` services deployed

---

## 🔒 Future Security

- Token-based auth for public exposure
- Input validation and sanitization
- Structured logging with adjustable verbosity

---

## 🔮 Future Modules

- `/explain-error`: analyze tracebacks or errors and return explanations
- `/summarize-pipeline`: summarize CI/CD for auditing
- `/compare-logs`: diff logs between two executions

---

## 👨‍💻 Author

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0