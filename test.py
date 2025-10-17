from kage import Kage
from kage.font.sans import Sans
from kage.font.serif import Serif
import csv
import os

# Set the flag `ignore_component_version` if you want to use the glyph data in `dump_newest_only.txt`.
# This is because `dump_newest_only.txt` only contains the latest version of components.
# However, glyphs in `dump_newest_only.txt` may reference older versions of multiple components.
k = Kage(ignore_component_version=True)
# You can use `Serif()` as well!
k.font = Serif()


# generate a glyph
def gen(char: str, key: str):
    canvas = k.make_glyph(name=key)
    canvas.saveas(os.path.join("./output", f"{char}.svg"))


print("Loading components...")

# read the glyph data
with open("dump/dump_newest_only.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

lines = csv.reader(lines, delimiter="|")
for i, line in enumerate(lines):
    if i <= 1 or len(line) < 3:
        continue
    line = [i.strip() for i in line]

    k.components.push(line[0], line[2])

print("Components loaded.")

semantic_chars = "日月夕金水木火土气云风天雨申川山石厂瓦田马牛羊豕犬鱼隹鸟虫象龟鹿鼠兔龙口目耳自手止面首心肉冎彡爪羽齿舌"

print("Adding synthetic components...")

for first_char in semantic_chars:
    for second_char in semantic_chars:
        first_key = f"u{ord(first_char):x}"
        second_key = f"u{ord(second_char):x}"
        key = f"h{first_key}_{second_key}"
        data = f"99:0:0:25:0:180:100:{first_key}:0:0:0$99:0:0:0:90:200:200:{second_key}:0:0:0"
        k.components.push(key, data)

print("Synthetic components added.")

# parallel generation
if __name__ == "__main__":
    for char in semantic_chars:
        gen(char, f"u{ord(char):x}")

    i = 0
    for first_char in semantic_chars:
        for second_char in semantic_chars:
            i += 1
            if i % 50 == 0:
                print(f"Generating compound {i} of {len(semantic_chars) ** 2}...")
            first_key = f"u{ord(first_char):x}"
            second_key = f"u{ord(second_char):x}"
            key = f"h{first_key}_{second_key}"
            gen("⿱" + first_char + second_char, key)

    print("All glyphs generated.")

    print("Run the following command to generate sprite.svg:")
    print("svgsprite --src output --dest sprite.svg")
