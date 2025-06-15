import re
import os

# === 1) Lire le JS principal ===
js_filename = "JVChat_Premium.user.js"
with open(js_filename, "r", encoding="utf-8") as f:
    js_content = f.read()

# === 2) Lire le CSS ===
css_filename = "jvchat-premium.css"
with open(css_filename, "r", encoding="utf-8") as f:
    css_content = f.read()

# === 3) Corriger Unicode : \EA ➜ \UEA
css_content = re.sub(r"\\([0-9A-Fa-f]{2,6})", r"\\U\1", css_content)

# === 4) Préparer le bloc CSS
css_block = f"let CSS = `<style type=\"text/css\" id=\"jvchat-css\">\n{css_content}\n</style>`;\n"

# === 5) Nettoyer l’entête : supprimer @grant et @resource
js_content = re.sub(r"^//\s*@grant.*$\n?", "", js_content, flags=re.MULTILINE)
js_content = re.sub(r"^//\s*@resource.*$\n?", "", js_content, flags=re.MULTILINE)

# === 6) Ajouter `@grant none` après @version ou avant ==/UserScript==
js_content = re.sub(
    r"(// ==UserScript==.*?)(\n)(?=// @|// ==/UserScript==)",
    r"\1\n// @grant       none",
    js_content,
    flags=re.DOTALL
)

# === 7) Supprimer la ligne `const jvchatCSS = GM_getResourceText(...)`
js_content = re.sub(r"^.*GM_getResourceText.*$\n?", "", js_content, flags=re.MULTILINE)

# === 8) Remplacer `GM_addStyle(jvchatCSS);` par `document.head.insertAdjacentHTML(...)`
js_content = js_content.replace(
    "GM_addStyle(jvchatCSS);",
    'document.head.insertAdjacentHTML("beforeend", CSS);'
)

# === 9) Insérer le bloc CSS avant `let freshHash = undefined;`
js_content = js_content.replace(
    "let freshHash = undefined;",
    css_block + "\nlet freshHash = undefined;"
)

# === 10) Construire le nouveau nom du fichier
name_part, ext = os.path.splitext(js_filename)
output_filename = f"{name_part}M{ext}"

# === 11) Sauvegarder le résultat
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ Fichier standalone généré : {output_filename}")

# === 12) Pause manuelle ===
input("\nEntrée pour fermer le script...")
