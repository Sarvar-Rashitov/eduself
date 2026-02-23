"""
Qo'shimcha statik tarjimalar
"""
import json

new_translations = {
    "fan": {
        "en": "subject",
        "ru": "предмет",
        "kk": "пән",
        "kaa": "фан",
        "tg": "фан",
        "ky": "предмет"
    },
    "O'zbekiston umumta'lim fanlari bo'yicha testlar va mavzular": {
        "en": "Tests and topics on general education subjects of Uzbekistan",
        "ru": "Тесты и темы по общеобразовательным предметам Узбекистана",
        "kk": "Өзбекстанның жалпы білім беру пәндері бойынша тесттер мен тақырыптар",
        "kaa": "Өзбекстанның жалпы билим бериў фанлары бойынша тестлер ҳәм мавзулар",
        "tg": "Тестҳо ва мавзуъҳо оид ба фанҳои таҳсилоти умумии Ӯзбекистон",
        "ky": "Өзбекстандын жалпы билим берүү предметтери боюнча тесттер жана темалар"
    },
    "ta": {
        "en": "",
        "ru": "",
        "kk": "",
        "kaa": "",
        "tg": "",
        "ky": ""
    }
}

# Mavjud tarjimalarni yuklash
with open('static_translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Yangi tarjimalarni qo'shish
count_before = len(translations)
translations.update(new_translations)
count_after = len(translations)

# Saqlash
with open('static_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"✓ {count_after - count_before} ta yangi tarjima qo'shildi!")
print(f"✓ Jami tarjimalar: {count_after}")
