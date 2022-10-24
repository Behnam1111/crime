FROM python:3.10

RUN apt-get update -y
RUN apt-get install -y python-dev build-essential

RUN mkdir /usr/src/app

WORKDIR /usr/src/crime

COPY ./requirements.txt ./
RUN pip install --upgrade -r requirements.txt

COPY ./ ./
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]