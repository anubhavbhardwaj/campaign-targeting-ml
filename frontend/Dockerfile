FROM python:3.11-slim

WORKDIR /app

COPY requirements-frontend.txt .
RUN pip install -r requirements-frontend.txt

COPY frontend/ frontend/
COPY settings.py settings.py
COPY pyproject.toml pyproject.toml

RUN pip install -e .

EXPOSE 8080

CMD ["sh", "-c", "streamlit run frontend/app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]