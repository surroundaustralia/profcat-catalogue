import logging
from rdflib import Graph, URIRef, Namespace, BNode
from rdflib.namespace import DCAT, DCTERMS, PROF, RDF, SDO, SKOS
from pyldapi.renderer import Renderer


# def cache_load()

def cache_expand(g: Graph):
    """This is the ProfCat cache builder expansion: it creates dcat:Resources from prof:Profile classes for CatPrez
    """
    logging.info("Running profiles.py's plugin cache_expand(g)")

    ROLE = Namespace("http://www.w3.org/ns/dx/prof/role/")

    # for each prof:Profile in the cache, re-class it a dcat:Resource
    for s in g.subjects(predicate=RDF.type, object=PROF.Profile):
        g.add((s, RDF.type, DCAT.Resource))

    # convert all tokens to identifiers
    for s, o in g.subject_objects(predicate=PROF.hasToken):
        g.add((s, DCTERMS.identifier, o))

    # infer that each prof:Profile instances prof:hasResource objects are prof:ResourceDescriptor instances
    for s, o in g.subject_objects(predicate=PROF.hasResource):
        g.add((o, RDF.type, PROF.ResourceDescriptor))

    # for each prof:ResourceDescriptor in the cache, re-class it a dcat:Distribution
    for s in g.subjects(predicate=RDF.type, object=PROF.ResourceDescriptor):
        g.add((s, RDF.type, DCAT.Distribution))

    # link the dcat:Resource instances with their dcat:Distribution instances
    for s, o in g.subject_objects(predicate=PROF.hasResource):
        g.add((s, DCAT.distribution, o))

    # make the prof:ResourceDescriptor's prof:hasArtifact object the object of the dcat:Distribution's dcat:downloadURL
    for s, o in g.subject_objects(predicate=PROF.hasArtifact):
        g.add((s, DCAT.downloadURL, o))

    # type each dcat:Distribution from the prof:ResourceDescriptor's various properties
    doc_types = ["text/html", "text/xml", "application/json"] + Renderer.RDF_MEDIA_TYPES
    for s in g.subjects(predicate=RDF.type, object=PROF.ResourceDescriptor):
        for p, o in g.predicate_objects(subject=s):
            if p == DCTERMS['format']:
                if str(o) in doc_types:
                    g.add((s, DCTERMS.type, SDO.DigitalDocument))
            if p == PROF.hasRole:
                if o == ROLE.repository:
                    g.add((s, DCTERMS.type, URIRef("https://w3id.org/profile/catprez/OnlineVCSRepo")))

    # for each prof:Profile, ensure that it is added to the Catalogue
    for c in g.subjects(predicate=RDF.type, object=DCAT.Catalog):
        for s in g.subjects(predicate=RDF.type, object=PROF.Profile):
            g.add((c, DCTERMS.hasPart, s))

    # slot Profile into top of rendering order
    RT = Namespace("https://w3id.org/profile/catprez/resourcetypes/")
    for o in g.objects(subject=RT["rendering-order"], predicate=SKOS.memberList):
        for o2 in g.objects(subject=o, predicate=RDF.first):
            # remove existing first
            g.remove((o, RDF.first, o2))

            # add in new first
            g.add((o, RDF.first, URIRef("http://www.w3.org/ns/dx/prof/Profile")))

            # add in a new BN
            b0 = BNode()
            g.add((o, RDF.rest, b0))

            # add former first to BN
            g.add((b0, RDF.first, o2))

            for o3 in g.objects(subject=o, predicate=RDF.rest):
                # join new BN to rest
                g.add((b0, RDF.rest, o3))
