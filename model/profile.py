from pyldapi import Renderer
from flask import Response, render_template
from catprez.model.resource import Resource, ResourceRenderer
from catprez.model.profiles import profile_prof, profile_dcat, profile_sdo
from rdflib import Graph, URIRef
from rdflib.namespace import DCAT, DCTERMS, PROF, SDO
import markdown


class ProfileRenderer(ResourceRenderer):
    def __init__(self, request, instance_uri: str, data_source_graph: Graph):
        self.data_source_graph = data_source_graph
        self.profiles = {
            "prof": profile_prof,
            "sdo": profile_sdo,
            "dcat": profile_dcat
        }
        self.resource = Resource(instance_uri, data_source_graph)

        super(ResourceRenderer, self).__init__(request, instance_uri, self.profiles, "prof")

    def render(self):
        # try returning alt profile
        response = super().render()
        if response is not None:
            return response
        elif self.profile == "prof":
            if self.mediatype in Renderer.RDF_SERIALIZER_TYPES_MAP:
                g = self._render_prof_rdf()
                return super(ResourceRenderer, self)._make_rdf_response(g)
            else:
                return self._render_prof_html()

    def _render_prof_rdf(self):
        # get the graph of this resource from the main graph
        g = Graph()
        g.bind("dcterms", DCTERMS)
        g.bind("prof", PROF)
        s = URIRef(self.instance_uri)
        for p, o in self.data_source_graph.predicate_objects(s):
            if str(p).startswith(PROF) or str(p).startswith(DCTERMS):
                g.add((s, p, o))

        for s2, p in self.data_source_graph.subject_predicates(s):
            if str(p).startswith(PROF):
                g.add((s2, p, s))

        for o in self.data_source_graph.objects(subject=s, predicate=PROF.hasResource):
            for p2, o2 in self.data_source_graph.predicate_objects(subject=o):
                if str(p2).startswith(PROF) or str(p2).startswith(DCTERMS):
                    g.add((o, p2, o2))

        return g

    def _render_prof_html(self):
        title = None
        description = None
        created = None
        modified = None
        creator = None
        publisher = None
        isProfileOf = []
        hasToken = None

        s = URIRef(self.instance_uri)
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
                    for o2 in self.data_source_graph.objects(subject=o, predicate=DCTERMS.title):
                        isProfileOf.append((str(o), str(o2)))
                elif p == PROF.hasToken:
                    hasToken = str(o)

        if any(elem is None for elem in [self.instance_uri, title, publisher, hasToken]):
            return Response(
                "The Profile you requested, {}, is missing Profile information and cannot be displayed. It must have"
                "a URI, title, publisher and a token."
                    .format(self.instance_uri),
                headers=self.headers,
            )

        _template_context = {
            "uri": self.instance_uri,
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
