FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev libmagic-dev \
  && apt-get install -y gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $HOME \
    && mkdir $APP_HOME

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/prod.txt

COPY ./compose/prod/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint \ 
    && chown django /entrypoint

COPY ./compose/prod/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start \ 
    && chown django /start

COPY --chown=django:django . $APP_HOME

RUN mkdir -p $APP_HOME/staticfiles
RUN chown -R django:django $APP_HOME

USER django
WORKDIR $APP_HOME

ENTRYPOINT ["/entrypoint"]
