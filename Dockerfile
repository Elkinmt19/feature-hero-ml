FROM python:3.9.7-slim

WORKDIR /feature_hero_repo

COPY ["./feature_hero_repo/*", "./"]
COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN mkdir offline_store registry && \
    mv *.parquet offline_store && \
    mv registry.db registry

RUN pip install -U pip
RUN pip install pipenv 
RUN pipenv install --system --deploy

EXPOSE 8888
EXPOSE 6566

RUN feast serve &

ENTRYPOINT [ "feast","ui" ]