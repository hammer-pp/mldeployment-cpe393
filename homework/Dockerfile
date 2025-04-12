FROM python:3.9-slim

WORKDIR /homework/app

COPY app/ /homework/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["python", "app.py"]
