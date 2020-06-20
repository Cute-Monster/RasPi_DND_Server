FROM arm32v7/python:3.7-stretch

RUN mkdir ./DND_Server/

WORKDIR ./DND_Server/

ENV SSH_Host="178.132.***.***"
ENV SSH_Port=*****
ENV SSH_Username="pi"
ENV SSH_Password="*********"
ENV SSH_RemoteBindHost="localhost"
ENV SSH_RemoteBindPort=****
ENV DataBase_Host="localhost"
ENV DataBase_Name="*********"
ENV DataBase_Username="*********"
ENV DataBase_Password="*********"


COPY ./Logs/ ./Logs/
COPY ./Requirements ./Requirements/
COPY ./src/ ./src/
COPY ./server.py ./

RUN ls -la

RUN pwd
RUN echo "Python -> $(python3 -V)"
RUN pip3 --version

RUN pip3 install --no-cache-dir -U -r ./Requirements/requirements.txt

ENTRYPOINT ["python3", "server.py"]
