from typing import Iterable
from frozendict import frozendict


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
