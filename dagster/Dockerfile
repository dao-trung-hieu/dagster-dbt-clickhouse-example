FROM python:3.11-slim

ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY dagster/requirements.txt $DAGSTER_HOME/requirements.txt
RUN pip install -r requirements.txt 
COPY dagster $DAGSTER_HOME

ENTRYPOINT ["dagster","dev","-h","0.0.0.0","-p","3000","-m","data_pipeline"]
