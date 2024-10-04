# AviMate-LLM

### Introduction

Developing a Pilot Assistance Tool involves creating an application that aids pilots by summarizing Air Traffic Control (ATC) communications and providing relevant flight information in real-time. This tool aims to enhance situational awareness, reduce workload, and improve safety during flight operations.


Create Venv with python 3.11

### Install below dependancies and activate the venv
```bash
pipenv --python 3.11
pipenv install ipython openai scikit-learn pandas flask streamlit
pipenv shell
```

### Install Development depencies
```bash
pipenv install elasticsearch openpyxl --dev
pipenv install spacy dateparser --dev
pipenv run python -m spacy download en_core_web_sm
pipenv install sentence-transformers --dev
pipenv install openai-whisper --dev
```

### RUn the Elastic Search with Docker
```bash
docker run -it \
    --rm \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```
### OR you can also run Elastic Search using Docker-compose.yaml file.
```bash
docker-compose up

### Running the ollama Model
#### Pulling the model using service-name from the docker-compose.yaml file
```bash
docker-compose exec ollama bash
ollama pull phi3
```

### To do Speech Queries we will use OPENAI's whisper model



