import os
from catprez.source import *
from catprez.model import *

APP_DIR = os.environ.get("APP_DIR", os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", os.path.join(APP_DIR, "view", "templates"))
STATIC_DIR = os.environ.get("STATIC_DIR", os.path.join(APP_DIR, "view", "style"))
LOGFILE = os.environ.get("LOGFILE", os.path.join(APP_DIR, "catprez.log"))
DEBUG = True
PORT = os.environ.get("PORT", 5000)
CACHE_HOURS = os.environ.get("CACHE_HOURS", 1)
CACHE_FILE_PATH = os.environ.get("CACHE_DIR", os.path.join(APP_DIR, "cache", "DATA.pickle"))
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
    "http://www.w3.org/2004/02/skos/core#ConceptScheme",
    "http://purl.org/dc/terms/Standard",
    "http://www.w3.org/ns/dcat#Distribution",
    "https://schema.org/DigitalDocument",
    "https://schema.org/Person",
    "https://schema.org/Organization",
    "http://www.w3.org/2002/07/owl#NamedIndividual",
]
CLASS_RENDERER = {
    "https://schema.org/DigitalDocument": ResourceRenderer,
    "http://www.w3.org/ns/dx/prof/Profile": ResourceRenderer,
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


DATA_SOURCES = [
    {
        "name": "Local Files",
        "source": DataSourceTypes.FILE,
        "data_folder": "/Users/nick/Work/surround/catprez-overlay-profcat/data",
        "cache_age": CACHE_HOURS * 3600
    }
]
CATALOGUE_URI = "https://w3id.org/profile"

MANAGED_URIS = {
    "https://w3id.org/profile/dcat2null": [
        {
            "label": "Specification Resource",
            "from": "https://w3id.org/profile/dcat2null/specification",
            "to": "https://github.com/surroundaustralia/dcat2-null-profile/blob/master/specification.md",
        },
        {
            "label": "Validation Resource",
            "from": "https://w3id.org/profile/dcat2null/validation",
            "to": "https://raw.githack.com/surroundaustralia/dcat2-null-profile/master/validaton.ttl",
        },
        {
            "label": "DCAT2 Specification Resource",
            "from": "https://w3id.org/profile/dcat2null/dcat2",
            "to": "https://raw.githack.com/surroundaustralia/dcat2-null-profile/master/dcat2.ttl",
        },
        {
            "label": "Data Expanders Resource",
            "from": "https://w3id.org/profile/dcat2null/dataexpanders",
            "to": "https://github.com/surroundaustralia/dcat2-null-profile/tree/master/dataexpanders",
        },
        {
            "label": "Redirects Resource",
            "from": "https://w3id.org/profile/dcat2null/redirects",
            "to": "https://github.com/surroundaustralia/dcat2-null-profile/tree/master/redirects.txt",
        },
        {
            "label": "Profile RDF (turtle) via file ext.",
            "from": "https://w3id.org/profile/dcat2null.ttl",
            "to": "https://raw.githack.com/surroundaustralia/dcat2-null-profile/master/profile.ttl",
        },
        {
            "label": "Profile HTML",
            "from": "https://w3id.org/profile/dcat2null.html",
            "to": "https://github.com/surroundaustralia/dcat2-null-profile/blob/master/profile.md",
        },
    ],
}
