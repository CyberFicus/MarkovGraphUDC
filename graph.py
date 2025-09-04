from config import LAMBDA

class Node:
    nodes = {}

    def __init__(self, node_name: str):
        if (node_name is None):
            raise ValueError("node_name is None")
        if (node_name == ""):
            raise ValueError("node_name is empty")
        self.name = node_name
        self.links = {}
        self.linked_nodes = set()

        Node.nodes[node_name] = self
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, value):
        if (not isinstance(value, Node)):
            return False
        
        return (
            self.name == value.name and 
            self.links == value.links
        )

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def link(self, dst :'Node', link_name :str):
        newlink = Link(self, dst, link_name)
        self.links[dst] = newlink
        self.linked_nodes.add(dst)
        return newlink     

class Link:
    def __init__(self, src :Node, dst :Node, link_name :str):
        if (src is None):
            raise ValueError("src in None")
        if (dst is None):
            raise ValueError("dst is none")
        if (link_name is None):
            raise ValueError("link_name is None")
        if (link_name == ""):
            raise ValueError("link_name is empty")
        
        self.src = src
        self.dst = dst
        self.name = link_name

    def __hash__(self):
        return hash((self.src, self.dst, self.name))

    def __eq__(self, value):
        if (not isinstance(value, Link)):
            return False
        return (
            self.name == value.src and
            self.src == value.src and
            self.dst == value.dst
        )
    
    def __str__(self):
        return f"{self.src} -({self.name})-> {self.dst}"
    
    def __repr__(self):
        return self.__str__()