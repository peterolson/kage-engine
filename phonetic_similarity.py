import json
import Levenshtein


word_phones = {}

with open("word_morph_phones.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            word = parts[0]
            morph_phones = parts[2]
            phones = []
            for mp in morph_phones.split("|"):
                phones.extend(mp.split())
            word_phones[word] = phones

print(f"Loaded phonetic data for {len(word_phones)} words.")


def strip_stress(phones: list[str]) -> list[str]:
    return [p for p in phones if "*" not in p]


def strip_pre_stress(phones: list[str]) -> list[str]:
    # get all symbols after the * indicating primary stress
    for i, phone in enumerate(phones):
        if phone.endswith("*"):
            return strip_stress(phones[i + 1 :])
    return strip_stress(phones)


def exact_match(phones1: list[str], phones2: list[str]) -> bool:
    return strip_stress(phones1) == strip_stress(phones2)


def exact_rhyme(phones1: list[str], phones2: list[str]) -> bool:
    return strip_pre_stress(phones1) == strip_pre_stress(phones2)


vowel_map = {
    "a": "æ",
    "A1": "æ",
    "A5": "ə",
    "aa": "ä",
    "AA": "ə",
    "ei": "ei",
    "EI": "ə",
    "ee": "ei",
    "EE": "ə",
    "EE1": "ei",
    "EE5": "ei",
    "ah": "æ",
    "ah2": "æ",
    "AH1": "æ",
    "aa": "ä",
    "oa": "æ",
    "A": "æ",
    "e": "ɛ",
    "E": "ɛ",
    "E1": "ɛ",
    "E5": "ɛ",
    "E05": "ɛ",
    "E50": "ə",
    "ii": "i",
    "ii2": "i",
    "II1": "i",
    "I2": "ɪ",
    "I5": "ɪ",
    "I6": "ɪ",
    "I7": "ɪ",
    "i": "ɪ",
    "I1": "ɪ",
    "ai": "ai",
    "AI": "ai",
    "iy": "i",
    "i@": "ə",
    "ae": "ai",
    "AE": "ai",
    "I": "ɪ",
    "II": "i",
    "o": "ä",
    "oo": "ä",
    "OO": "ə",
    "OO1": "ə",
    "ou": "ou",
    "ouw": "ou",
    "oou": "ou",
    "au": "ä",
    "O": "ä",
    "O1": "ä",
    "O4": "ə",
    "O5": "ə",
    "OU": "ou",
    "OU1": "ou",
    "ow": "au",
    "oow": "au",
    "oi": "oi",
    "uh": "ə",
    "UH": "ə",
    "UH1": "ə",
    "UH4": "ə",
    "u": "ʊ",
    "uu": "u",
    "UU": "u",
    "UU1": "u",
    "@": "ə",
    "iu": "u",
    "IU": "u",
    "iu3": "u",
    "U": "ə",
    "ir": "r",
    "IR": "r",
    "er": "r",
    "ER": "r",
    "eir": "r",
    "EIR": "r",
    "EIR1": "r",
    "aer": "r",
    "AER": "r",
    "AER1": "r",
    "ar": "r",
    "AR": "r",
    "AR1": "r",
    "or": "r",
    "OR": "r",
    "OR1": "r",
    "our": "r",
    "OUR1": "r",
    "ur": "r",
    "UR": "r",
    "@r": "r",
    "@@r": "r",
    "@@R1": "r",
    "@@r2": "r",
    "@@r3": "r",
    "owr": "r",
    "oir": "r",
}

fuzzy_vowel_map = {
    "ä": "a",
    "æ": "a",
    "ɛ": "e",
    "ei": "e",
    "ai": "i",
    "ɪ": "i",
    "i": "i",
    "ou": "o",
    "ʊ": "u",
    "ə": "u",
    "u": "u",
    "oi": "O",
    "au": "A",
    "r": "r",
}

# print distinct vowels in the dataset
distinct_vowels = set(list(vowel_map.values()))


def project_phone(phone: str):
    if phone in ["t", "d"]:
        return "T"
    if phone in ["th", "dh"]:
        return "D"
    if phone in ["ch", "jh"]:
        return "C"
    if phone in ["n", "ng"]:
        return "N"
    if phone in ["f", "v"]:
        return "F"
    if phone in ["w", "hw"]:
        return "W"
    if phone in ["s", "z", "sh", "zh"]:
        return "S"
    if phone in ["l", "ll", "y", "r"]:
        return "L"
    if phone in ["h", "x"]:
        return "H"
    if phone in ["p", "b"]:
        return "P"
    if phone in ["k", "g"]:
        return "K"
    if phone in vowel_map:
        return fuzzy_vowel_map[vowel_map[phone]]
    return phone


def is_fuzzy_match(phones1: list[str], phones2: list[str]) -> bool:
    projected1 = [project_phone(p) for p in strip_stress(phones1)]
    projected2 = [project_phone(p) for p in strip_stress(phones2)]
    return projected1 == projected2


def is_fuzzy_rhyme(phones1: list[str], phones2: list[str]) -> bool:
    projected1 = [project_phone(p) for p in strip_pre_stress(phones1)]
    projected2 = [project_phone(p) for p in strip_pre_stress(phones2)]
    return projected1 == projected2


def levenstein_distance(phones1: list[str], phones2: list[str]) -> int:
    projected1 = strip_stress(phones1)
    projected2 = strip_stress(phones2)
    str1 = " ".join(projected1)
    str2 = " ".join(projected2)
    return Levenshtein.distance(str1, str2)


def get_difference(phones1: list[str], phones2: list[str]) -> float:
    if exact_match(phones1, phones2):
        return 0
    if exact_rhyme(phones1, phones2):
        return 1 + (levenstein_distance(phones1, phones2) / 10)
    if is_fuzzy_match(phones1, phones2):
        return 2 + (levenstein_distance(phones1, phones2) / 10)
    if is_fuzzy_rhyme(phones1, phones2):
        return 3 + (levenstein_distance(phones1, phones2) / 10)
    first_phone_match = is_fuzzy_match([phones1[0]], [phones2[0]])
    return 4 + levenstein_distance(phones1, phones2) - (1 if first_phone_match else 0)


def get_best_phonetic_components(
    target_word: str | list[str],
) -> list[tuple[float, str, str]]:
    with open("dictionary.json", "r", encoding="utf-8") as f:
        dictionary = json.load(f)
        dictionary_words = set(dictionary.keys())
        filtered_words = {
            word: (word_phones[word], dictionary[word])
            for word in dictionary_words
            if word in word_phones
            and not dictionary[word].startswith("⿰")
            and not " " in dictionary[word]
            and len(dictionary[word]) <= 6
        }

    candidate_words = filtered_words.keys()
    target_phones = (
        word_phones[target_word] if isinstance(target_word, str) else target_word
    )
    scores = []
    for candidate in candidate_words:
        if candidate == target_word:
            continue
        candidate_phones, glyph = filtered_words[candidate]
        difference = get_difference(target_phones, candidate_phones)
        scores.append((difference, candidate, glyph))

    scores.sort(key=lambda x: x[0])
    min_score = scores[0][0]
    best_matches = [s for s in scores if s[0] <= min_score + 0.5]
    return best_matches


print(get_best_phonetic_components(["E05", "s", "t"]))
