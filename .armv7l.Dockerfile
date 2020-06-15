FROM arm32v7/python:3.7-stretch

RUN mkdir ./DND_Server/

WORKDIR ./DND_Server/

ENV SSH_Host="178.132.156.98"
ENV SSH_Port=22458
ENV SSH_Username="pi"
ENV SSH_Password="lafMNGQ4"
ENV SSH_RemoteBindHost="localhost"
ENV SSH_RemoteBindPort=3306
ENV DataBase_Host="localhost"
ENV DataBase_Name="CodeDungeon"
ENV DataBase_Username="CodeDungeon"
ENV DataBase_Password="CodeDungeon"


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
