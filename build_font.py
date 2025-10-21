import json
from kage import Kage
from kage.font.sans import Sans
from kage.font.serif import Serif
import csv
import os
import subprocess


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


with open("filtered_semantic_compounds.json", "r", encoding="utf-8") as f:
    filtered_compounds = json.load(f)


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

semantic_chars = "日月夕金水木火土气云风天雨申川山石厂瓦田乇马牛羊豕犬鱼隹鸟虫龙已虍口目耳自手止面首心肉彡毛爪羽牙舌革贝囟角人女子儿父母王士示生大小古疒丑甘白丰禾米来酉卤食皿豆上下中又正非刀勺叉工力弓矢车舟丁门方斗斤戈攵网卜聿辛井臼糸巾衣包冃立丮干回化巴八"

disable_top = {"月", "瓦", "龙", "心"}
disable_bottom = {"气", "厂", "疒", "门"}

special_tops = {
    "气": lambda bottom: f"99:0:0:0:0:200:200:u6c14-10:0:0:0$99:0:0:15:70:150:200:{bottom}:0:0:0",
    "风": lambda bottom: f"99:0:0:0:0:200:200:u20628:0:0:0$99:0:0:40:30:150:175:{bottom}:0:0:0",
    "厂": lambda bottom: f"99:0:0:0:0:200:200:u5382:0:0:0$99:0:0:50:40:175:180:{bottom}:0:0:0",
    "雨": lambda bottom: f"99:0:0:0:0:200:180:u96e8-03:0:0:0$99:0:0:0:80:200:200:{bottom}:0:0:0",
    "门": lambda bottom: f"99:0:0:0:0:200:200:u95e8:0:0:0$99:0:0:40:40:160:170:{bottom}:0:0:0",
    "疒": lambda bottom: f"99:0:0:0:0:200:200:u7592:0:0:0$99:0:0:55:40:180:180:{bottom}:0:0:0",
}

print("Adding synthetic components...")
semantic_char_count = 0
for first_char in semantic_chars:
    if first_char in disable_top:
        continue
    for second_char in semantic_chars:
        if second_char in disable_bottom:
            continue
        compound = "⿱" + first_char + second_char
        if compound not in filtered_compounds:
            continue
        first_key = f"u{ord(first_char):x}"
        second_key = f"u{ord(second_char):x}"
        key = f"h{first_key}_{second_key}"
        data = f"99:0:0:25:0:180:100:{first_key}:0:0:0$99:0:0:0:90:200:200:{second_key}:0:0:0"
        if first_char in special_tops:
            data = special_tops[first_char](second_key)
        k.components.push(key, data)
        semantic_char_count += 1

print("Synthetic components added.")

if __name__ == "__main__":
    # clear output folder
    if not os.path.exists("./output"):
        os.makedirs("./output")
    else:
        for f in os.listdir("./output"):
            os.remove(os.path.join("./output", f))
    print("Generating glyphs...")
    for char in semantic_chars:
        gen(char, f"u{ord(char):x}")

    i = 0
    for first_char in semantic_chars:
        if first_char in disable_top:
            continue
        for second_char in semantic_chars:
            if second_char in disable_bottom:
                continue
            compound = "⿱" + first_char + second_char
            if compound not in filtered_compounds:
                continue
            i += 1
            if i % 50 == 0:
                print(f"Generating compound {i} of {semantic_char_count}...")
            first_key = f"u{ord(first_char):x}"
            second_key = f"u{ord(second_char):x}"
            key = f"h{first_key}_{second_key}"
            gen(compound, key)

    print("All glyphs generated.")

    print("Generating sprite.svg...")

    try:
        result = subprocess.run(
            ["svgsprite", "--src", "output", "--dest", "sprite.svg"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("sprite.svg generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running svgsprite: {e}")
    except FileNotFoundError:
        print("svgsprite command not found!")
