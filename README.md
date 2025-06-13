# LogAnalyzer Operator

Um operador Kubernetes que usa LLMs (como GPT-3.5/GPT-4) para analisar logs de pods com base em seletores definidos no recurso `LogAnalyzer`.

## 📦 Componentes

- **CRD**: Define o recurso `LogAnalyzer`
- **Controller**: Implementado em Python com `kopf`
- **Dockerfile**: Imagem do operador
- **Helm Chart**: Facilita a instalação
- **RBAC**: Permissões mínimas necessárias

---

## 🚀 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/thomazdevmaster/logAnalyzer.git
cd loganalyzer-operator
```

### 2. Configure a chave da OpenAI

Crie um `Secret` com sua chave:

```bash
kubectl create secret generic openai-secret --from-literal=apiKey=$OPENAI_API_KEY
kubectl create secret generic gemini-secret --from-literal=apiKey=$GOOGLE_API_KEY
```

### 3. Build da imagem Docker

```bash
cd controller
docker build -t loganalyzer-operator:latest .
```

Envie para seu repositório, se necessário:

```bash
docker tag loganalyzer-operator:latest seu-repo/loganalyzer-operator:latest
docker push seu-repo/loganalyzer-operator:latest
```

### 4. Instale via Helm

```bash
cd helm
helm install loganalyzer ./loganalyzer --namespace default --create-namespace
```

### 5. Aplique o CRD

```bash
kubectl apply -f crd/loganalyzer-crd.yaml
```

### 6. Crie um recurso `LogAnalyzer`

```yaml
apiVersion: mlops.dev/v1alpha1
kind: LogAnalyzer
metadata:
  name: nginx-analyzer
spec:
  namespace: default
  podSelector:
    app: nginx
  llmModel: gpt-3.5-turbo
  prompt: "Analise os logs e identifique erros ou padrões estranhos."
```

```bash
kubectl apply -f loganalyzer.yaml
```

### 7. Verifique a análise

```bash
kubectl get loganalyzer nginx-analyzer -o jsonpath="{.status.analysis}"
```

---

## ✅ Requisitos

- Python 3.11+
- Kubernetes 1.20+
- Helm 3+
- Docker
- Chave da API da OpenAI

---

## 📌 Dicas

- Use seletores para limitar o escopo dos pods.
- Edite `tail_lines` no controller se quiser logs mais longos.
- A resposta da LLM fica salva no campo `.status.analysis`.

---

MIT License