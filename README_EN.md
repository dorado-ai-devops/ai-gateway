# 🔁 ai-gateway

> Flask microservice that acts as an intelligent gateway between Jenkins, AI microservices (`ai-log-analyzer`, `ai-helm-linter`, `ai-pipeline-gen`), and local (Ollama) or remote (OpenAI) LLMs. This component orchestrates request routing, fallback handling, and MCP message generation.

---

## 🚪 Main Purpose

Centralizes Jenkins calls and dispatches requests to AI services within the `devops-ai-lab` environment, leveraging LLMs for:

- 📊 Log analysis
- 🧪 Helm Chart validation
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
→ Internally forwarded to `ai-log-analyzer`.

---

### `POST /lint-chart`

Audits a Helm Chart using AI.

**Payload (multipart/form-data):**
- `chart`: `.tgz` archive of the Helm Chart
- `mode`: `"ollama"` or `"openai"`
- `ruleset`: `"default"` (optional)

→ Forwards to `ai-helm-linter`.

---

### `POST /generate-pipeline`

Generates a CI/CD pipeline definition from natural language.

**Payload:**
```json
{
  "description": "Pipeline with test and Helm deploy",
  "target": "jenkins"
}
```
→ Forwards to `ai-pipeline-gen`.

---

### `GET /health`

Response: `200 OK`  
Used to verify the gateway is live.

---

## 📦 Project Structure

```
ai-gateway/
├── app.py                 # Main Flask server
├── routes/                # Endpoint definitions
│   ├── analyze_log.py
│   ├── lint_chart.py
│   └── generate_pipeline.py
├── clients/               # Microservice dispatchers
│   ├── service_dispatcher.py
│   └── mcp_client.py
├── config.py              # Service URLs, timeout, default LLM
├── requirements.txt       # Python dependencies
├── Makefile               # Build and deployment automation
├── Dockerfile             # Container image
└── run_*.sh               # Local test scripts
```

---

## ⚙️ Local Execution

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

---

## 🔁 Jenkins Integration Example

```groovy
def jsonPayload = '''
{
  "description": "Basic test and deploy pipeline",
  "target": "jenkins"
}
'''

sh '''
curl -X POST http://ai-gateway.devops-ai.svc.cluster.local:5000/generate-pipeline \
     -H "Content-Type: application/json" \
     -d '${jsonPayload}'
'''
```

---

## 🧠 Adaptive Intelligence

- Tries **local Ollama (Mistral)** model first
- Falls back to **OpenAI GPT-4o** if needed
- Behavior controlled via `service_dispatcher.py`

---

## 📥 MCP Logging

On successful LLM dispatch (with `prompt_path` and `response_path`), the gateway:

- Sends a structured **MCP message** to `ai-mcp-server`
- Logs source (`ai-gateway`), type, microservice, summary, and tags
- Useful for observability and audit trails

---

## 🔐 Security & Next Steps

- Token-based authentication (planned)
- Input validation & sanitization in place
- Structured logging (WIP)

---

## 🔮 Planned Modules

- `/explain-error`: traceback analysis
- `/summarize-pipeline`: CI/CD definition summarizer
- `/compare-logs`: diffing log sequences

---

## 👨‍💻 Author

**Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🛡 License

GNU General Public License v3.0