# state-of-indices

Fetch the state of all indices in an Elastic search cluster and return the name of index, age, number of documents etc.

## Index structure
Index names consist of 2 parts, the content type that is indexed and the timestamp that indicates the creation time of the index. The index "media-1641833637" means that the content type is “media”, 1641833637 in the name of the index is a unix timestamp which gives us the information that the index was created on the 10th of January at 16:53 GMT.
The index "media-1641833637" has next aliases:
[ {"alias": "media--read", "index": "media-1641833637", "is_write_index": "false"},
{"alias": "media--write", "index": "media-1641833637", "is_write_index": "true"}]
Required data:
- Age of indices
- Number of documents in each index
- Flag indices that have both read and write aliases


## How to run
### Prerequisites
- Setup Elastic search using a docker container on your local and get it running
```
docker pull elasticsearch:7.17.2
docker network create dockernetwork
docker run -d --name elasticsearch --net dockernetwork -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.2
```

- Install all dependencies listed in file `prerequisite/requirements.txt` 
```
pip install -r prerequisite/requirements.txt

```
- Run the file `prerequisite/populate_es.py`
```
python prerequisite/populate_es.py  prerequisite/populate_es_config.yaml

```

### To get state of indices
- Build the Dockerfile
```
docker build -t indices .

```

- Run the docker container as follows (Note: As the docker container needs access to elastic search which is running as a docker container, specify the network):
```
docker run --net dockernetwork indices

```
