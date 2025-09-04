from config import LAMBDA
from utils import parse_file
from partition import Partition as prt
from graph import Node as node, Link as link 

def findall(base_word: str, root_word: str):
    res = []
    i = 0

    while (True):
        i = base_word.find(root_word, i)
        
        if i == -1:
            break

        res.append(i)
        i += 1

    return res

def build_partitions(
        base_word: str,
        root_len :int,
        root_idx :int,
        codewords :list
):
    res = []
    suff_idx = root_idx + root_len 
    res.append(prt(base_word, root_idx, suff_idx))

    suff_len = len(base_word) - suff_idx

    if suff_len < 1:
        return res

    for word in codewords:
        if not isinstance(word,str):
            continue 
        if len(word) > suff_len:
            break
        
        if (base_word.find(word,suff_idx) == suff_idx):
            res.extend(
                build_partitions(
                    base_word, 
                    root_len + len(word),
                    root_idx,
                    codewords
                )
            )
    
    return res

def get_all_partitions(codewords: list):
    res = set()

    for base_word in codewords:
        if (not isinstance(base_word, str)):
            continue

        bwlen = len(base_word)
        if (bwlen < 2):
            continue
        
        # simple partitions
        for i in range(1,bwlen):
            res.add(prt(base_word,i,i))

        # complex partitions
        for word in codewords:
            if len(word) >= len(base_word):
                break
            root_starts = findall(base_word, word)

            if len(root_starts) == 0:
                continue

            for i in root_starts:
                buf = build_partitions(
                    base_word, 
                    len(word),
                    i,
                    codewords
                )
                
                for partition in buf:
                    res.add(partition)
    return res

def build_graph(partitions: list):
    node_names = prt.prefixes.intersection(prt.suffixes)
    lambda_node = None

    # create nodes
    for node_name in node_names:
        if (not isinstance(node_name, str)):
            continue

        n = node(node_name)
        if (node_name == LAMBDA):
            lambda_node = n

    # build links
    for partition in partitions:
        if (
            not isinstance(partition, prt) or
            not partition.pref in prt.suffixes or
            not partition.suff in prt.prefixes
        ):
            continue
        if (partition.pref not in node.nodes):
            print(f"WARNING: {partition.pref} not in nodes!")
            continue
        if (partition.suff not in node.nodes):
            print(f"WARNING: {partition.suff} not in nodes!")
            continue

        src = node.nodes[partition.pref]
        dst = node.nodes[partition.suff]

        if (not isinstance(src, node)):
            print(f"WARNING: src {partition.pref} is not a node!")
        if (not isinstance(dst, node)):
            print(f"WARNING: dst {partition.suff} is not a node!")

        src.link(dst, partition.root)

    if (lambda_node is None):
        print("WARNING: lambda node is none!!!")
    
    return lambda_node

passed_nodes = set()

def find_way(src: node, dst :node):
    res = []
    passed_nodes.add(src)

    def find_link_to(dst :node):
        if (dst not in src.linked_nodes):
            raise Exception(f"{dst} not linked to {src}")
        
        l = src.links[dst]
        if (not isinstance(l, link)):
            raise Exception(f"{l} in links of node {src} is not a link")
        if (l.src != src):
            raise Exception(f"link {l} does not belong to node {src}")
        if (l.dst != dst):
            raise Exception(f"{l} links to {l.dst} instead of {dst}")
        return l

    if ( # dst one link away
        src != dst and        
        dst in src.linked_nodes
    ):     
        passed_nodes.remove(src)
        return [find_link_to(dst)]

    for n in src.linked_nodes:
        if (not isinstance(n, node)):
            print(f"WARNING: {n} in linked nodes of {src}")
            continue
        if ( # infinite loop ahead
            n == src or 
            n in passed_nodes
        ): 
            continue

        buf = find_way(n, dst)
        if (buf != []):
            res = [find_link_to(n)]
            res.extend(buf)
            passed_nodes.remove(src)   
            return res
    
    passed_nodes.remove(src)
    return res
        
fname = "input/in1.txt"
codewords = parse_file(fname)

partitions = get_all_partitions(codewords)

print("\nPartitions:")
print(partitions)

lambda_node = build_graph(partitions)
cycle = find_way(lambda_node, lambda_node)

if (cycle != []):
    print("\nCycle is:")
    for l in cycle:
        print(l)
else:
    print("\nCycle not found")