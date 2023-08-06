from pytextrust.pytextrust import wrap_literal_replacer, wrap_literal_replacer_from_lookup, \
    wrap_lookup_write, wrap_lookup_load, wrap_map_lookup_load
from typing import List
from enum import Enum
from pytextrust.constants import get_logger
import pickle

logger = get_logger()


class MatchKind(Enum):
    LeftmostLongest = "LeftmostLongest"
    Standard = "Standard"
    LeftmostFirst = "LeftmostFirst"


class AhoCorasickKind(Enum):
    NoncontiguousNFA = "NoncontiguousNFA"
    ContiguousNFA = "ContiguousNFA"
    DFA = "DFA"
    Auto = "Auto"


def replace_literal_patterns(literal_patterns: List[str], replacements: List[str], text_to_replace: List[str],
                             is_bounded: bool = True, case_insensitive: bool = True,
                             match_kind: MatchKind = MatchKind.LeftmostLongest, n_jobs: int = 1,
                             aho_corasick_kind: AhoCorasickKind = AhoCorasickKind.Auto):
    """
    Function to replace literal patterns in texts. A literal pattern consists only in unicode characters, without
    anchors, repetitions, groups or any regex specific symbol, just literals.

    The list literal_patterns is searched and found over the provided text_to_replace list, substituting each
    literal in literal_patterns by its corresponding replacement in replacements list.

    Options:
    - is_bounded: if True, it forces the literal pattern to be bounded by non-words/numbers to be replaced
    - case_insensitive: if True, ignores case.
    - match_kind corresponds to different matching possibilities described here 
        https://docs.rs/aho-corasick/latest/aho_corasick/enum.MatchKind.html
    - n_jobs: -1 means to use all paralellization available, 1 just one thread, N to set to exactly N threads

    It returns the replaced texts and the numbers of total replacements on all texts provided.
    """
    text_list, n_reps = wrap_literal_replacer(patterns=literal_patterns,
                                              replacements=replacements,
                                              texts=text_to_replace,
                                              is_bounded=is_bounded,
                                              case_insensitive=case_insensitive,
                                              match_kind=match_kind.value,
                                              n_jobs=n_jobs,
                                              aho_corasick_kind=aho_corasick_kind.value)

    return text_list, n_reps


def replace_literal_patterns_from_lookup(lookup_path: str, text_to_replace: List[str],
                                         is_bounded: bool = True, case_insensitive: bool = True,
                                         match_kind: MatchKind = MatchKind.LeftmostLongest, n_jobs: int = 1,
                                         aho_corasick_kind: AhoCorasickKind = AhoCorasickKind.Auto):
    """
    Same than function before but uses local lookup saved data to perform substitutions
    """
    text_list, n_reps = wrap_literal_replacer_from_lookup(path=lookup_path,
                                                          texts=text_to_replace,
                                                          is_bounded=is_bounded,
                                                          case_insensitive=case_insensitive,
                                                          match_kind=match_kind.value,
                                                          n_jobs=n_jobs,
                                                          aho_corasick_kind=aho_corasick_kind.value)

    return text_list, n_reps


def load_lookup(path: str):
    src, dst = wrap_lookup_load(path)
    return src, dst


def write_lookup(src_list: List[str], dst_list: List[str], path: str):
    wrap_lookup_write(source=src_list, destination=dst_list, path=path)


def load_map_lookup(path: str):
    lookup_dict = wrap_map_lookup_load(path)
    return lookup_dict


class LookUpReplacer:

    def __init__(self, path, load_pickle=True):
        self.path = path
        self.lookup_dict = None
        self.load_pickle = load_pickle
        self.load_lookup()

    def load_lookup(self):
        if self.load_pickle:
            with open(self.path, mode='rb') as file:
                self.lookup_dict = pickle.load(file)
        else:
            self.lookup_dict = load_map_lookup(self.path)

    def write_pickle(self, pickle_path):
        with open(pickle_path, mode='wb') as file:
            pickle.dump(self.lookup_dict, file)

    def reduce_token(self, token):
        return self.lookup_dict.get(token, token)
