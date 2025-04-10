FROM python:3.12

WORKDIR /app

COPY ./frontend /app

RUN pip install --no-cache-dir -r streamlit_requirements.txt

CMD ["streamlit", "run", "streamlit_app.py"]