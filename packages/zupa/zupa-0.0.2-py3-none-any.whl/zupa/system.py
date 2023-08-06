import ipaddress
from dataclasses import dataclass
import arklog
import logging
from pathlib import Path
import owlready2
from rdflib import Graph
from owly import Endpoint, QueryResult


@dataclass(frozen=True, slots=True)
class Server:
    """Single server."""
    name: str
    address: ipaddress.ip_address


def load_ontologies():
    """"""
    data_path = Path("data/classes.ttl")
    g = Graph()
    g.parse(data_path)
    # v = g.serialize(destination="data/hm.xml", format="xml")
    # onto = owlready2.get_ontology(str("data/hm.xml")).load()
    servers_file_path = Path("data/individuals.ttl")


def main():
    """"""
    arklog.set_config_logging()
    load_ontologies()


if __name__ == "__main__":
    main()
