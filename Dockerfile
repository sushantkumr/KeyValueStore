FROM python:3.9.1
COPY . /keyvaluestore-app
WORKDIR /keyvaluestore-app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["server.py"]
