from config import LAMBDA

class Partition:
    suffixes = set(LAMBDA)
    prefixes = set(LAMBDA)

    def __init__(self, codeword: str, root_idx: int, suff_idx: int):
        if (root_idx < 0 or root_idx > suff_idx or suff_idx > len(codeword)):
            raise ValueError(f"Value error: {codeword}, {root_idx}, {suff_idx}")
        self.word = codeword
        self.root_idx = root_idx
        self.suff_idx = suff_idx

        Partition.prefixes.add(self.pref)
        Partition.suffixes.add(self.suff)

    def __get_pref(self ):
        res = self.word[:self.root_idx]
        return LAMBDA if res == "" else res 
    
    def __get_root(self):
        res = self.word[self.root_idx:self.suff_idx]
        return LAMBDA if res == "" else res

    def __get_suff(self):
        res = self.word[self.suff_idx:]
        return LAMBDA if res == "" else res    

    pref = property(__get_pref)
    root = property(__get_root)
    suff = property(__get_suff)

    def __str__(self):
        return f"{self.pref}.{self.root}.{self.suff}"

    def __repr__(self):
        return Partition.__str__(self)

    def __hash__(self):
        return hash((self.word, self.root_idx, self.suff_idx))
    
    def __eq__(self, value):
        if not isinstance(value, Partition):
            return False
        return (
            self.word == value.word and
            self.root_idx == value.root_idx and
            self.suff_idx == value.suff_idx
        )
