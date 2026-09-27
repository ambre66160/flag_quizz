import os
import urllib.request

# Dossier de destination
output_dir = "assets/flags"
os.makedirs(output_dir, exist_ok=True)

# Codes ISO 3166-1 alpha-2 des 195 États souverains
country_codes = [
    # Afrique (54)
    "za", "dz", "ao", "bj", "bw", "bf", "bi", "cv", "cm", "km", "cg", "cd", "ci", "dj",
    "eg", "er", "sz", "et", "ga", "gm", "gh", "gn", "gw", "gq", "ke", "ls", "lr", "ly",
    "mg", "mw", "ml", "ma", "mu", "mr", "mz", "na", "ne", "ng", "ug", "rw", "st", "sn",
    "sc", "sl", "so", "sd", "ss", "tz", "td", "tg", "tn", "zm", "zw",

    # Amériques (35)
    "ag", "ar", "bs", "bb", "bz", "bo", "br", "ca", "cl", "co", "cr", "cu", "dm", "ec",
    "us", "gd", "gt", "gy", "ht", "hn", "jm", "mx", "ni", "pa", "py", "pe", "do", "kn",
    "lc", "vc", "sv", "sr", "tt", "uy", "ve",

    # Asie (48)
    "af", "sa", "am", "az", "bh", "bd", "bt", "mm", "bn", "kh", "cn", "cy", "kp", "kr",
    "ae", "ge", "in", "id", "iq", "ir", "il", "jp", "jo", "kz", "kg", "kw", "la", "lb",
    "my", "mv", "mn", "np", "om", "uz", "pk", "ps", "ph", "qa", "sg", "lk", "sy", "tj",
    "th", "tl", "tm", "tr", "vn", "ye",

    # Europe (44)
    "al", "de", "ad", "at", "be", "by", "ba", "bg", "hr", "dk", "es", "ee", "fi", "fr",
    "gr", "hu", "ie", "is", "it", "lv", "li", "lt", "lu", "mk", "mt", "md", "mc", "me",
    "no", "nl", "pl", "pt", "cz", "ro", "gb", "ru", "sm", "rs", "sk", "si", "se", "ch",
    "va",

    # Océanie (14)
    "au", "fj", "ki", "mh", "fm", "nr", "nz", "pw", "pg", "sb", "ws", "to", "tv", "vu"
]

print(f"Téléchargement des drapeaux dans '{output_dir}/'...")

success_count = 0
for code in country_codes:
    # URL de l'image PNG (largeur 320px, adaptée pour les affichages web/mobile)
    url = f"https://flagcdn.com/w320/{code}.png"
    file_path = os.path.join(output_dir, f"{code}.png")

    try:
        urllib.request.urlretrieve(url, file_path)
        success_count += 1
        print(f"[{success_count}/{len(country_codes)}] Téléchargé : {code}.png")
    except Exception as e:
        print(f"Erreur pour {code}.png : {e}")

print(f"\nTerminé ! {success_count} drapeaux ont été enregistrés dans {output_dir}/")