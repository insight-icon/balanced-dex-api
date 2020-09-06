FROM python:3.7


EXPOSE 8000

COPY ./app /app

RUN pip install fastapi uvicorn
RUN pip install -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]