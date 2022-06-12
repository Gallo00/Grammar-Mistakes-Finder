# Calcolo degli errori grammaticali nei testi dei Tweet in real time
 
Per usare l'applicazione la prima volta lanciare il comando <br>
>- docker compose up --build <br>
facendo però attenzione che la cartella di lavoro sia projTAP <br>
Dopo aver stoppato l'esecuzione si può riprendere lanciando <br>
>- docker compose up  <br>
facendo però attenzione che prima sia stato lanciato il comando <br>
>- docker compose down <br>

Se si volessero resettare tutti i dati relativi all'indice Elastic Search e al servizio Kibana lanciare <br>
>- docker compose down -v
