# 🔁 ai-gateway

> Flask microservice acting as an intelligent gateway between Jenkins, DevOps AI microservices (`ai-logs-analyze`, `ai-helm-linter`, `ai-pipeline-gen`), and local (Ollama) or remote (OpenAI) LLMs. This component organizes the flow of information, dispatches requests, and establishes fallback between AI engines.

---

## 🚪 Main Function

Centralizes Jenkins calls and dispatches them to AI microservices in the `DEVOPS-AI-LAB` environment, using LLM backends for:

- 📊 Log analysis
- 🧪 Helm Chart linting and validation
- ⚙️ CI/CD pipeline generation from natural language

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

→ Internally redirects to `ai-logs-analyze`.

---

### `POST /lint-chart`

Validates a Helm Chart via LLM.

**Payload (multipart/form-data):**

- `chart`: `.tgz` Helm Chart archive
- `mode`: `"ollama"` or `"openai"`
- `ruleset`: `"default"` (optional)

→ Redirects to `ai-helm-linter`.

---

### `POST /generate-pipeline`

Converts natural language into a CI/CD pipeline definition.

**Payload:**
```json
{
  "description": "Create a pipeline that builds, tests, and deploys to Kubernetes using Helm",
  "target": "jenkins"
}
```

→ Sends request to `ai-pipeline-gen`.

---

### `GET /health`

Response: `200 OK`  
Used to check gateway health status.

---

## 🧠 Adaptive Intelligence

- Uses **local Ollama models** by default (e.g., Mistral 7b)
- Automatically falls back to **OpenAI GPT-4o** if Ollama fails
- All routing, dispatch and fallback logic lives within `ai-gateway`

---

## 📦 Project Structure

```
ai-gateway/
├── app.py                 # Flask server with all endpoints
├── routes/                # Endpoint-specific modules
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Connections to services and models
│   ├── ollama_client.py
│   ├── openai_client.py
│   └── service_dispatcher.py
├── config/                # Configs, paths, fallbacks
├── requirements.txt
└── Dockerfile
```

---

## ⚙️ Running the App

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🔗 Jenkins Integration

Jenkins pipelines can call the gateway directly:

```groovy
def jsonPayload = '''
{
  "description": "Generate pipeline for testing + deployment in K8s",
  "target": "jenkins"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🧠 System Role

- Acts as the unified entry point to the AI backend
- Deployable as a Flask microservice in Kubernetes
- Managed by ArgoCD with GitOps manifests
- Requires `ai-logs-analyze`, `ai-helm-linter`, and `ai-pipeline-gen` deployed beforehand

---

## 🔒 Security Roadmap

- Token-based authentication (if public)
- Input validation and sanitization
- Structured logging with adjustable verbosity

---

## 🔮 Possible Future Modules

- `/explain-error`: AI explanation of tracebacks or technical errors
- `/summarize-pipeline`: Pipeline summaries for audits
- `/compare-logs`: Log diffs between two runs

---

## 👨‍💻 Author

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0