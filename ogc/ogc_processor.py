from rdflib import Graph, Literal, URIRef, BNode
from rdflib.namespace import DCAT, DCTERMS, PROF, RDF, RDFS, SDO

g = Graph().parse("ogc-profiles-prof.ttl", format="turtle")
g2 = Graph()
g2.bind("dcat", DCAT)
g2.bind("dcterms", DCTERMS)
g2.bind("sdo", SDO)

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

g2.serialize(destination="ogc-profiles-dcat.ttl", format="turtle")
