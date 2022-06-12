# Calcolo degli errori grammaticali nei testi dei Tweet in real time

Nota: fare attenzione alla cartella in cui si lanciano i comandi "docker compose".<br>
E' necessario essere nella cartella projTAP.<br>

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

|Servizio                | link                   | Note                                              |
|------------------------|------------------------|---------------------------------------------------|
|KafkaUI                 |http://localhost:8080   | Per controllare lo stato dei topic e dei messaggi |
|Cluster Elastic Search  |https://localhost:9200/ | Per visualizzare l'indice                         |
|Kibana                  |http://localhost:5601/  | Per accedere alla dashboard                       |

## Approfodimenti
Per approfondire visualizzare https://github.com/Gallo00/projTAP/blob/main/review/review.ipynb
