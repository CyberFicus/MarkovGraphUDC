from utils import parse_file
from partition import Partition as prt

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


fname = "input/in1.txt"
codewords = parse_file(fname)

partitions = get_all_partitions(codewords)
final_partitions = set([p for p in partitions if (
    isinstance(p, prt) and
    p.pref in prt.suffixes and
    p.suff in prt.prefixes
)])

print("\nPartitions:")
print(final_partitions)