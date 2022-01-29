FROM python:3.9

RUN apt-get update && apt-get install git -y
RUN pip install --upgrade pip

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "/home/src/main.py"]
