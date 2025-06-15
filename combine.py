import re

# 1. Lire les fichiers
with open("JVChat_Premium.user.js", "r", encoding="utf-8") as f:
    js_content = f.read()

with open("jvchat-premium.css", "r", encoding="utf-8") as f:
    css_content = f.read()

# 2. Corriger Unicode
css_content = css_content.replace("\\EA", "\\uEA")  # ou tout pattern que tu veux

# 3. Remplacer la balise ou le pattern
# Exemple : remplacer le bloc entre /* CSS_START */ et /* CSS_END */
js_content = re.sub(
    r"/\* CSS_START \*/.*?/\* CSS_END \*/",
    f"GM_addStyle('''{css_content}''')",
    js_content,
    flags=re.DOTALL
)

# 4. Optionnel : virer les `@resource` et `GM.getResourceText` restants
js_content = re.sub(r"@resource.*\n", "", js_content)
js_content = re.sub(r"GM\.getResourceText.*\n", "", js_content)

# 5. Sauver le résultat
with open("final.user.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("A finir")
