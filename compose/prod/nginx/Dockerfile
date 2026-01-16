FROM nginx:1.29-alpine

RUN addgroup --system django \
    && adduser --system --ingroup django django

ENV APP_HOME=/home/app

RUN mkdir $APP_HOME

RUN mkdir /etc/nginx/ssl \
    && chown -R django:django $APP_HOME

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/default.conf
