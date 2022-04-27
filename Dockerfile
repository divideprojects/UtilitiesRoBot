FROM python:3.10.4
WORKDIR .
COPY . .
RUN pip3 install requirements.txt
CMD [ "python3", "-m" , "bots"]