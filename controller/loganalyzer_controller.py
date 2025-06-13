import kopf, kubernetes, os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

@kopf.on.create('mlops.dev', 'v1alpha1', 'loganalyzers')
@kopf.on.update('mlops.dev', 'v1alpha1', 'loganalyzers')
def analyze_logs(spec, name, namespace, patch, **kwargs):
    ns = spec.get('namespace', namespace)
    sel = spec.get('podSelector', {})
    prompt = spec.get('prompt', 'Analise logs:')
    model = spec.get('llmModel', 'gpt-3.5-turbo')

    k8s = kubernetes.client.CoreV1Api()
    sel_str = ",".join(f"{k}={v}" for k, v in sel.items())
    pods = k8s.list_namespaced_pod(ns, label_selector=sel_str).items

    collated = ""
    for p in pods:
        try:
            log = k8s.read_namespaced_pod_log(p.metadata.name, ns, tail_lines=200)
            collated += f"\n== Pod: {p.metadata.name} ==\n{log}"
        except Exception as e:
            collated += f"\n== Pod: {p.metadata.name} ERROR: {e}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um analista de logs Kubernetes."},
            {"role": "user", "content": f"{prompt}\n{collated}"}
        ]
    )
    analysis = response.choices[0].message.content

    patch.status['analysis'] = analysis
    kopf.info(f"Análise armazenada no status do LogAnalyzer/{name}")