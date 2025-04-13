from pypdf import PdfReader
import re
import yaml

# === PARAMÈTRES ===
PDF_FILE = "./cis_pdf/cis_iosxe17.pdf"
OUTPUT_YAML = "cis_iosxe17_descriptions_only.yml"

# === CONFIGURATION DES REGEX ===
rule_title_pattern = re.compile(r"^(\d+\.\d+\.\d+)\s+(.*?)\s+\((Automated|Manual)\)$")
description_pattern = re.compile(r"^Description\s*:?$", re.IGNORECASE)
section_end_pattern = re.compile(r"^(Rationale|Impact|Audit|Remediation|Default Value|References)\s*:?$", re.IGNORECASE)

# === INITIALISATION ===
reader = PdfReader(PDF_FILE)
contenu_final = []
current_rule = None
collect_description = False
description_lines = []

# === TRAITEMENT DES PAGES ===
for page in reader.pages:
    lines = page.extract_text().split("\n")
    for line in lines:
        line = line.strip()

        # Détection d'une nouvelle règle
        match = rule_title_pattern.match(line)
        if match:
            if current_rule:
                current_rule["description"] = "\n".join(description_lines).strip() if description_lines else None
                contenu_final.append(current_rule)

            current_rule = {
                "titre": match.group(1),
                "titre_texte": match.group(2),
                "description": None
            }
            description_lines = []
            collect_description = False
            continue

        # Détection du début de la description
        if description_pattern.match(line):
            collect_description = True
            continue

        # Détection de la fin de la section description
        if section_end_pattern.match(line):
            collect_description = False
            continue

        # Collecte des lignes de description
        if collect_description:
            description_lines.append(line)

# Ajouter la dernière règle
if current_rule:
    current_rule["description"] = "\n".join(description_lines).strip() if description_lines else None
    contenu_final.append(current_rule)

# === SAUVEGARDE ===
with open(OUTPUT_YAML, "w", encoding="utf-8") as f:
    yaml.dump(contenu_final, f, sort_keys=False, allow_unicode=True)

print(f"{len(contenu_final)} règles extraites avec description. Fichier sauvegardé dans : {OUTPUT_YAML}")
