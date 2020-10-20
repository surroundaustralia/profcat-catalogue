from pyldapi import Renderer
from flask import Response, render_template
from catprez.model.resource import ResourceRenderer
from catprez.model.profiles import profile_dcat, profile_prof
from rdflib import Graph, URIRef
from rdflib.namespace import DCAT, DCTERMS, PROF, SDO
import markdown


class ProfileRenderer(ResourceRenderer):
    def __init__(self, request, resource_uri: str, data_source_graph: Graph):
        self.profiles = {"dcat": profile_dcat, "prof": profile_prof}
        self.uri = resource_uri
        self.data_source_graph = data_source_graph

        super(ResourceRenderer, self).__init__(request, resource_uri, self.profiles, "prof")

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response
        elif self.profile == "prof":
            if self.mediatype in Renderer.RDF_SERIALIZER_TYPES_MAP:
                return self._render_prof_rdf()
            else:
                return self._render_prof_html()

    def _render_prof_rdf(self):
        # get the graph of this resource from the main graph
        rg = Graph()
        rg.bind("dcterms", DCTERMS)
        rg.bind("prof", PROF)
        s = URIRef(self.uri)
        for p, o in self.data_source_graph.predicate_objects(s):
            if str(p).startswith(PROF) or str(p).startswith(DCTERMS):
                rg.add((s, p, o))

        for s2, p in self.data_source_graph.subject_predicates(s):
            if str(p).startswith(PROF):
                rg.add((s2, p, s))

        # serialise in the appropriate RDF format
        if self.mediatype in ["application/rdf+json", "application/json"]:
            return Response(rg.serialize(format="json-ld"), mimetype=self.mediatype, headers=self.headers)
        else:
            return Response(rg.serialize(format=self.mediatype), mimetype=self.mediatype, headers=self.headers)

    def _render_prof_html(self):
        title = None
        description = None
        created = None
        modified = None
        creator = None
        publisher = None
        isProfileOf = []
        hasToken = None

        s = URIRef(self.uri)
        for p, o in self.data_source_graph.predicate_objects(subject=s):
            if str(p).startswith(PROF) or str(p).startswith(DCTERMS):
                if p == DCTERMS.title:
                    title = str(o)
                elif p == DCTERMS.description:
                    description = markdown.markdown(str(o))
                elif p == DCTERMS.created:
                    created = str(o)
                elif p == DCTERMS.modified:
                    modified = str(o)
                elif p == DCTERMS.creator:  # TODO: handle BNode
                    for o2 in self.data_source_graph.objects(subject=o, predicate=SDO.name):
                        creator = (str(o), str(o2))
                elif p == DCTERMS.publisher:  # TODO: handle BNode
                    for o2 in self.data_source_graph.objects(subject=o, predicate=SDO.name):
                        publisher = (str(o), str(o2))
                elif p == PROF.isProfileOf:
                    isProfileOf.append(str(o))
                    # try and get the Profile's label
                    for o2 in self.data_source_graph.objects(subject=o2, predicate=DCTERMS.title):
                        isProfileOf.append((str(o), str(o2)))
                elif p == PROF.hasToken:
                    hasToken = str(o)

        if any(elem is None for elem in [self.uri, title, publisher, hasToken]):
            return Response(
                "The resource you requested, {}, is missing Profile information and cannot be displayed. It must have"
                "a URI, title, publisher and a token."
                    .format(self.uri),
                headers=self.headers,
            )

        _template_context = {
            "uri": self.uri,
            "title": title,
            "description": description,
            "created": created,
            "modified": modified,
            "creator": creator,
            "publisher": publisher,
            "isProfileOf": isProfileOf,
            "hasToken": hasToken
        }

        return Response(
            render_template("profile.html", **_template_context),
            headers=self.headers,
        )
