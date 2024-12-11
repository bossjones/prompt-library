"""
This type stub file was generated by pyright.
"""

from pylint.pyreverse.printer import EdgeType, NodeProperties, NodeType, Printer

"""Class to generate files in dot format and image formats supported by Graphviz."""
class PlantUmlPrinter(Printer):
    """Printer for PlantUML diagrams."""
    DEFAULT_COLOR = ...
    NODES: dict[NodeType, str] = ...
    ARROWS: dict[EdgeType, str] = ...
    def emit_node(self, name: str, type_: NodeType, properties: NodeProperties | None = ...) -> None:
        """Create a new node.

        Nodes can be classes, packages, participants etc.
        """
        ...

    def emit_edge(self, from_node: str, to_node: str, type_: EdgeType, label: str | None = ...) -> None:
        """Create an edge from one node to another to display relationships."""
        ...
