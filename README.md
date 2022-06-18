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
## LanguageTool
LanguageTool è un ottimo strumento (utilizzato anche da aziende molto importanti come riportato nell'home page) per individuare (e anche correggere) errori grammaticali presenti in un testo. <br>
La potenza di questo strumento è data dal fatto che supporti moltissime lingue oltre all'inglese. <br>
Per semplificarci la vita, invece di interagire direttamente con le API, useremo una libreria in Python che farà il lavoro sporco per noi. <br>
La libreria, come riportato nella tabella, si chiama language_tool_python. <br>
**Codice di esempio** 
```python
import language_tool_python

tool = language_tool_python.LanguageToolPublicAPI('it')
s = "sto faccendo un erore gramma"
matches = tool.check(s)
print(len(matches)) #4
```
In questo caso usiamo LanguageToolPublicAPI che comporta ovviamente richiamare le API (e sostanzialmente far svolgere i calcoli su un server remoto). <br>
Un'alternativa potrebbe essere richiamare la funzione LanguageTool('it') che sostanzialmente darebbe lo stesso risultato ma creando un server sulla macchina locale, quindi i calcoli verrebbero fatti in locale. <br>
La scelta da prendere dipende da due variabili che sono la potenza di calcolo della macchina e la qualità della connessione alla rete. Per approfondire vedere la repo del wrapper https://github.com/jxmorris12/language_tool_python <br>

## Architettura dell'applicazione
![Pipeline](/review/img/pipeline.png?raw=true "Architettura dell'applicazione")

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
