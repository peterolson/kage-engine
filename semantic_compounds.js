const groups = [
    {
        group: "Nature",
        chars: [
            { char: "日", eng: "sun" },
            { char: "月", eng: "moon", disableTop: true },
            { char: "夕", eng: "night" },
            { char: "金", eng: "gold" },
            { char: "水", eng: "water" },
            { char: "木", eng: "wood" },
            { char: "火", eng: "fire" },
            { char: "土", eng: "earth" },
            { char: "气", eng: "air", disableBottom: true },
            { char: "云", eng: "cloud" },
            { char: "风", eng: "wind" },
            { char: "天", eng: "sky" },
            { char: "雨", eng: "rain" },
            { char: "申", eng: "thunder" },
            { char: "川", eng: "river" },
            { char: "山", eng: "mountain" },
            { char: "石", eng: "rock" },
            { char: "厂", eng: "cliff", disableBottom: true },
            { char: "瓦", eng: "clay", disableTop: true },
            { char: "田", eng: "field" },
            { char: "乇", eng: "grass" },
        ],
    },
    {
        group: "Animals",
        chars: [
            { char: "马", eng: "horse" },
            { char: "牛", eng: "ox" },
            { char: "羊", eng: "sheep" },
            { char: "豕", eng: "pig" },
            { char: "犬", eng: "dog" },
            { char: "鱼", eng: "fish" },
            { char: "隹", eng: "bird" },
            { char: "鸟", eng: "fowl" },
            { char: "虫", eng: "bug" },
            { char: "龙", eng: "dragon", disableTop: true },
            { char: "已", eng: "snake" },
            { char: "虍", eng: "tiger" },
        ],
    },
    {
        group: "Body",
        chars: [
            { char: "口", eng: "mouth" },
            { char: "目", eng: "eye" },
            { char: "耳", eng: "ear" },
            { char: "自", eng: "nose" },
            { char: "手", eng: "hand" },
            { char: "止", eng: "foot" },
            { char: "面", eng: "face" },
            { char: "首", eng: "head" },
            { char: "心", eng: "heart", disableTop: true },
            { char: "肉", eng: "flesh" },
            { char: "彡", eng: "hair" },
            { char: "毛", eng: "fur" },
            { char: "爪", eng: "claw" },
            { char: "羽", eng: "feather" },
            { char: "牙", eng: "tooth" },
            { char: "舌", eng: "tongue" },
            { char: "革", eng: "skin" },
            { char: "贝", eng: "shell" },
            { char: "囟", eng: "skull" },
            { char: "角", eng: "horn" },
        ],
    },
    {
        group: "People",
        chars: [
            { char: "人", eng: "man" },
            { char: "女", eng: "woman" },
            { char: "子", eng: "son" },
            { char: "儿", eng: "daughter" },
            { char: "父", eng: "father" },
            { char: "母", eng: "mother" },
            { char: "王", eng: "king" },
            { char: "士", eng: "sage" },
            { char: "示", eng: "spirit" },
            { char: "生", eng: "life" },
        ],
    },
    {
        group: "Adjectives",
        chars: [
            { char: "大", eng: "big" },
            { char: "小", eng: "small" },
            { char: "古", eng: "old" },
            { char: "疒", eng: "sick", disableBottom: true },
            { char: "丑", eng: "ugly" },
            { char: "甘", eng: "sweet" },
            { char: "白", eng: "white" },
            { char: "丰", eng: "lush" },
        ],
    },
    {
        group: "Food",
        chars: [
            { char: "禾", eng: "corn" },
            { char: "米", eng: "rice" },
            { char: "来", eng: "wheat" },
            { char: "酉", eng: "wine" },
            { char: "卤", eng: "salt" },
            { char: "食", eng: "eat" },
            { char: "皿", eng: "dish" },
            { char: "豆", eng: "bean" },
        ],
    },
    {
        group: "Ideographs",
        chars: [
            { char: "上", eng: "up" },
            { char: "下", eng: "down" },
            { char: "中", eng: "mid" },
            { char: "又", eng: "right" },
            { char: "正", eng: "straight" },
            { char: "非", eng: "not" },
        ],
    },
    {
        group: "Tools",
        chars: [
            { char: "刀", eng: "knife" },
            { char: "勺", eng: "spoon" },
            { char: "叉", eng: "fork" },
            { char: "工", eng: "work" },
            { char: "力", eng: "plow" },
            { char: "弓", eng: "bow" },
            { char: "矢", eng: "arrow" },
            { char: "车", eng: "car" },
            { char: "舟", eng: "boat" },
            { char: "丁", eng: "nail" },
            { char: "门", eng: "door", disableBottom: true },
            { char: "方", eng: "square" },
            { char: "斗", eng: "ladle" },
            { char: "斤", eng: "axe" },
            { char: "戈", eng: "spear" },
            { char: "攵", eng: "tap" },
            { char: "网", eng: "net" },
            { char: "卜", eng: "crack" },
            { char: "聿", eng: "brush" },
            { char: "辛", eng: "chisel" },
            { char: "井", eng: "well" },
            { char: "臼", eng: "mortar" },
            { char: "市", eng: "market" },
        ],
    },
    {
        group: "Textile",
        chars: [
            { char: "糸", eng: "silk" },
            { char: "巾", eng: "cloth" },
            { char: "衣", eng: "shirt" },
            { char: "包", eng: "wrap" },
            { char: "冃", eng: "hat" },
        ],
    },
    {
        group: "Actions",
        chars: [
            { char: "立", eng: "stand" },
            { char: "丮", eng: "catch" },
            { char: "干", eng: "hunt" },
            { char: "回", eng: "turn" },
            { char: "化", eng: "change" },
            { char: "巴", eng: "grab" },
            { char: "八", eng: "split" },
        ],
    },
];

const flatChars = [];
let groupCounter = 0;
for (const group of groups) {
    const { group: groupName, chars } = group;
    groupCounter++;
    for (const charObj of chars) {
        flatChars.push({
            ...charObj,
            group: groupName,
            groupIndex: groupCounter,
        });
    }
}

console.log("Flat chars:", flatChars, flatChars.map((c) => c.char).join(""));

function svgChar(char) {
    const id = char;
    return `<svg baseProfile="full" viewBox="0 0 200 200" width="48" height="48">
                <use href="sprite.svg?14#${id}" xlink:href="sprite.svg#${id}"/>
            </svg>`;
}

function initTable(compounds) {
    const table = document.getElementById("compound-table");
    const thead = table.querySelector("thead");
    const tbody = table.querySelector("tbody");

    // Create table header
    const groupHeaderRow = document.createElement("tr");
    groupHeaderRow.appendChild(document.createElement("th")); // Top-left empty cell
    for (const group of groups) {
        const { group: groupName, chars } = group;
        const headerCell = document.createElement("th");
        headerCell.textContent = groupName;
        headerCell.colSpan = chars.length;
        groupHeaderRow.appendChild(headerCell);
    }

    thead.appendChild(groupHeaderRow);

    const charHeaderRow = document.createElement("tr");
    charHeaderRow.appendChild(document.createElement("th")); // Top-left empty cell
    for (const charObj of flatChars) {
        if (charObj.disableBottom) {
            continue; // Skip characters that cannot be on bottom
        }
        const headerCell = document.createElement("th");
        const id = charObj.char;
        headerCell.innerHTML =
            svgChar(id) + `<br><small>${charObj.eng}</small>`;
        charHeaderRow.appendChild(headerCell);
    }
    thead.appendChild(charHeaderRow);

    // Create table body
    for (const rowChar of flatChars) {
        if (rowChar.disableTop) {
            continue; // Skip characters that cannot be on top
        }
        const row = document.createElement("tr");
        const header = document.createElement("th");
        header.innerHTML =
            svgChar(rowChar.char) + `<br><small>${rowChar.eng}</small>`;
        row.appendChild(header);
        for (const colChar of flatChars) {
            if (colChar.disableBottom) {
                continue; // Skip characters that cannot be on bottom
            }
            const cell = document.createElement("td");
            const compoundChar = "⿱" + rowChar.char + colChar.char;
            if (
                rowChar.disableTop ||
                colChar.disableBottom ||
                !(compoundChar in compounds)
            ) {
                cell.innerHTML = "";
                cell.classList.add("disabled");
            } else {
                const id = compoundChar;
                cell.innerHTML =
                    svgChar(id) +
                    `<br><small>${compounds[compoundChar]}</small>`;
            }
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
}

fetch("filtered_semantic_compounds.json")
    .then((response) => response.json())
    .then((data) => {
        initTable(data);
    })
    .catch((error) =>
        console.error("Error fetching filtered compounds:", error)
    );
