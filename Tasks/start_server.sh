#!/bin/bash -i
echo "Started at : $( date) and $(/home/pi/Desktop/DND_Server/venv/bin/python3.7 --version)" >> /home/pi/Desktop/DND_Server/Logs/terminal.log
cd /home/pi/Desktop/DND_Server
/home/pi/Desktop/DND_Server/venv/bin/python3.7 server.py