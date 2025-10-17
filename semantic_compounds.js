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
            { char: "厂", eng: "cliff" },
            { char: "瓦", eng: "clay", disableTop: true },
            { char: "田", eng: "field" },
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
            { char: "象", eng: "elephant", disableTop: true },
            { char: "龟", eng: "turtle", disableTop: true },
            { char: "鹿", eng: "deer", disableTop: true },
            { char: "鼠", eng: "rat", disableTop: true },
            { char: "兔", eng: "rabbit", disableTop: true },
            { char: "龙", eng: "dragon", disableTop: true },
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
            { char: "冎", eng: "bone" },
            { char: "彡", eng: "hair" },
            { char: "爪", eng: "claw" },
            { char: "羽", eng: "feather" },
            { char: "齿", eng: "tooth" },
            { char: "舌", eng: "tongue" },
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

console.log("Flat chars:", flatChars);

function svgChar(char) {
    const id = char;
    return `<svg baseProfile="full" viewBox="0 0 200 200" width="48" height="48">
                <use href="sprite.svg?1#${id}" xlink:href="sprite.svg#${id}"/>
            </svg>`;
}

function initTable() {
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
            if (rowChar.disableTop || colChar.disableBottom) {
                cell.innerHTML = "";
                cell.classList.add("disabled");
            } else {
                const id = compoundChar;
                cell.innerHTML = svgChar(id);
            }
            row.appendChild(cell);
        }
        tbody.appendChild(row);
    }
}

initTable();
