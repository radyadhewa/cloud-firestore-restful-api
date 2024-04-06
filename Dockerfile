FROM python:3.10
RUN apt-get update && apt-get install -y python3-pip
WORKDIR /restful-api
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]