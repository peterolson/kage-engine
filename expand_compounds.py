import json
from typing_extensions import Literal

from pydantic import BaseModel
from chat import chat_with_retry

with open("semantic_compounds.json", "r", encoding="utf-8") as f:
    semantic_compounds = json.load(f)

single_chars = [k for k in semantic_compounds.keys() if len(k) == 1]

disable_top = {"月", "瓦", "龙", "心"}
disable_bottom = {"气", "厂"}


class Compound(BaseModel):
    meaning: str | None
    explanation: str


class Validation(BaseModel):
    valid: bool
    error_code: (
        Literal["compound_word", "affix", "not-root", "unrelated", "stretch", "other"]
        | None
    )
    error_message: str | None


system_prompt = (
    "You are a helpful assistant that for brainstorming meanings of semantic compounds in a conlang inspired by Chinese characters.\n"
    "You will be given a two charcters and their meanings, and you must suggest a meaning for the compound formed by placing the first character on top of the second character.\n"
    "Order is important: the first character will be treated like an attribute or modifier of the second character.\n"
    "For example, if the first character is 女 (woman) and the second character is 水 (water), the compound ⿱女水 could mean 'milk', i.e. water (liquid) produced by a woman."
    "However, if you go in the reverse order, the compound ⿱水女 could mean 'naiad', i.e. a female spirit associated with water."
    "Another example: ⿱大水 would mean 'big water', which could be a sea or ocean or flood. In the other direction, ⿱水大 would mean 'big in a water-related way', i.e. an adjective characteristic of water, i.e. 'wet', and by extension, ⿱水小 would be 'dry'.\n"
    "A reduplication of a character could indicate plurality or collectiveness, e.g. ⿱人人 could be 'crowd' or ⿱羊羊 could be 'sheep'.\n"
    "Keep in mind that the output must be a single word with a single morpheme. Multi-word phrases (e.g. 'sun god'), compound words (e.g. 'doghouse'), and words with prefixes or suffixes (e.g. 'hunter') are not allowed. Germanic words are generally preferred to Latin words.\n"
    "Not every combination will yield a meaningful compound. If you cannot think of a good meaning that fits the criteria, return None for the meaning with an appropriate explanation.\n"
)


def get_compound_meaning(first: str, second: str) -> Compound | None:
    compound_key = f"⿱{first}{second}"

    examples = [
        (k, semantic_compounds[k])
        for k in semantic_compounds
        if (first in k or second in k) and semantic_compounds[k]
    ]

    messages = [
        {
            "role": "system",
            "content": system_prompt
            + "\n----\nHere are some example compounds and their meanings:\n"
            + "\n".join(f"{k}: {v}" for k, v in examples),
        },
        {"role": "user", "content": "⿱夕日\nFirst: night\nSecond: sun"},
        {
            "role": "assistant",
            "content": Compound(
                meaning="star",
                explanation="A star is a celestial body that shines at night, similar to how the sun shines during the day.",
            ).model_dump_json(),
        },
        {
            "role": "user",
            "content": f"{compound_key}\nFirst: {semantic_compounds[first]}\nSecond: {semantic_compounds[second]}",
        },
    ]

    def validate_response(input: str, response: Compound) -> str | None:
        if not response.meaning or " " in response.meaning or "-" in response.meaning:
            return "Meaning must be a single word."

        examples = [
            (
                "⿱火人\nfire\nman",
                Compound(
                    meaning="fireman",
                    explanation="A fireman is a person who fights fires.",
                ),
                Validation(
                    valid=False,
                    error_code="compound_word",
                    error_message="fireman is a compound word combining 'fire' and 'man'.",
                ),
            ),
            (
                "⿱干人\nhunt\nman",
                Compound(
                    meaning="hunter",
                    explanation="A hunter is a person who hunts animals.",
                ),
                Validation(
                    valid=False,
                    error_code="affix",
                    error_message="hunter contains the suffix '-er', which is an affix.",
                ),
            ),
            (
                "⿱日生\nsun\nlife",
                Compound(
                    meaning="growth",
                    explanation="The sun is essential for the growth and development of all life forms, particularly plants.",
                ),
                Validation(
                    valid=False,
                    error_code="not-root",
                    error_message="The root form of 'growth' is 'grow', so 'growth' is not acceptable.",
                ),
            ),
            (
                "⿱水木\nwater\ntree",
                Compound(
                    meaning="river",
                    explanation="A river is a natural watercourse, typically flowing in a channel to the sea, lake, or another body of water.",
                ),
                Validation(
                    valid=False,
                    error_code="unrelated",
                    error_message="While river is related to 'water', it is not directly related to 'tree'.",
                ),
            ),
            (
                "⿱气人\nair\nman",
                Compound(
                    meaning="pilot",
                    explanation="A pilot is a person who flies airplanes.",
                ),
                Validation(valid=True, error_code=None, error_message=None),
            ),
            (
                "⿱手气\nhand\nair",
                Compound(
                    meaning="puff",
                    explanation="The compound could refer to a small burst of air, such as one created by a hand movement (e.g., fanning or clapping).",
                ),
                Validation(
                    valid=False,
                    error_code="stretch",
                    error_message="The connection between 'hand' and 'air' to mean 'puff' is too loose and requires too much guesswork to be considered valid.",
                ),
            ),
            (
                "⿱卜犬\ncrack\ndog",
                Compound(
                    meaning="mad",
                    explanation="The character 卜 (crack) can refer to a mental break or instability. When applied to a dog, a 'crack-dog' could mean a dog that is mentally unsound or rabid, hence 'mad'.",
                ),
                Validation(
                    valid=False,
                    error_code="stretch",
                    error_message="'mad' is not an immediately obvious meaning derived from 'crack' and 'dog'; it requires significant interpretation.",
                ),
            ),
        ]

        validation_messages = [
            {
                "role": "system",
                "content": system_prompt
                + "\n----\nYou are an evaluator determining whether the proposed meaning for a semantic compound is valid.\n"
                "If the meaning is not immediately obvious from the meanings of the component characters without reading the explanation, it is considered invalid.\n"
                "You must return 'VALID' if the proposed meaning is acceptable, or explain why it is not acceptable.\n"
                "Possible reasons for invalidity include:\n"
                "- The meaning is a multi-word phrase (e.g. 'sun god').\n"
                "- The meaning is a compound word (e.g. 'doghouse').\n"
                "- The meaning contains prefixes or suffixes (e.g. 'hunter').\n"
                "- The meaning is not a single morpheme.\n"
                "- The meaning is not the root form of the word (e.g. 'growth' instead of 'grow').\n"
                "- The meaning is unrelated to the meanings of the component characters.\n"
                "- The meaning is a stretch and requires too much interpretation, i.e. the relationship between the component characters and the meaning is not obvious.\n",
            }
        ]

        for example_input, example_response, example_validation in examples:
            validation_messages.append(
                {
                    "role": "user",
                    "content": example_input
                    + "\n"
                    + example_response.model_dump_json(),
                }
            )
            validation_messages.append(
                {
                    "role": "assistant",
                    "content": example_validation.model_dump_json(),
                }
            )

        validation_messages.append(
            {
                "role": "user",
                "content": input + "\n" + response.model_dump_json(),
            }
        )

        def validation_validation(
            original_input: str, parsed_response: Validation
        ) -> str | None:
            if not parsed_response.valid and (
                not parsed_response.error_code or not parsed_response.error_message
            ):
                return "If the response is invalid, both error_code and error_message must be provided."
            return None  # No further validation needed for the validation step

        validation_response = chat_with_retry(
            validation_messages,
            format=Validation,
            model="medium",
            validation=validation_validation,
        )
        if not validation_response:
            return None
        if (
            not validation_response.valid
            and validation_response.error_code
            and validation_response.error_message
        ):
            return (
                validation_response.error_code
                + ": "
                + validation_response.error_message
            )
        return None

    try:
        reponse = chat_with_retry(
            messages, format=Compound, model="medium", validation=validate_response
        )
        if reponse and reponse.meaning == "None":
            return None
        return reponse
    except Exception as e:
        print(f"Error occurred while generating compound meaning: {e}")
        return None


if __name__ == "__main__":
    for first_char in single_chars:
        if first_char in disable_top:
            continue
        for second_char in single_chars:
            if second_char in disable_bottom:
                continue
            compound_key = f"⿱{first_char}{second_char}"
            if compound_key in semantic_compounds:
                continue  # Skip if we already have a meaning for this compound
            print(f"Generating meaning for {compound_key}...")
            compound = get_compound_meaning(first_char, second_char)
            print(compound)

            semantic_compounds[compound_key] = compound.meaning if compound else None

            with open("semantic_compounds.json", "w", encoding="utf-8") as f:
                json.dump(semantic_compounds, f, ensure_ascii=False, indent=4)
