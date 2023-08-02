# syntax=docker/dockerfile:1

FROM ubuntu:latest

# Atualiza o SO
RUN apt-get update && apt-get upgrade -y

# Instala o python3, pip3 e o git
RUN apt-get install python3 python3-pip git unzip libnss3 wget curl xvfb -y

# Instala Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
RUN apt-get install -f -y

# Instala Chromedriver
RUN wget http://chromedriver.storage.googleapis.com/`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip && chmod +x chromedriver
RUN mv chromedriver /usr/local/share/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
RUN chromedriver --version
RUN google-chrome --version

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app

COPY req.txt req.txt
RUN pip3 install -r req.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "main.py"]