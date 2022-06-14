# Stream Processing per l'identificazione di Errori Grammaticali in varie lingue
## Progetto per il corso universitario Technologies for Advanced Programming AA 2021/22
La seguente applicazione fornisce un servizio stream processing di Tweets ricavati in real time. <br>
L'obiettivo è per ogni tweet ottenere il numero di errori grammaticali presenti nel testo. <br>
Viene fornita una dashboard Kibana per la data visualization. <br>

## Teconologie usate

|Tecnologia              | Link                                 | Note                                      |
|------------------------|--------------------------------------|-------------------------------------------|
|Twitter (API)           |https://developer.twitter.com/en      | E' necessario creare un account developer |
|Docker                  |https://www.docker.com/               | Serve per containerizzare i servizi       |
|Logstash                |https://www.elastic.co/logstash/      | Data Ingestion                            |
|Kafka                   |https://kafka.apache.org/             | Data streaming                            |
|Spark                   |https://spark.apache.org/             | Data Processing                           | 
|Elastic Search          |https://www.elastic.co/elasticsearch/ | Data Indexing                             |
|Kibana                  |https://www.elastic.co/kibana/        | Data Visualization                        |
|Language Tool           |https://languagetool.org              | Servizio che dato un testo in una certa lingua ne corregge gli errori grammaticali                     |
|language_tool_python                  |https://github.com/jxmorris12/language_tool_python/ | Wrapper in python che mette a disposizione una libreria ad alto livello per richiamare le API di Language Tool                       |
|Python + libreria pyspark|https://spark.apache.org/docs/latest/api/python/index.html      |Libreria python per manovrare il cluster Spark                    |
## Architettura dell'applicazione
![Pipeline](/review/img/pipeline.png?raw=true "Architettura dell'applicazione")

## Eseguire l'applicazione 

Nota: fare attenzione alla cartella in cui si lanciano i comandi "docker compose".<br>
E' necessario essere nella cartella del progetto.<br>

Per usare l'applicazione la prima volta lanciare il comando <br>
>- docker compose up --build <br>

Dopo aver stoppato l'esecuzione si può riprendere lanciando <br>
>- docker compose up  <br>
facendo però attenzione che prima sia stato lanciato il comando <br>
>- docker compose down <br>

Se si volessero resettare tutti i dati relativi all'indice Elastic Search e al servizio Kibana lanciare <br>
>- docker compose down -v <br>

Nel caso siano state fatte modifiche al progetto, lanciare per sicurezza il comando
>- docker compose up --build <br>

## Exit status 78 di es01 con esecuzione da WSL
Potrebbe il container es01 uscire con exit status 78, andando a vedere gli errori probabilmente ci si imbatterà nel messaggio <br>
>- "Elasticsearch: Max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]". <br>
L'errore è causato perchè la memoria concessa alla WSL è troppo bassa. <br>

Se dovesse essere così, dovrebbe essere sufficiente lanciare questi 2 comandi prima della compose up: <br>
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
Per approfondire visualizzare https://github.com/Gallo00/Grammar-Mistakes-Finder/blob/main/review/review.ipynb
