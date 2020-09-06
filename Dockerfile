FROM python:3.7

COPY ./app /app

RUN pip install fastapi uvicorn
RUN pip install -r /app/requirements.txt

EXPOSE 8000
# EXPOSE 80

RUN apt-get update && apt-get install -y netcat

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]