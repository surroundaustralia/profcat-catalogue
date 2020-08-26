import os
from catprez.source import *
from catprez.model import *

APP_DIR = os.environ.get("APP_DIR", os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", os.path.join(APP_DIR, "view", "templates"))
STATIC_DIR = os.environ.get("STATIC_DIR", os.path.join(APP_DIR, "view", "style"))
LOGFILE = os.environ.get("LOGFILE", os.path.join(APP_DIR, "catprez.log"))
DEBUG = False
PORT = os.environ.get("PORT", 5000)
CACHE_HOURS = os.environ.get("CACHE_HOURS", 1)
CACHE_FILE_PATH = os.environ.get("CACHE_DIR", os.path.join(APP_DIR, "cache", "DATA.pickle"))
LOCAL_URIS = os.environ.get("LOCAL_URIS", True)
CLASS_RENDERERING_PREFERENCE_ORDER = [
    "http://www.w3.org/ns/dcat#Catalog",
    "http://www.w3.org/ns/dcat#Dataset",
    "http://www.w3.org/ns/dcat#DataService",
    "http://purl.org/dc/dcmitype/Service",
    "http://www.w3.org/ns/dcat#Resource",
    "http://www.w3.org/2002/07/owl#Ontology",
    "http://purl.org/dc/dcmitype/Software",
    "http://www.w3.org/2004/02/skos/core#ConceptScheme",
    "http://purl.org/dc/terms/Standard",
    "http://www.w3.org/ns/dcat#Distribution",
    "https://schema.org/Person",
    "https://schema.org/Organization",
    "http://www.w3.org/2002/07/owl#NamedIndividual",
]
CLASS_RENDERER = {
    "http://www.w3.org/ns/dcat#Catalog": CatalogueRenderer,
    "http://www.w3.org/ns/dcat#Dataset": ResourceRenderer,
    "http://www.w3.org/ns/dcat#DataService": DataServiceRenderer,
    "http://purl.org/dc/dcmitype/Service": DataServiceRenderer,
    "http://www.w3.org/ns/dcat#Resource": ResourceRenderer,
    "http://www.w3.org/ns/dcat#Distribution": DistributionRenderer,
    "https://schema.org/Person": AgentRenderer,
    "https://schema.org/Organization": AgentRenderer,
    "http://www.w3.org/2002/07/owl#Ontology": ResourceRenderer,
    "http://purl.org/dc/dcmitype/Software": ResourceRenderer,
    "http://www.w3.org/2004/02/skos/core#ConceptScheme": ResourceRenderer,
    "http://purl.org/dc/terms/Standard": ResourceRenderer,
}


class DataSourceTypes:
    FILE = FILE
    SPARQL = SPARQL


DATA_SOURCES = [
    {
        "name": "Local Files",
        "source": DataSourceTypes.FILE,
        "data_folder": "CP_DATA_DIR",
        "cache_age": CACHE_HOURS * 3600
    }
]
CATALOGUE_URI = "https://w3id.org/dggs/cat"
