FROM library/nginx:latest

RUN mkdir -p /data

ADD ./ /data/
WORKDIR /data
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
