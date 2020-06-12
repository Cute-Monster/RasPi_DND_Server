FROM python:3.7

RUN mkdir ./DND_Server/

WORKDIR ./DND_Server/

COPY ./Logs/ ./Logs/
COPY ./Requrements/ ./Requrements/
COPY ./src/ ./src/
COPY ./server.py ./

RUN ls -la

RUN pwd

RUN pip install --no-cache-dir -U -r ./Requrements/requirements.txt

ENTRYPOINT ["python", "server.py"]