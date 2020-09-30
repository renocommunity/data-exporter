FROM httpd:2.4.46-alpine

COPY ./mr_project /var/www/html/mr_project
ADD ./docker/httpd.conf /usr/local/apache2/conf/httpd.conf
ADD ./docker/entrypoint.sh /entrypoint.sh
ADD ./requirements.txt /tmp/requirements.txt
RUN chmod +x /entrypoint.sh

RUN apk update \
    && apk add --no-cache python3-dev==3.8.5-r0 py3-pip==20.1.1-r0 postgresql-dev==12.3-r2 \
    && apk add --no-cache --virtual build-deps gcc==9.3.0-r2 musl-dev==1.1.24-r9 apache2-mod-wsgi==4.7.1-r0 \
    && pip3 install --no-cache-dir -r /tmp/requirements.txt \
    && cp /usr/lib/apache2/mod_wsgi.so /usr/local/apache2/modules/ \
    && apk del --purge build-deps

EXPOSE 80

CMD ["httpd-foreground"]
ENTRYPOINT ["/entrypoint.sh"]