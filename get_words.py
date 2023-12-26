import os
import itertools
import requests
import time
from html.parser import HTMLParser


class GetScrabbleWordsHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_word_list = False
        self.in_word = False
        self.all_words = list[str]()

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "entries") in attrs:
            self.in_word_list = True
            return

        if self.in_word_list and tag == "a":
            self.in_word = True

    def handle_endtag(self, tag):
        if tag == "div":
            self.in_word_list = False
            return
        if tag == "a":
            self.in_word = False

    def handle_data(self, data):
        if self.in_word:
            # print(f"Word: {data}")
            self.all_words.append(data.strip().upper())


# Return the words in the given response.
def get_words(resp: requests.Response) -> list[str] | None:
    try:
        parser = GetScrabbleWordsHtmlParser()
        parser.feed(resp.text)
        return parser.all_words
    except KeyboardInterrupt:
        raise
    except:
        return None


def get_address(letter, index) -> str:
    if index == 1:
        return f"https://scrabble.merriam.com/browse/{letter}"
    return f"https://scrabble.merriam.com/browse/{letter}/{index}"


def test_1():
    address = r"https://scrabble.merriam.com/browse/a"
    resp = requests.get(url=address)
    out_file = "resp.txt"
    with open(out_file, "w", encoding="utf-8") as file:
        file.write(resp.text)


def test_2():
    address = r"https://scrabble.merriam.com/browse/a"
    resp = requests.get(url=address)
    parser = GetScrabbleWordsHtmlParser()
    parser.feed(data=resp.text)
    for word in parser.all_words:
        print(word)


ACCESS_WEBSITE_DELAY = 0.001


def get_words_starting_with(letter: str) -> list[str] | None:
    result = list[str]()
    prev_words = list[str]()
    for i in itertools.count(start=1):
        address = get_address(letter=letter, index=i)

        # Wait just a little bit of time before accessing the website.
        time.sleep(ACCESS_WEBSITE_DELAY)
        print(f"  {address}")
        resp = requests.get(url=address)
        if resp.status_code != 200:
            print(f"Error {resp.status_code}")
            return None
        words = get_words(resp)
        if words is None:
            return None
        if words == prev_words:
            break
        prev_words = words
        result.extend(words)
    return result


def test_3():
    for letter in "abcdefghijklmnopqrstuvwxyz":
        # for letter in "q":
        # all_words_starting_with = list[str]()
        print("")
        print(f"Getting words starting with {letter}")
        words_starting_with = get_words_starting_with(letter=letter)
        if words_starting_with is None:
            print(f"Failed to get words starting with {letter}")
            continue

        out_filename = f"all_words_starting_with_{letter}.txt"
        with open(out_filename, "w") as file:
            for word in words_starting_with:
                file.write(f"{word}\n")

        # for word in words_starting_with:
        # all_words.extend(words_starting_with)

    # out_filename = "all_words.txt"
    # with open(out_filename, "w") as file:
    #     for word in all_words:
    #         file.write(f"{word}\n")


# def collect_all_words():
#     path = r"Scrabble_Words_Starting_With"
#     all_words = list[str]()
#     for filename in os.listdir(path):
#         with open(os.path.join(path, filename)) as file:
#             for line in file:
#                 line = line.strip()
#                 if not line:
#                     continue
#                 all_words.append(line)

#     out_path = os.path.join("Scrabble_Words", "all_scrabble_words.txt")
#     with open(out_path, "w") as file:
#         for word in all_words:
#             file.write(f"{word}\n")

ALL_WORDS_PATH = r"Scrabble_Words\all_scrabble_words.txt"


# Return all of the words in the Scrabble dictionary.
def get_all_words(_cache=list[str]()) -> list[str]:
    if not _cache:
        with open(ALL_WORDS_PATH) as file:
            for line in file:
                line = line.strip()
                if line:
                    _cache.append(line)
    return list(_cache)


def test_4():
    for word in get_all_words():
        print(word)


def get_all_substrings(s: str) -> list[str]:
    result = list[str]()
    for i in range(len(s)):
        for l in range(len(s) - i):
            result.append(s[i : i + l])
    return result


def make_infix_data():
    all_words = get_all_words()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    can_add_at_start = {c: set[str]() for c in alphabet}
    can_add_at_end = {c: set[str]() for c in alphabet}

    for word in all_words:
        # if "AA" in word:
        #     pass
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

    for l, can_add in can_add_at_start.items():
        can_add = sorted(list(can_add))
        filename = f"can_add_{l}_at_start.txt"
        filepath = os.path.join("Infix_Data", filename)
        with open(filepath, "w") as file:
            for word in can_add:
                file.write(f"{word}\n")

    for l, can_add in can_add_at_end.items():
        can_add = sorted(list(can_add))
        filename = f"can_add_{l}_at_end.txt"
        filepath = os.path.join("Infix_Data", filename)
        with open(filepath, "w") as file:
            for word in can_add:
                file.write(f"{word}\n")


def main():
    # test_1()
    # test_2()
    # test_3()
    # collect_all_words()
    # test_4()
    make_infix_data()


if __name__ == "__main__":
    main()
