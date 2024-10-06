# AviMate-LLM

### Introduction

```AviMate``` a Pilot Cockpit Assistance Tool involves creating an application that aids pilots by summarizing Flight manuals, Air Traffic Control (ATC) communications and providing relevant flight information in real-time. This tool aims to enhance situational awareness, reduce workload, and improve safety during flight operations.


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

### To run the streamlit app
```bash
streamlit run app.py
```

## Experiments

For experiments, we use Jupyter notebooks.
They are in the [`notebooks`](notebooks/) folder.

To start Jupyter, run:

```bash
cd notebooks
pipenv run jupyter notebook
```

We have the following notebooks:

- [`rag-test.ipynb`](notebooks/rag-test.ipynb): The RAG flow and evaluating the system.
- [`evaluation-data-generation.ipynb`](notebooks/evaluation-data-generation.ipynb): Generating the ground truth dataset for retrieval evaluation.
- [`evaluate-vector-retrieval.ipynb`](notebooks/evaluate-vector-retrieval.ipynb): Elastic serach result evaluation.
- [`rag-evaluation.ipynb`](notebooks/rag-evaluatation.ipynb): to evaluate the LLM answers by LLM as a Judge approach.



## Retrieval Evaluation

The basic approach - using `ElasticSearch` without any boosting - gave the following metrics:

    - Hit Rate: 0.550
    - MRR: 0.259

The improved version (with tuned boosting): Boosts: {'text': 1.22, 'scenario': 2.81, 'manual_section': 1.95, 'instructions': 2.61}
    - Hit Rate: 0.550
    - MRR: 0.259


## RAG Evaluation
* Offline Evaluation and Online Evaluation
1. Offline Evaluation: for each question from the ground truth data, answers have generated and classified as NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT using gpt-4o-mini and data is stored in [`flight-manuals-evaluations-qa.csv`](data/flight-manuals-evaluations-qa.csv). Classification carried out by LLM as a Judge approach.
 - out of 150 answers, 149 are classified Relevant answer to the given question.

### Streamlit

We use Streamlit for creating the WEB interference for our application. 




