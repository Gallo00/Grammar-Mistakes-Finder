FROM jupyter/pyspark-notebook:spark-3.1.1

RUN pip install language-tool-python elasticsearch
RUN pip3 install pyspark numpy 

WORKDIR /app

COPY ./code .

ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1", "--master", "local[*]", "streaming.py"]