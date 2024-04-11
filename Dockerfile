FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN python3 -m ensurepip


RUN pip3 install -r requirements.txt 

COPY . . 

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]