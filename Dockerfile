FROM library/nginx:latest

RUN mkdir -p /data
RUN apt-get update && apt-get install -y python python3 python3-pip

ADD ./ /data/
WORKDIR /data
COPY nginx.conf /etc/nginx/nginx.conf
RUN python3 -m pip install -r requirement.txt
RUN python3 main.py&

EXPOSE 80 9999
