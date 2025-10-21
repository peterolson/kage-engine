import json

from pydantic import BaseModel

from chat import chat_with_retry


with open("semantic_compounds.json", "r", encoding="utf-8") as f:
    semantic_compounds = json.load(f)

print(f"Loaded compounds: {len(semantic_compounds)} entries.")

# remove entries for compounds where meaning is None or "null" or "None" or empty
semantic_compounds = {
    k: v
    for k, v in semantic_compounds.items()
    if v and v not in [None, "null", "None", ""]
}

print(f"Filtered compounds: {len(semantic_compounds)} entries remain.")

# reverse the dictionary to map meanings to lists of compounds
meaning_to_compounds = {}
for compound, meaning in semantic_compounds.items():
    if meaning not in meaning_to_compounds:
        meaning_to_compounds[meaning] = []
    meaning_to_compounds[meaning].append(compound)

print("Mapped meanings to compounds. Found meanings:", len(meaning_to_compounds))


class BestCompound(BaseModel):
    explanation: str
    compound: str


def get_best_compound(meaning: str, compounds: list[str]) -> str:
    if len(compounds) == 1:
        return compounds[0]

    single_char_compounds = [c for c in compounds if len(c) == 1]
    if single_char_compounds:
        return single_char_compounds[0]

    print("Selecting best compound for meaning:", meaning, compounds)

    def explain_compounds(compounds: list[str]) -> str:
        compound_list = []
        for c in compounds:
            if not c.startswith("⿱"):
                continue
            first = c[1]
            second = c[2]
            first_eng = semantic_compounds.get(first, "unknown")
            second_eng = semantic_compounds.get(second, "unknown")
            compound_list.append(
                f"'{c}' ({first}='{first_eng}', {second}='{second_eng}')"
            )

        return "\n".join(compound_list)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant helping with the construction of a conlang that uses Chinese characters as components. "
                "You will be given a meaning and a list of Chinese character compounds that could represent that meaning. "
                "Select the compound that best represents the meaning based on simplicity and clarity. "
                "Order is important: the first character will be treated like an attribute or modifier of the second character.\n"
                "For example, if the first character is 女 (woman) and the second character is 水 (water), the compound ⿱女水 could mean 'milk', i.e. water (liquid) produced by a woman."
                "However, if you go in the reverse order, the compound ⿱水女 could mean 'naiad', i.e. a female spirit associated with water."
                "Another example: ⿱大水 would mean 'big water', which could be a sea or ocean or flood. In the other direction, ⿱水大 would mean 'big in a water-related way', i.e. an adjective characteristic of water, i.e. 'wet', and by extension, ⿱水小 would be 'dry'.\n"
                "So if there are compounds that differ only in the order of their characters, choose the one where the first character logically modifies the second character to produce the desired meaning.\n"
                "A reduplication of a character could indicate plurality or collectiveness, e.g. ⿱人人 could be 'crowd' or ⿱羊羊 could be 'sheep'.\n"
                "Provide a brief explanation for your choice."
            ),
        }
    ]

    messages.append(
        {
            "role": "user",
            "content": (
                f"Meaning: '{meaning}'\n"
                f"Compounds:\n{explain_compounds(compounds)}\n"
                "Select the best compound and explain your choice."
            ),
        }
    )

    result = chat_with_retry(
        messages,
        format=BestCompound,
        validation=lambda inp, resp: (
            None
            if resp.compound in compounds
            else "Selected compound not in provided list"
        ),
        model="medium",
    )
    if not result:
        return compounds[0]
    print(result)
    return result.compound


with open("filtered_semantic_compounds.json", "r", encoding="utf-8") as f:
    best_compounds = json.load(f)

i = 0
for meaning, compounds in meaning_to_compounds.items():
    if meaning in best_compounds.values():
        i += 1
        continue
    best_compound = get_best_compound(meaning, compounds)
    best_compounds[best_compound] = meaning

    i += 1

    print(
        f"({i}/{len(meaning_to_compounds)})\tSelected best compound for meaning '{meaning}': {best_compound}"
    )

    with open("filtered_semantic_compounds.json", "w", encoding="utf-8") as f:
        json.dump(best_compounds, f, ensure_ascii=False, indent=4)
