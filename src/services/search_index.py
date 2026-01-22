from elasticsearch import Elasticsearch
import os

ES_HOST = os.getenv("ES_HOST", "localhost")
INDEX_NAME = "documents"


def get_es_client():
    return Elasticsearch(
        hosts=[{"host": ES_HOST, "port": 9200, "scheme": "http"}],
        verify_certs=False
    )

def create_index_if_not_exists():
    es = get_es_client()
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "tags": {"type": "keyword"}
                    }
                }
            }
        )

def index_document(doc: dict):
    es = get_es_client()
    create_index_if_not_exists()
    es.index(index=INDEX_NAME, id=doc["id"], document=doc)
