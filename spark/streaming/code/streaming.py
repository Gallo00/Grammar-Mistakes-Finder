from pprint import pprint
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import types as st
from pyspark.sql.functions import from_json, col, udf

from elasticsearch import Elasticsearch

import language_tool_python

APP_NAME = 'compute_grammar_mistakes'
APP_BATCH_INTERVAL = 1
#tool = language_tool_python.LanguageToolPublicAPI('en') 


elastic_host="https://es01:9200"
elastic_index="tweets"

es_mapping = {
    "mappings": {
        "properties": 
            {
                "created_at": {"type": "date","format": "EEE MMM dd HH:mm:ss Z yyyy"},
                "text": {"type": "text","fielddata": True},
                "lang": {"type": "text","fielddata": True},
                "G_mistakes": {"type":"integer"}
            }
    }
}

#NEL FILE ca.crt SI PUO' VEDERE LA "FORMA" CHE DOVREBBE AVERE UN CERTIFICATO
es = Elasticsearch(
    hosts=elastic_host,
    ca_certs="/app/certs/ca/ca.crt",
    basic_auth=("elastic", "passwordTAP"), 
) 
# make an API call to the Elasticsearch cluster
# and have it return a response:
response = es.indices.create(
    index=elastic_index,
    body=es_mapping,
    ignore=400 # ignore 400 already exists code
)

if 'acknowledged' in response:
    if response['acknowledged'] == True:
        print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])


def get_record_schema():
    return st.StructType([
        st.StructField('text',         st.StringType()),
        st.StructField('lang',         st.StringType()),
        st.StructField('created_at',         st.StringType()),
    ])

def get_mistakes_count(txt,lang):
    # Bisogna fare attenzione alle lingue non supportate dal tool
    # se si provasse a generare il tool con una lingua non supportata ci sarebbe un errore che 
    # farebbe morire il container di spark streaming
    # Se una lingua non è supportata ritorniamo -1

    try:
        tool = language_tool_python.LanguageToolPublicAPI(lang)
        x = tool.check(txt)
        return len(x)
    except:
        return -1

def process_batch(batch_df, batch_id):
    #funzione per scrivere/mandare sull'indice elastic_index i dati
    for idx, row in enumerate(batch_df.collect()):
        row_dict = row.asDict()
        resp = es.index(
            index=elastic_index, 
            document=row_dict)
        print(resp)

def main():

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    schema = get_record_schema()
    
    df = spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'kafkaserver:9092') \
        .option('subscribe', 'tweets') \
        .option("maxOffsetsPerTrigger",1) \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")) \
        .selectExpr("data.*")

    #print(type(df))
    #<class 'pyspark.sql.dataframe.DataFrame'>

    # aggiungere colonna a df
    GMC = udf(lambda x, y: get_mistakes_count(x,y),st.IntegerType() )

    df_G = df.withColumn('G_mistakes',GMC(col('text'),col('lang')))

    df_G_filtered = df_G.filter(df_G.G_mistakes > -1) #non ci interessa streammare i contenuti non analizzabili

    
    """
    #per debug
    df_G_filtered.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()
    """
    df_G_filtered.writeStream \
        .foreachBatch(process_batch) \
        .start() \
        .awaitTermination()


if __name__ == '__main__': main()

