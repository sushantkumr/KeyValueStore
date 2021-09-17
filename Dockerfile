FROM python:3.9.1
ADD . /keyvaluestore-app
WORKDIR /keyvaluestore-app
RUN pip install -r requirements.txt
EXPOSE 5000
