"""
Список названий всех стран мира.
"""


class Country():
    """
    Список названий всех старн мира на русском языке
    """

    ...


COUNTRIES_DICT: dict[str, dict[str, int | str]] = {
    "AFGHANISTAN": {
        "id": 1,
        "title_eng": "Afghanistan",
        "title_rus": "Афганистан",
        "code": "AFG"
    },
    "ALBANIA": {
        "id": 2,
        "title_eng": "Albania",
        "title_rus": "Албания",
        "code": "ALB"
    },
    "ALGERIA": {
        "id": 3,
        "title_eng": "Algeria",
        "title_rus": "Алжир",
        "code": "DZA"
    },
    "ANDORRA": {
        "id": 4,
        "title_eng": "Andorra",
        "title_rus": "Андорра",
        "code": "AND"
    },
    "ANGOLA": {
        "id": 5,
        "title_eng": "Angola",
        "title_rus": "Ангола",
        "code": "AGO"
    },
    "ANTIGUA AND BARBUDA": {
        "id": 6,
        "title_eng": "Antigua and Barbuda",
        "title_rus": "Антигуа и Барбуда",
        "code": "ATG"
    },
    "ARGENTINA": {
        "id": 7,
        "title_eng": "Argentina",
        "title_rus": "Аргентина",
        "code": "ARG"
    },
    "ARMENIA": {
        "id": 8,
        "title_eng": "Armenia",
        "title_rus": "Армения",
        "code": "ARM"
    },
    "AUSTRALIA": {
        "id": 9,
        "title_eng": "Australia",
        "title_rus": "Австралия",
        "code": "AUS"
    },
    "AUSTRIA": {
        "id": 10,
        "title_eng": "Austria",
        "title_rus": "Австрия",
        "code": "AUT"
    },
    "AZERBAIJAN": {
        "id": 11,
        "title_eng": "Azerbaijan",
        "title_rus": "Азербайджан",
        "code": "AZE"
    },
    "THE BAHAMAS": {
        "id": 12,
        "title_eng": "The Bahamas",
        "title_rus": "Багамские Острова",
        "code": "BHS"
    },
    "BAHRAIN": {
        "id": 13,
        "title_eng": "Bahrain",
        "title_rus": "Бахрейн",
        "code": "BHR"
    },
    "BANGLADESH": {
        "id": 14,
        "title_eng": "Bangladesh",
        "title_rus": "Бангладеш",
        "code": "BGD"
    },
    "BARBADOS": {
        "id": 15,
        "title_eng": "Barbados",
        "title_rus": "Барбадос",
        "code": "BRB"
    },
    "BELARUS": {
        "id": 16,
        "title_eng": "Belarus",
        "title_rus": "Беларусь",
        "code": "BLR"
    },
    "BELGIUM": {
        "id": 17,
        "title_eng": "Belgium",
        "title_rus": "Бельгия",
        "code": "BEL"
    },
    "BELIZE": {
        "id": 18,
        "title_eng": "Belize",
        "title_rus": "Белиз",
        "code": "BLZ"
    },
    "BENIN": {
        "id": 19,
        "title_eng": "Benin",
        "title_rus": "Бенин",
        "code": "BEN"
    },
    "BHUTAN": {
        "id": 20,
        "title_eng": "Bhutan",
        "title_rus": "Бутан",
        "code": "BTN"
    },
    "BOLIVIA": {
        "id": 21,
        "title_eng": "Bolivia",
        "title_rus": "Боливия",
        "code": "BOL"
    },
    "BOSNIA AND HERZEGOVINA": {
        "id": 22,
        "title_eng": "Bosnia and Herzegovina",
        "title_rus": "Босния и Герцеговина",
        "code": "BIH"
    },
    "BOTSWANA": {
        "id": 23,
        "title_eng": "Botswana",
        "title_rus": "Ботсвана",
        "code": "BWA"
    },
    "BRAZIL": {
        "id": 24,
        "title_eng": "Brazil",
        "title_rus": "Бразилия",
        "code": "BRA"
    },
    "BRUNEI": {
        "id": 25,
        "title_eng": "Brunei",
        "title_rus": "Бруней",
        "code": "BRN"
    },
    "BULGARIA": {
        "id": 26,
        "title_eng": "Bulgaria",
        "title_rus": "Болгария",
        "code": "BGR"
    },
    "BURKINA FASO": {
        "id": 27,
        "title_eng": "Burkina Faso",
        "title_rus": "Буркина-Фасо",
        "code": "BFA"
    },
    "BURUNDI": {
        "id": 28,
        "title_eng": "Burundi",
        "title_rus": "Бурунди",
        "code": "BDI"
    },
    "CABO VERDE": {
        "id": 29,
        "title_eng": "Cabo Verde",
        "title_rus": "Кабо-Верде",
        "code": "CPV"
    },
    "CAMBODIA": {
        "id": 30,
        "title_eng": "Cambodia",
        "title_rus": "Камбоджа",
        "code": "KHM"
    },
    "CAMEROON": {
        "id": 31,
        "title_eng": "Cameroon",
        "title_rus": "Камерун",
        "code": "CMR"
    },
    "CANADA": {
        "id": 32,
        "title_eng": "Canada",
        "title_rus": "Канада",
        "code": "CAN"
    },
    "CENTRAL AFRICAN REPUBLIC": {
        "id": 33,
        "title_eng": "Central African Republic",
        "title_rus": "Центральноафриканская Республика",
        "code": "CAF"
    },
    "CHAD": {
        "id": 34,
        "title_eng": "Chad",
        "title_rus": "Чад",
        "code": "TCD"
    },
    "CHILE": {
        "id": 35,
        "title_eng": "Chile",
        "title_rus": "Чили",
        "code": "CHL"
    },
    "CHINA": {
        "id": 36,
        "title_eng": "China",
        "title_rus": "Китай",
        "code": "CHN"
    },
    "COLOMBIA": {
        "id": 37,
        "title_eng": "Colombia",
        "title_rus": "Колумбия",
        "code": "COL"
    },
    "COMOROS": {
        "id": 38,
        "title_eng": "Comoros",
        "title_rus": "Коморские Острова",
        "code": "COM"
    },
    "CONGO, DEMOCRATIC REPUBLIC OF THE": {
        "id": 39,
        "title_eng": "Congo, Democratic Republic of the",
        "title_rus": "Конго, Демократическая Республика",
        "code": "COD"
    },
    "CONGO, REPUBLIC OF THE": {
        "id": 40,
        "title_eng": "Congo, Republic of the",
        "title_rus": "Конго, Республика",
        "code": "COG"
    },
    "COSTA RICA": {
        "id": 41,
        "title_eng": "Costa Rica",
        "title_rus": "Коста-Рика",
        "code": "CRI"
    },
    "CÔTE D’IVOIRE": {
        "id": 42,
        "title_eng": "Côte d’Ivoire",
        "title_rus": "Кот-д’Ивуар",
        "code": "CIV"
    },
    "CROATIA": {
        "id": 43,
        "title_eng": "Croatia",
        "title_rus": "Хорватия",
        "code": "HRV"
    },
    "CUBA": {
        "id": 44,
        "title_eng": "Cuba",
        "title_rus": "Куба",
        "code": "CUB"
    },
    "CYPRUS": {
        "id": 45,
        "title_eng": "Cyprus",
        "title_rus": "Кипр",
        "code": "CYP"
    },
    "CZECH REPUBLIC": {
        "id": 46,
        "title_eng": "Czech Republic",
        "title_rus": "Чехия",
        "code": "CZE"
    },
    "DENMARK": {
        "id": 47,
        "title_eng": "Denmark",
        "title_rus": "Дания",
        "code": "DNK"
    },
    "DJIBOUTI": {
        "id": 48,
        "title_eng": "Djibouti",
        "title_rus": "Джибути",
        "code": "DJI"
    },
    "DOMINICA": {
        "id": 49,
        "title_eng": "Dominica",
        "title_rus": "Доминика",
        "code": "DMA"
    },
    "DOMINICAN REPUBLIC": {
        "id": 50,
        "title_eng": "Dominican Republic",
        "title_rus": "Доминиканская Республика",
        "code": "DOM"
    },
    "EAST TIMOR (TIMOR-LESTE)": {
        "id": 51,
        "title_eng": "East Timor (Timor-Leste)",
        "title_rus": "Восточный Тимор (Тимор-Лесте)",
        "code": "TLS"
    },
    "ECUADOR": {
        "id": 52,
        "title_eng": "Ecuador",
        "title_rus": "Эквадор",
        "code": "ECU"
    },
    "EGYPT": {
        "id": 53,
        "title_eng": "Egypt",
        "title_rus": "Египет",
        "code": "EGY"
    },
    "EL SALVADOR": {
        "id": 54,
        "title_eng": "El Salvador",
        "title_rus": "Сальвадор",
        "code": "SLV"
    },
    "EQUATORIAL GUINEA": {
        "id": 55,
        "title_eng": "Equatorial Guinea",
        "title_rus": "Экваториальная Гвинея",
        "code": "GNQ"
    },
    "ERITREA": {
        "id": 56,
        "title_eng": "Eritrea",
        "title_rus": "Эритрея",
        "code": "ERI"
    },
    "ESTONIA": {
        "id": 57,
        "title_eng": "Estonia",
        "title_rus": "Эстония",
        "code": "EST"
    },
    "ESWATINI": {
        "id": 58,
        "title_eng": "Eswatini",
        "title_rus": "Эсватини",
        "code": "SWZ"
    },
    "ETHIOPIA": {
        "id": 59,
        "title_eng": "Ethiopia",
        "title_rus": "Эфиопия",
        "code": "ETH"
    },
    "FIJI": {
        "id": 60,
        "title_eng": "Fiji",
        "title_rus": "Фиджи",
        "code": "FJI"
    },
    "FINLAND": {
        "id": 61,
        "title_eng": "Finland",
        "title_rus": "Финляндия",
        "code": "FIN"
    },
    "FRANCE": {
        "id": 62,
        "title_eng": "France",
        "title_rus": "Франция",
        "code": "FRA"
    },
    "GABON": {
        "id": 63,
        "title_eng": "Gabon",
        "title_rus": "Габон",
        "code": "GAB"
    },
    "THE GAMBIA": {
        "id": 64,
        "title_eng": "The Gambia",
        "title_rus": "Гамбия",
        "code": "GMB"
    },
    "GEORGIA": {
        "id": 65,
        "title_eng": "Georgia",
        "title_rus": "Грузия",
        "code": "GEO"
    },
    "GERMANY": {
        "id": 66,
        "title_eng": "Germany",
        "title_rus": "Германия",
        "code": "DEU"
    },
    "GHANA": {
        "id": 67,
        "title_eng": "Ghana",
        "title_rus": "Гана",
        "code": "GHA"
    },
    "GREECE": {
        "id": 68,
        "title_eng": "Greece",
        "title_rus": "Греция",
        "code": "GRC"
    },
    "GRENADA": {
        "id": 69,
        "title_eng": "Grenada",
        "title_rus": "Гренада",
        "code": "GRD"
    },
    "GUATEMALA": {
        "id": 70,
        "title_eng": "Guatemala",
        "title_rus": "Гватемала",
        "code": "GTM"
    },
    "GUINEA": {
        "id": 71,
        "title_eng": "Guinea",
        "title_rus": "Гвинея",
        "code": "GIN"
    },
    "GUINEA-BISSAU": {
        "id": 72,
        "title_eng": "Guinea-Bissau",
        "title_rus": "Гвинея-Бисау",
        "code": "GNB"
    },
    "GUYANA": {
        "id": 73,
        "title_eng": "Guyana",
        "title_rus": "Гайана",
        "code": "GUY"
    },
    "HAITI": {
        "id": 74,
        "title_eng": "Haiti",
        "title_rus": "Гаити",
        "code": "HTI"
    },
    "HONDURAS": {
        "id": 75,
        "title_eng": "Honduras",
        "title_rus": "Гондурас",
        "code": "HND"
    },
    "HUNGARY": {
        "id": 76,
        "title_eng": "Hungary",
        "title_rus": "Венгрия",
        "code": "HUN"
    },
    "ICELAND": {
        "id": 77,
        "title_eng": "Iceland",
        "title_rus": "Исландия",
        "code": "ISL"
    },
    "INDIA": {
        "id": 78,
        "title_eng": "India",
        "title_rus": "Индия",
        "code": "IND"
    },
    "INDONESIA": {
        "id": 79,
        "title_eng": "Indonesia",
        "title_rus": "Индонезия",
        "code": "IDN"
    },
    "IRAN": {
        "id": 80,
        "title_eng": "Iran",
        "title_rus": "Иран",
        "code": "IRN"
    },
    "IRAQ": {
        "id": 81,
        "title_eng": "Iraq",
        "title_rus": "Ирак",
        "code": "IRQ"
    },
    "IRELAND": {
        "id": 82,
        "title_eng": "Ireland",
        "title_rus": "Ирландия",
        "code": "IRL"
    },
    "ISRAEL": {
        "id": 83,
        "title_eng": "Israel",
        "title_rus": "Израиль",
        "code": "ISR"
    },
    "ITALY": {
        "id": 84,
        "title_eng": "Italy",
        "title_rus": "Италия",
        "code": "ITA"
    },
    "JAMAICA": {
        "id": 85,
        "title_eng": "Jamaica",
        "title_rus": "Ямайка",
        "code": "JAM"
    },
    "JAPAN": {
        "id": 86,
        "title_eng": "Japan",
        "title_rus": "Япония",
        "code": "JPN"
    },
    "JORDAN": {
        "id": 87,
        "title_eng": "Jordan",
        "title_rus": "Иордания",
        "code": "JOR"
    },
    "KAZAKHSTAN": {
        "id": 88,
        "title_eng": "Kazakhstan",
        "title_rus": "Казахстан",
        "code": "KAZ"
    },
    "KENYA": {
        "id": 89,
        "title_eng": "Kenya",
        "title_rus": "Кения",
        "code": "KEN"
    },
    "KIRIBATI": {
        "id": 90,
        "title_eng": "Kiribati",
        "title_rus": "Кирибати",
        "code": "KIR"
    },
    "KOREA, NORTH": {
        "id": 91,
        "title_eng": "Korea, North",
        "title_rus": "Корея, Северная",
        "code": "PRK"
    },
    "KOREA, SOUTH": {
        "id": 92,
        "title_eng": "Korea, South",
        "title_rus": "Корея, Южная",
        "code": "KOR"
    },
    "KOSOVO": {
        "id": 93,
        "title_eng": "Kosovo",
        "title_rus": "Косово",
        "code": "XKX"
    },
    "KUWAIT": {
        "id": 94,
        "title_eng": "Kuwait",
        "title_rus": "Кувейт",
        "code": "KWT"
    },
    "KYRGYZSTAN": {
        "id": 95,
        "title_eng": "Kyrgyzstan",
        "title_rus": "Киргизия",
        "code": "KGZ"
    },
    "LAOS": {
        "id": 96,
        "title_eng": "Laos",
        "title_rus": "Лаос",
        "code": "LAO"
    },
    "LATVIA": {
        "id": 97,
        "title_eng": "Latvia",
        "title_rus": "Латвия",
        "code": "LVA"
    },
    "LEBANON": {
        "id": 98,
        "title_eng": "Lebanon",
        "title_rus": "Ливан",
        "code": "LBN"
    },
    "LESOTHO": {
        "id": 99,
        "title_eng": "Lesotho",
        "title_rus": "Лесото",
        "code": "LSO"
    },
    "LIBERIA": {
        "id": 100,
        "title_eng": "Liberia",
        "title_rus": "Либерия",
        "code": "LBR"
    },
    "LIBYA": {
        "id": 101,
        "title_eng": "Libya",
        "title_rus": "Ливия",
        "code": "LBY"
    },
    "LIECHTENSTEIN": {
        "id": 102,
        "title_eng": "Liechtenstein",
        "title_rus": "Лихтенштейн",
        "code": "LIE"
    },
    "LITHUANIA": {
        "id": 103,
        "title_eng": "Lithuania",
        "title_rus": "Литва",
        "code": "LTU"
    },
    "LUXEMBOURG": {
        "id": 104,
        "title_eng": "Luxembourg",
        "title_rus": "Люксембург",
        "code": "LUX"
    },
    "MADAGASCAR": {
        "id": 105,
        "title_eng": "Madagascar",
        "title_rus": "Мадагаскар",
        "code": "MDG"
    },
    "MALAWI": {
        "id": 106,
        "title_eng": "Malawi",
        "title_rus": "Малави",
        "code": "MWI"
    },
    "MALAYSIA": {
        "id": 107,
        "title_eng": "Malaysia",
        "title_rus": "Малайзия",
        "code": "MYS"
    },
    "MALDIVES": {
        "id": 108,
        "title_eng": "Maldives",
        "title_rus": "Мальдивы",
        "code": "MDV"
    },
    "MALI": {
        "id": 109,
        "title_eng": "Mali",
        "title_rus": "Мали",
        "code": "MLI"
    },
    "MALTA": {
        "id": 110,
        "title_eng": "Malta",
        "title_rus": "Мальта",
        "code": "MLT"
    },
    "MARSHALL ISLANDS": {
        "id": 111,
        "title_eng": "Marshall Islands",
        "title_rus": "Маршалловы Острова",
        "code": "MHL"
    },
    "MAURITANIA": {
        "id": 112,
        "title_eng": "Mauritania",
        "title_rus": "Мавритания",
        "code": "MRT"
    },
    "MAURITIUS": {
        "id": 113,
        "title_eng": "Mauritius",
        "title_rus": "Маврикий",
        "code": "MUS"
    },
    "MEXICO": {
        "id": 114,
        "title_eng": "Mexico",
        "title_rus": "Мексика",
        "code": "MEX"
    },
    "MICRONESIA, FEDERATED STATES OF": {
        "id": 115,
        "title_eng": "Micronesia, Federated States of",
        "title_rus": "Микронезия, Федеративные Штаты",
        "code": "FSM"
    },
    "MOLDOVA": {
        "id": 116,
        "title_eng": "Moldova",
        "title_rus": "Молдова",
        "code": "MDA"
    },
    "MONACO": {
        "id": 117,
        "title_eng": "Monaco",
        "title_rus": "Монако",
        "code": "MCO"
    },
    "MONGOLIA": {
        "id": 118,
        "title_eng": "Mongolia",
        "title_rus": "Монголия",
        "code": "MNG"
    },
    "MONTENEGRO": {
        "id": 119,
        "title_eng": "Montenegro",
        "title_rus": "Черногория",
        "code": "MNE"
    },
    "MOROCCO": {
        "id": 120,
        "title_eng": "Morocco",
        "title_rus": "Марокко",
        "code": "MAR"
    },
    "MOZAMBIQUE": {
        "id": 121,
        "title_eng": "Mozambique",
        "title_rus": "Мозамбик",
        "code": "MOZ"
    },
    "MYANMAR (BURMA)": {
        "id": 122,
        "title_eng": "Myanmar (Burma)",
        "title_rus": "Мьянма (Бирма)",
        "code": "MMR"
    },
    "NAMIBIA": {
        "id": 123,
        "title_eng": "Namibia",
        "title_rus": "Намибия",
        "code": "NAM"
    },
    "NAURU": {
        "id": 124,
        "title_eng": "Nauru",
        "title_rus": "Науру",
        "code": "NRU"
    },
    "NEPAL": {
        "id": 125,
        "title_eng": "Nepal",
        "title_rus": "Непал",
        "code": "NPL"
    },
    "NETHERLANDS": {
        "id": 126,
        "title_eng": "Netherlands",
        "title_rus": "Нидерланды",
        "code": "NLD"
    },
    "NEW ZEALAND": {
        "id": 127,
        "title_eng": "New Zealand",
        "title_rus": "Новая Зеландия",
        "code": "NZL"
    },
    "NICARAGUA": {
        "id": 128,
        "title_eng": "Nicaragua",
        "title_rus": "Никарагуа",
        "code": "NIC"
    },
    "NIGER": {
        "id": 129,
        "title_eng": "Niger",
        "title_rus": "Нигер",
        "code": "NER"
    },
    "NIGERIA": {
        "id": 130,
        "title_eng": "Nigeria",
        "title_rus": "Нигерия",
        "code": "NGA"
    },
    "NORTH MACEDONIA": {
        "id": 131,
        "title_eng": "North Macedonia",
        "title_rus": "Северная Македония",
        "code": "MKD"
    },
    "NORWAY": {
        "id": 132,
        "title_eng": "Norway",
        "title_rus": "Норвегия",
        "code": "NOR"
    },
    "OMAN": {
        "id": 133,
        "title_eng": "Oman",
        "title_rus": "Оман",
        "code": "OMN"
    },
    "PAKISTAN": {
        "id": 134,
        "title_eng": "Pakistan",
        "title_rus": "Пакистан",
        "code": "PAK"
    },
    "PALAU": {
        "id": 135,
        "title_eng": "Palau",
        "title_rus": "Палау",
        "code": "PLW"
    },
    "PANAMA": {
        "id": 136,
        "title_eng": "Panama",
        "title_rus": "Панама",
        "code": "PAN"
    },
    "PAPUA NEW GUINEA": {
        "id": 137,
        "title_eng": "Papua New Guinea",
        "title_rus": "Папуа — Новая Гвинея",
        "code": "PNG"
    },
    "PARAGUAY": {
        "id": 138,
        "title_eng": "Paraguay",
        "title_rus": "Парагвай",
        "code": "PRY"
    },
    "PERU": {
        "id": 139,
        "title_eng": "Peru",
        "title_rus": "Перу",
        "code": "PER"
    },
    "PHILIPPINES": {
        "id": 140,
        "title_eng": "Philippines",
        "title_rus": "Филиппины",
        "code": "PHL"
    },
    "POLAND": {
        "id": 141,
        "title_eng": "Poland",
        "title_rus": "Польша",
        "code": "POL"
    },
    "PORTUGAL": {
        "id": 142,
        "title_eng": "Portugal",
        "title_rus": "Португалия",
        "code": "PRT"
    },
    "QATAR": {
        "id": 143,
        "title_eng": "Qatar",
        "title_rus": "Катар",
        "code": "QAT"
    },
    "ROMANIA": {
        "id": 144,
        "title_eng": "Romania",
        "title_rus": "Румыния",
        "code": "ROU"
    },
    "RUSSIA": {
        "id": 145,
        "title_eng": "Russia",
        "title_rus": "Россия",
        "code": "RUS"
    },
    "RWANDA": {
        "id": 146,
        "title_eng": "Rwanda",
        "title_rus": "Руанда",
        "code": "RWA"
    },
    "SAINT KITTS AND NEVIS": {
        "id": 147,
        "title_eng": "Saint Kitts and Nevis",
        "title_rus": "Сент-Китс и Невис",
        "code": "KNA"
    },
    "SAINT LUCIA": {
        "id": 148,
        "title_eng": "Saint Lucia",
        "title_rus": "Сент-Люсия",
        "code": "LCA"
    },
    "SAINT VINCENT AND THE GRENADINES": {
        "id": 149,
        "title_eng": "Saint Vincent and the Grenadines",
        "title_rus": "Сент-Винсент и Гренадины",
        "code": "VCT"
    },
    "SAMOA": {
        "id": 150,
        "title_eng": "Samoa",
        "title_rus": "Самоа",
        "code": "WSM"
    },
    "SAN MARINO": {
        "id": 151,
        "title_eng": "San Marino",
        "title_rus": "Сан-Марино",
        "code": "SMR"
    },
    "SAO TOME AND PRINCIPE": {
        "id": 152,
        "title_eng": "Sao Tome and Principe",
        "title_rus": "Сан-Томе и Принсипи",
        "code": "STP"
    },
    "SAUDI ARABIA": {
        "id": 153,
        "title_eng": "Saudi Arabia",
        "title_rus": "Саудовская Аравия",
        "code": "SAU"
    },
    "SENEGAL": {
        "id": 154,
        "title_eng": "Senegal",
        "title_rus": "Сенегал",
        "code": "SEN"
    },
    "SERBIA": {
        "id": 155,
        "title_eng": "Serbia",
        "title_rus": "Сербия",
        "code": "SRB"
    },
    "SEYCHELLES": {
        "id": 156,
        "title_eng": "Seychelles",
        "title_rus": "Сейшельские Острова",
        "code": "SYC"
    },
    "SIERRA LEONE": {
        "id": 157,
        "title_eng": "Sierra Leone",
        "title_rus": "Сьерра-Леоне",
        "code": "SLE"
    },
    "SINGAPORE": {
        "id": 158,
        "title_eng": "Singapore",
        "title_rus": "Сингапур",
        "code": "SGP"
    },
    "SLOVAKIA": {
        "id": 159,
        "title_eng": "Slovakia",
        "title_rus": "Словакия",
        "code": "SVK"
    },
    "SLOVENIA": {
        "id": 160,
        "title_eng": "Slovenia",
        "title_rus": "Словения",
        "code": "SVN"
    },
    "SOLOMON ISLANDS": {
        "id": 161,
        "title_eng": "Solomon Islands",
        "title_rus": "Соломоновы Острова",
        "code": "SLB"
    },
    "SOMALIA": {
        "id": 162,
        "title_eng": "Somalia",
        "title_rus": "Сомали",
        "code": "SOM"
    },
    "SOUTH AFRICA": {
        "id": 163,
        "title_eng": "South Africa",
        "title_rus": "ЮАР",
        "code": "ZAF"
    },
    "SPAIN": {
        "id": 164,
        "title_eng": "Spain",
        "title_rus": "Испания",
        "code": "ESP"
    },
    "SRI LANKA": {
        "id": 165,
        "title_eng": "Sri Lanka",
        "title_rus": "Шри-Ланка",
        "code": "LKA"
    },
    "SUDAN": {
        "id": 166,
        "title_eng": "Sudan",
        "title_rus": "Судан",
        "code": "SDN"
    },
    "SUDAN, SOUTH": {
        "id": 167,
        "title_eng": "Sudan, South",
        "title_rus": "Южный Судан",
        "code": "SSD"
    },
    "SURINAME": {
        "id": 168,
        "title_eng": "Suriname",
        "title_rus": "Суринам",
        "code": "SUR"
    },
    "SWEDEN": {
        "id": 169,
        "title_eng": "Sweden",
        "title_rus": "Швеция",
        "code": "SWE"
    },
    "SWITZERLAND": {
        "id": 170,
        "title_eng": "Switzerland",
        "title_rus": "Швейцария",
        "code": "CHE"
    },
    "SYRIA": {
        "id": 171,
        "title_eng": "Syria",
        "title_rus": "Сирия",
        "code": "SYR"
    },
    "TAIWAN": {
        "id": 172,
        "title_eng": "Taiwan",
        "title_rus": "Тайвань",
        "code": "TWN"
    },
    "TAJIKISTAN": {
        "id": 173,
        "title_eng": "Tajikistan",
        "title_rus": "Таджикистан",
        "code": "TJK"
    },
    "TANZANIA": {
        "id": 174,
        "title_eng": "Tanzania",
        "title_rus": "Танзания",
        "code": "TZA"
    },
    "THAILAND": {
        "id": 175,
        "title_eng": "Thailand",
        "title_rus": "Таиланд",
        "code": "THA"
    },
    "TOGO": {
        "id": 176,
        "title_eng": "Togo",
        "title_rus": "Того",
        "code": "TGO"
    },
    "TONGA": {
        "id": 177,
        "title_eng": "Tonga",
        "title_rus": "Тонга",
        "code": "TON"
    },
    "TRINIDAD AND TOBAGO": {
        "id": 178,
        "title_eng": "Trinidad and Tobago",
        "title_rus": "Тринидад и Тобаго",
        "code": "TTO"
    },
    "TUNISIA": {
        "id": 179,
        "title_eng": "Tunisia",
        "title_rus": "Тунис",
        "code": "TUN"
    },
    "TURKEY": {
        "id": 180,
        "title_eng": "Turkey",
        "title_rus": "Турция",
        "code": "TUR"
    },
    "TURKMENISTAN": {
        "id": 181,
        "title_eng": "Turkmenistan",
        "title_rus": "Туркменистан",
        "code": "TKM"
    },
    "TUVALU": {
        "id": 182,
        "title_eng": "Tuvalu",
        "title_rus": "Тувалу",
        "code": "TUV"
    },
    "UGANDA": {
        "id": 183,
        "title_eng": "Uganda",
        "title_rus": "Уганда",
        "code": "UGA"
    },
    "UKRAINE": {
        "id": 184,
        "title_eng": "Ukraine",
        "title_rus": "Украина",
        "code": "UKR"
    },
    "UNITED ARAB EMIRATES": {
        "id": 185,
        "title_eng": "United Arab Emirates",
        "title_rus": "ОАЭ",
        "code": "ARE"
    },
    "UNITED KINGDOM": {
        "id": 186,
        "title_eng": "United Kingdom",
        "title_rus": "Великобритания",
        "code": "GBR"
    },
    "UNITED STATES": {
        "id": 187,
        "title_eng": "United States",
        "title_rus": "США",
        "code": "USA"
    },
    "URUGUAY": {
        "id": 188,
        "title_eng": "Uruguay",
        "title_rus": "Уругвай",
        "code": "URY"
    },
    "UZBEKISTAN": {
        "id": 189,
        "title_eng": "Uzbekistan",
        "title_rus": "Узбекистан",
        "code": "UZB"
    },
    "VANUATU": {
        "id": 190,
        "title_eng": "Vanuatu",
        "title_rus": "Вануату",
        "code": "VUT"
    },
    "VATICAN CITY": {
        "id": 191,
        "title_eng": "Vatican City",
        "title_rus": "Ватикан",
        "code": "VAT"
    },
    "VENEZUELA": {
        "id": 192,
        "title_eng": "Venezuela",
        "title_rus": "Венесуэла",
        "code": "VEN"
    },
    "VIETNAM": {
        "id": 193,
        "title_eng": "Vietnam",
        "title_rus": "Вьетнам",
        "code": "VNM"
    },
    "YEMEN": {
        "id": 194,
        "title_eng": "Yemen",
        "title_rus": "Йемен",
        "code": "YEM"
    },
    "ZAMBIA": {
        "id": 195,
        "title_eng": "Zambia",
        "title_rus": "Замбия",
        "code": "ZMB"
    },
    "ZIMBABWE": {
        "id": 196,
        "title_eng": "Zimbabwe",
        "title_rus": "Зимбабве",
        "code": "ZWE"
    }
}

COUNTRIES_LIST: list[str] = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "The Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo, Democratic Republic of the",
    "Congo, Republic of the",
    "Costa Rica",
    "Côte d’Ivoire",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "East Timor (Timor-Leste)",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "The Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, North",
    "Korea, South",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia, Federated States of",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar (Burma)",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Sudan, South",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]
