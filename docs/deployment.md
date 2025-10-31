# Deployment Guide

## Local Development
1. Create a virtual environment: `make install-dev`
2. Run the CLI demo: `make demo`
3. Launch the Gradio UI: `make gradio`

Set environment variables for live LLM calls:
```bash
export OPENAI_API_KEY=sk-...
export MODEL_PROVIDER=openai:gpt-4o-mini
```

## Docker
```bash
docker build -t ai-agent-patterns .
docker run -p 7860:7860 -e OPENAI_API_KEY=$OPENAI_API_KEY ai-agent-patterns
```

## Hugging Face Spaces
- Copy the `huggingface_space` directory into your Space root.
- Add secrets for API keys under the Space settings.
- The default `app.py` imports the Gradio app from `demos.gradio_interface`.
- Spaces automatically install dependencies from `huggingface_space/requirements.txt`.

## Cloud Kubernetes (Optional)
- Build and push the Docker image to your registry.
- Use the following deployment snippet as a starting point:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-patterns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-agent-patterns
  template:
    metadata:
      labels:
        app: ai-agent-patterns
    spec:
      containers:
        - name: app
          image: <registry>/ai-agent-patterns:latest
          ports:
            - containerPort: 7860
          envFrom:
            - secretRef:
                name: llm-credentials
---
apiVersion: v1
kind: Service
metadata:
  name: ai-agent-patterns
spec:
  selector:
    app: ai-agent-patterns
  ports:
    - port: 80
      targetPort: 7860
      protocol: TCP
```
