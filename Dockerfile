FROM python:3.8
WORKDIR /usr/src/shop-fast-api
COPY . .
COPY requiremenets.txt requiremenets.txt
RUN pip3 install -r requiremenets.txt