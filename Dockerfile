FROM python:3.10.8-alpine
WORKDIR /bot
ENV BOT_APP = main.py

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "./main.py"]