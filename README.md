# Stream Processing for detection of Grammatical Errors in various languages
## Project for the university course "Technologies for advanced programming" AA 2021/22
The following application provides a stream processing service of Tweets obtained in real time. <br>
The goal is to get for each tweet the number of grammatical errors in the text. <br>
A Kibana dashboard is provided for data visualization. <br>

## Technologies used

|Tecnologia              | Link                                 | Note                                         |
|------------------------|--------------------------------------|----------------------------------------------|
|Twitter (API)           |https://developer.twitter.com/en      | It's necessary to create a developer account |
|Docker                  |https://www.docker.com/               | Used to containerize services                |
|Logstash                |https://www.elastic.co/logstash/      | Data Ingestion                               |
|Kafka                   |https://kafka.apache.org/             | Data streaming                               |
|Spark                   |https://spark.apache.org/             | Data Processing                              | 
|Elastic Search          |https://www.elastic.co/elasticsearch/ | Data Indexing                                |
|Kibana                  |https://www.elastic.co/kibana/        | Data Visualization                           |
|Language Tool           |https://languagetool.org              | Service that, given a text in a certain language, corrects its grammatical errors                     |
|language_tool_python                  |https://github.com/jxmorris12/language_tool_python/ | Python wrapper that provides a high-level library to call the Language Tool APIs                       |
|Python + libreria pyspark|https://spark.apache.org/docs/latest/api/python/index.html      |Python library for maneuvering the Spark cluster                    |
## LanguageTool
LanguageTool is an excellent tool (also used by very important companies as reported on the home page) to identify (and even correct) grammatical errors in a text. <br>
The power of this tool is that it supports many languages besides English. <br>
To make our life easier, instead of interacting directly with the API, we will use a library in Python that will do the dirty work for us. <br>
The library, as shown in the table, is called language_tool_python. <br>
**Codice di esempio** 
```python
import language_tool_python

tool = language_tool_python.LanguageToolPublicAPI('it')
s = "sto faccendo un erore gramma"
matches = tool.check(s)
print(len(matches)) #4
```
In this case we use LanguageToolPublicAPI which obviously involves calling the API (and basically having the calculations done on a remote server). <br>
An alternative could be to call the LanguageTool('it') function which would basically give the same result but creating a server on the local machine, so the calculations would be done locally. <br>
The choice depends on two variables which are the computing power of the machine and the quality of connection to the network. View more on https://github.com/jxmorris12/language_tool_python <br>

## Application architecture
![Pipeline](/review/img/pipeline.png?raw=true "Application architecture")

## Eseguire l'applicazione 
Prima di eseguire l'applicazione è necessario modificare il file logstash.conf presente nella cartella logstash/pipeline/. <br>
Andranno inserite le proprie credenziali per l'accesso alle API di Twitter. <br>
Dunque si dovranno inserire i valori dei seguenti 4 campi:
>- consumer_key <br>
>- consumer_secret <br>
>- oauth_token <br>
>- oauth_token_secret <br>

Nota: fare attenzione alla cartella in cui si lanciano i comandi "docker compose".<br>
E' necessario essere nella cartella del progetto.<br>

Per usare l'applicazione la prima volta lanciare il comando <br>
>- docker compose up --build <br>

Dopo aver stoppato l'esecuzione lanciare il comando <br>
>- docker compose down <br>
(senza questa operazione al prossimo avvio dell'applicazione spark-streaming andrà in errore) <br>

Se si volessero anche resettare tutti i dati relativi all'indice Elastic Search e al servizio Kibana lanciare <br>
>- docker compose down -v <br>
al posto del comando <br>
>- docker compose down <br>

Per riusare l'applicazione lanciare il comando <br>
>- docker compose up <br>

Nel caso invece siano state fatte modifiche al progetto, lanciare per sicurezza il comando
>- docker compose up --build <br>

## Exit status 78 di es01 con esecuzione da WSL
Il container es01 potrebbe uscire con exit status 78, andando a vedere gli errori probabilmente ci si imbatterà nel messaggio <br>
>- "Elasticsearch: Max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]". <br>
L'errore è causato dal fatto che la memoria concessa alla WSL è troppo bassa. <br>

Se dovesse essere così, dovrebbe essere sufficiente lanciare questi 2 comandi su un prompt prima della compose up: <br>
>- wsl -d docker-desktop
>- sysctl -w vm.max_map_count=262144

## Link utili
Qualche istante dopo aver lanciato la docker compose up sarà possibile accedere ad alcuni servizi, tra cui ovviamente Kibana per visualizzare la/e dashboard 

|Servizio                | Link                   | Note                                              |
|------------------------|------------------------|---------------------------------------------------|
|KafkaUI                 |http://localhost:8080   | Per controllare lo stato dei topic e dei messaggi |
|Cluster Elastic Search  |https://localhost:9200/ | Per visualizzare l'indice                         |
|Kibana                  |http://localhost:5601/  | Per accedere alla dashboard                       |

## Approfodimenti
Per approfondire vedere https://github.com/Gallo00/Grammar-Mistakes-Finder/blob/main/review/review.ipynb
