from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import DCAT, DCTERMS, PROF, RDF, RDFS, SDO

g = Graph().parse("dataprofiles-dev.ttl", format="turtle")
g2 = Graph()
g2.bind("dcat", DCAT)
g2.bind("dcterms", DCTERMS)
g2.bind("sdo", SDO)

"""
<https://linked.data.gov.au/def/agop>
  a dcat:Resource ;
  dcterms:identifier "agop" ;
  dcterms:type <http://www.w3.org/ns/dx/prof/Profile> ;
  dcterms:title "Australian Government Ontologies Profile"@en ;
  dcterms:description "A profile for the publication of ontologies mandated by the Australian Government Linked Data Working Group to ensure ontologies contain sufficinet metadata for cataloguing. Unofficial as of August, 2020." ;
  dcterms:creator <https://surroundaustralia.com> ;
  dcterms:created "2020-06-25"^^xsd:date ;
  dcterms:modified "2020-08-25"^^xsd:date ;
  dcterms:publisher <https://surroundaustralia.com>  ;
  sdo:codeRepository <https://github.com/agldwg/agop> ;
  dcat:distribution
    <https://linked.data.gov.au/def/agop.html> ,
    <https://linked.data.gov.au/def/agop.ttl>
.
"""
"""
profiles:skos_concept
  a prof:Profile ;
  rdfs:comment "Provides a view of a definition as a SKOS concept. Entailments include broader/narrower, topConceptOf and inScheme links. Could profile a standard profile for SKOS when available." ;
  rdfs:label "SKOS Concept" ;
  prof:hasToken "concept"^^xsd:token ;
  prof:isProfileOf <http://www.w3.org/2004/02/skos/core> ;
.
"""
ogc = URIRef("https://www.ogc.org")
for s in g.subjects(predicate=RDF.type, object=PROF.Profile):
    if str(s).startswith("https://w3id.org/profile/"):
        g2.add((s, RDF.type, DCAT.Resource))
        g2.add((s, DCTERMS.type, PROF.Profile))
        g2.add((s, DCTERMS.creator, ogc))
        g2.add((s, DCTERMS.publisher, ogc))
        g2.add((s, SDO.codeRepository, URIRef("https://github.com/opengeospatial/NamingAuthority")))
        for p, o in g.predicate_objects(subject=s):
            if p == PROF.hasToken:
                g2.add((s, DCTERMS.identifier, o))
            elif p == RDFS.label:
                g2.add((s, DCTERMS.title, o))
            elif p == RDFS.comment:
                g2.add((s, DCTERMS.description, o))
            elif p == DCTERMS.created:
                g2.add((s, DCTERMS.created, o))
            elif p == DCTERMS.modified:
                g2.add((s, DCTERMS.modified, o))
            elif p == DCTERMS.issued:
                g2.add((s, DCTERMS.issued, o))

        html = URIRef(str(s) + ".html")
        g2.add((s, DCAT.distribution, html))
        g2.add((html, RDF.type, DCAT.Distribution))
        g2.add((html, DCTERMS.type, SDO.DigitalDocument))
        g2.add((html, DCTERMS.title, Literal("The profile, in HTML format")))
        g2.add((html, DCTERMS["format"], URIRef("https://w3id.org/mediatype/text/html")))

        ttl = URIRef(str(s) + ".ttl")
        g2.add((s, DCAT.distribution, ttl))
        g2.add((ttl, RDF.type, DCAT.Distribution))
        g2.add((ttl, DCTERMS.type, SDO.DigitalDocument))
        g2.add((ttl, DCTERMS.title, Literal("The profile, in RDF, Turtle format")))
        g2.add((ttl, DCTERMS["format"], URIRef("https://w3id.org/mediatype/text/turtle")))

g2.serialize(destination="ogc-profiles.ttl", format="turtle")
