FROM python:3.12-rc-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . . 

CMD ["python", "main.py"]