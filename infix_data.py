from typing import Iterable
from frozendict import frozendict

from game_state import ALPHABET

ALPHABET_SET = frozenset(ALPHABET)


class InfixData:
    def __init__(self, words: Iterable[str]) -> None:
        self.words = set(words)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        can_add_at_start = {c: set[str]() for c in alphabet}
        can_add_at_end = {c: set[str]() for c in alphabet}

        for word in self.words:
            for i in range(len(word)):
                for l in range(1, len(word) - i):
                    j = i + l
                    substring = word[i:j]
                    if i > 0:
                        before = word[i - 1]
                        can_add_at_start[before].add(substring)
                    if j < len(word):
                        after = word[j]
                        can_add_at_end[after].add(substring)

        # Make the dictionaries immutable.
        self.can_add_at_start = frozendict(
            {l: frozenset(words) for l, words in can_add_at_start.items()}
        )
        self.can_add_at_end = frozendict(
            {l: frozenset(words) for l, words in can_add_at_end.items()}
        )

        # Get the dictionaries that go in the other direction.
        infix_to_prefixes = dict[str, set[str]]()
        for prefix, infixes in self.can_add_at_start.items():
            for infix in infixes:
                if not infix in infix_to_prefixes:
                    infix_to_prefixes[infix] = set[str]()
                infix_to_prefixes[infix].add(prefix)

        infix_to_suffixes = dict[str, set[str]]()
        for suffix, infixes in self.can_add_at_end.items():
            for infix in infixes:
                if not infix in infix_to_suffixes:
                    infix_to_suffixes[infix] = set[str]()
                infix_to_suffixes[infix].add(suffix)

        # TODO Maybe use tuple instead of frozenset
        self.infix_to_prefixes = frozendict(
            {
                infix: frozenset(prefixes)
                for infix, prefixes in infix_to_prefixes.items()
            }
        )
        self.infix_to_suffixes = frozendict(
            {
                infix: frozenset(suffixes)
                for infix, suffixes in infix_to_suffixes.items()
            }
        )

    # Return all possible suffixes for the given string.
    def get_all_suffixes(self, s: str) -> frozenset[str]:
        if s == "":
            return ALPHABET_SET
        return self.infix_to_suffixes.get(s, frozenset())

    # Return all possible prefixes for the given string.
    def get_all_prefixes(self, s: str) -> frozenset[str]:
        if s == "":
            return ALPHABET_SET
        return self.infix_to_prefixes.get(s, frozenset())
