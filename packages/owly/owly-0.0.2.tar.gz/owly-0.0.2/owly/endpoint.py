import base64
import json
import urllib
from http.client import HTTPResponse
from typing import Any, Dict, Iterator, Optional
from rdflib import Graph
from owly import __version__

class QueryResult:
    def __init__(self, result: HTTPResponse):
        self.result = result
        self.value = result.read()

    def as_text(self) -> str:
        """Return a textual representation of the response."""
        return self.value.decode("utf-8")

    def as_json(self) -> Dict[Any, Any]:
        """Return the result as a json dictionary."""
        return json.loads(self.value.decode("utf-8"))

    def as_list(self) -> Iterator[dict]:
        """Return an interator for the items returned in the result."""
        for item in self.as_json().get("results", {"bindings": []}).get("bindings"):
            yield item

    def as_rdf_graph(self, incoming_format: str = "json-ld") -> Graph:
        """Return the result in the form of an rdflib Graph."""
        return Graph().parse(self.value, format=incoming_format)

class Endpoint:
    def __init__(self, endpoint: str, agent: str = f"Owly/{__version__}"):
        self.endpoint = endpoint
        self.agent = agent
        self.user: Optional[str] = None
        self.passwd: Optional[str] = None

    def perform_query(self, query: str | bytes) -> QueryResult:
        """
        Execute a query against the SPARQL endpoint.

        Queries are url-encoded and sent as a GET request.
        This means only certain (likely only 'query') operations are supported.
        The 'update' operation, for example, is not.
        """
        # TODO This requires more error handling!
        # http://www.w3.org/TR/sparql11-protocol/
        if isinstance(query, bytes):
            query = query.decode("utf-8")
        if not isinstance(query, str):
            raise TypeError("Query needs to be a string or utf-8 encoded value.")
        request = urllib.request.Request(self.endpoint + "?" + urllib.parse.urlencode({"query": query}))
        request.add_header("Accept", "*/*")  # TODO At the moment this causes a json response, but we need to specify it explicitly.
        request.add_header("User-Agent", self.agent)
        if self.user and self.passwd:
            credentials = f"{self.user}:{self.passwd}"
            encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
            request.add_header("Authorization", f"Basic {encoded}")
        response = urllib.request.urlopen(request)
        return QueryResult(response)


def main():
    endpoint = Endpoint("https://fuseki.rys.app/SystemDesignOntology2Layers/")
    result = endpoint.perform_query("""SELECT ?subject ?predicate ?object WHERE { ?subject ?predicate ?object } LIMIT 5""")
    print(result.as_text())

if __name__ == "__main__":
    main()
