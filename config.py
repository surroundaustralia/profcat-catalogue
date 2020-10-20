import os
from catprez.model import *
from rdflib import Graph, util
from pathlib import Path
import pickle
import logging
import catprez.utils


APP_DIR = os.environ.get("APP_DIR", Path(__file__).parent)
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", APP_DIR / "view" / "templates")
STATIC_DIR = os.environ.get("STATIC_DIR", APP_DIR / "view" / "style")
LOGFILE = os.environ.get("LOGFILE", APP_DIR / "catprez.log")
DEBUG = os.environ.get("DEBUG", True)
PORT = os.environ.get("PORT", 5000)
CACHE_HOURS = os.environ.get("CACHE_HOURS", 1)
CACHE_FILE = os.environ.get("CACHE_FILE", APP_DIR / "cache" / "DATA.pickle")
LOCAL_URIS = os.environ.get("LOCAL_URIS", True)
CLASS_RENDERERING_PREFERENCE_ORDER = [
    "http://www.w3.org/ns/dx/prof/Profile",
    "http://www.w3.org/ns/dcat#Catalog",
    "http://www.w3.org/ns/dcat#Dataset",
    "http://www.w3.org/ns/dcat#DataService",
    "http://purl.org/dc/dcmitype/Service",
    "http://www.w3.org/ns/dcat#Resource",
    "http://www.w3.org/2002/07/owl#Ontology",
    "http://purl.org/dc/dcmitype/Software",
    "http://www.w3.org/ns/dcat#Distribution",
    "https://schema.org/Person",
    "https://schema.org/Organization",
    "http://www.w3.org/2002/07/owl#NamedIndividual",
]
CLASS_RENDERER = {
    "http://www.w3.org/ns/dx/prof/Profile": ProfileRenderer,
    "http://www.w3.org/ns/dcat#Catalog": CatalogueRenderer,
    "http://www.w3.org/ns/dcat#DataService": DataServiceRenderer,
    "http://purl.org/dc/dcmitype/Service": DataServiceRenderer,
    "http://www.w3.org/ns/dcat#Distribution": DistributionRenderer,
    "https://schema.org/Person": AgentRenderer,
    "https://schema.org/Organization": AgentRenderer,
}
MANAGED_URIS = {}

DATA_DIR = Path(os.environ.get("DATA_DIR", APP_DIR / "data"))
CATALOGUE_URI = os.environ.get("CATALOGUE_URI", "http://example.com/cat")


def get_graph():
    # try to load static data from a pickle file
    logging.debug(CACHE_FILE)
    if Path.is_file(CACHE_FILE):
        logging.debug("loading g from cache")
        with open(CACHE_FILE, 'rb') as f:
            g = pickle.load(f)
    else:
        logging.debug("no cache - reloading g from source files")
        g = Graph()
        for rdf_file in DATA_DIR.glob("*.*"):
            g.parse(str(rdf_file), format=util.guess_format(rdf_file))

        catprez.utils.do_dcat_expansion(g)

        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(g, f)

    return g
