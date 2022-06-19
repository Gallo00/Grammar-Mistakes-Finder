# Stream Processing for detection of Grammatical Errors in various languages
## Project for the university course "Technologies for advanced programming" AA 2021/22
The following application provides a stream processing service of Tweets obtained in real time. <br>
The goal is to get for each tweet the number of grammatical errors in the text. <br>
A Kibana dashboard is provided for data visualization. <br>

## Technologies used

|Technology              | Link                                 | Note                                         |
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
|Python + pyspark|https://spark.apache.org/docs/latest/api/python/index.html      |Python library to manage the Spark cluster                    |
## LanguageTool
LanguageTool is an excellent tool (also used by very important companies as reported on the home page) to identify (and even correct) grammatical errors in a text. <br>
The power of this tool is that it supports many languages besides English. <br>
To make our life easier, instead of interacting directly with the API, we will use a library in Python that will do the dirty work for us. <br>
The library, as shown in the table, is called language_tool_python. <br>
**Sample code** 
```python
import language_tool_python

tool = language_tool_python.LanguageToolPublicAPI('it')
s = "sto faccendo un erore gramma"
matches = tool.check(s)
print(len(matches)) #4
```
In this case we use LanguageToolPublicAPI which obviously involves calling the API (and basically having the calculations done on a remote server). <br>
An alternative could be to call the LanguageTool('it') function which would basically give the same result but creating a server on the local machine, so the calculations would be done locally. <br>
The choice depends on two variables which are the computing power of the machine and the quality of connection to the network. View more https://github.com/jxmorris12/language_tool_python <br>

## Architecture
![Pipeline](/review/img/pipeline.png?raw=true "Application architecture")

## Run the application
Download this repo as you want <br> <br>
Docker must be running on your computer <br> <br>
Before running the application you need to modify the file logstash.conf located in logstash/pipeline/<br>
You will need to enter your credentials to access the Twitter APIs. <br>
The values of the following 4 fields must be entered: <br>
>- consumer_key <br>
>- consumer_secret <br>
>- oauth_token <br>
>- oauth_token_secret <br>

Another necessary step before running the application for the first time is to run the following command
>- docker network create -d bridge --subnet 10.0.100.0/16 tap <br>

A network will be created to connect the various containers <br>
Note: on a Windows environment you have to use WSL 2<br>

Note: Pay attention to the folder where the "docker compose" commands are launched. <br>
It' necessary to launch commands in the project folder.<br>

To use the application for the first time, run the command <br>
>- docker compose up --build <br>

After stopping the execution, launch the command <br>
>- docker compose down <br>
(without this operation; next time the application is started, spark-streaming will fail) <br>

If you also want to reset all the data relating to the Elastic Search index and the Kibana service, launch <br>
>- docker compose down -v <br>
instead of command <br>
>- docker compose down <br>

To reuse the application run the command <br>
>- docker compose up <br>

If, on the other hand, changes have been made to the project, launch the command for safety
>- docker compose up --build <br>

### Credentials for Kibana and Elastic
>- user: elastic
>- password: passwordTAP

## Import the dashboard into Kibana
In the "importDB" folder there is the "export.ndjson" file which contains configurations to be able to use an already implemented dashboard. <br>
To import the file, open the "hamburger" at the top left of the Kibana page, open "Stack Management", "Saved Objects", click on "import", drag the ndjson file and then press "import". <br>

![Pipeline](/importDB/tutorial/1hamburger.JPG?raw=true "step1") <br>
![Pipeline](/importDB/tutorial/2stack_management.JPG?raw=true "step2") <br>
![Pipeline](/importDB/tutorial/3saved_obj.JPG?raw=true "step3") <br>
![Pipeline](/importDB/tutorial/4import.JPG?raw=true "step4") <br>
![Pipeline](/importDB/tutorial/5import2.JPG?raw=true "step5") <br>


## Exit status 78 of es01 using WSL
The es01 container could come out with exit status 78, going to see the errors you will probably see the message <br>
>- "Elasticsearch: Max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]". <br>
The error message states that the memory granted to the WSL is too low <br>

If this is the case, it should be sufficient to run these two commands using a prompt before compose up: <br>
>- wsl -d docker-desktop
>- sysctl -w vm.max_map_count=262144

## Useful links
A few moments after launching the docker compose up it will be possible to access some services, obviously including Kibana to view the dashboard (s) 

|Service                 | Link                   | Note                                              |
|------------------------|------------------------|---------------------------------------------------|
|KafkaUI                 |http://localhost:8080   | To check the status of topics and their messages  |
|Cluster Elastic Search  |https://localhost:9200/ | To view the ES index                              |
|Kibana                  |http://localhost:5601/  | To access the dashboard                           |

View more (only in Italian) https://github.com/Gallo00/Grammar-Mistakes-Finder/blob/main/review/review.ipynb
