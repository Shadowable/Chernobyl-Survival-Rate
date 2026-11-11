FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py streamlit_app.py ./

RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 5000 8501

CMD ["waitress-serve", "--listen=0.0.0.0:5000", "--call", "app:create_app"]
