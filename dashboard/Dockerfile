FROM python:3.10

RUN apt-get update -y
RUN apt-get install -y python-dev build-essential

RUN mkdir /usr/src/crime

WORKDIR /usr/src/crime

COPY ./requirements.txt ./
RUN pip install --upgrade -r requirements.txt

COPY ./ ./
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]