FROM debian:stretch-slim

MAINTAINER Phillip Bailey <phillip@bailey.st>
ENV PYTHONIOENCODING=utf-8
ENV DEBIAN_FRONTEND noninteractive
ADD sources.list /etc/apt/
RUN echo "nameserver 114.114.114.114" >> /etc/resolv.conf
RUN apt-get update
RUN apt-get update  && apt-get install -y \
    python-pip python-dev uwsgi-plugin-python \
    nginx supervisor

COPY nginx/flask.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY app /var/www/app

RUN mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
&& rm /etc/nginx/sites-enabled/default \
&& ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
&& echo "daemon off;" >> /etc/nginx/nginx.conf \
&&  pip install -r /var/www/app/requirements.txt \
&& chown -R www-data:www-data /var/www/app \
&& chown -R www-data:www-data /var/log

CMD ["/usr/bin/supervisord"]