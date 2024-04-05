FROM python:3.10
RUN apt-get update
RUN apt-get install -y python3-pip
COPY . /restful-api
WORKDIR /restful-api
RUN pip install -r requirements.txt
CMD [ "python", "main.py", "config.py","api/ticketAPI.py", "api/stadiumAPI.py", "api/__init__.py", "api/key.json"]