FROM python:3.9

RUN apt-get update
RUN apt-get install git -y
RUN pip install --upgrade pip

WORKDIR /home

COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt
#RUN python3 -m spacy download en_core_web_sm

RUN bash