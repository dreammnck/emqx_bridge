FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY . .
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

CMD python3 -m uvicorn main:app