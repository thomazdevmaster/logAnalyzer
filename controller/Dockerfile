FROM python:3.11-slim
RUN pip install kopf kubernetes openai google-generativeai
COPY loganalyzer_controller.py /app/
ENTRYPOINT ["kopf", "run", "--standalone", "/app/loganalyzer_controller.py"]