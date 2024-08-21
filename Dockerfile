FROM python:3.8

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m pip install python-dotenv
COPY . .

EXPOSE 5000
CMD ["flask", "run"]