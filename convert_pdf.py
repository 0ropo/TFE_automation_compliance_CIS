
from pypdf import PdfReader
import re
import yaml

PDF_FILE = "./cis_pdf/cis_ios17.pdf"
OUTPUT_YAML = "cis_ios17_complet.yml"

rule_title_pattern = re.compile(r"^(\d+\.\d+\.\d+)\s+(.*?)\s+\((Automated|Manual)\)$")
section_start_pattern = re.compile(r"^(Description|Rationale|Impact|Audit|Remediation|Default Value|References)\s*:?$", re.IGNORECASE)
level_pattern = re.compile(r"Level\s+(1|2)", re.IGNORECASE)
commande_extract_pattern = re.compile(r"'([^']+)'")

def extract_commands_only(lines):
    cmds = []
    for l in lines:
        if "#" in l:
            cmd = l.split("#", 1)[1].strip()
            if cmd:
                cmds.append(cmd)
    return cmds

reader = PdfReader(PDF_FILE)
contenu_final = []
current_rule = None
current_section = None
section_data = {
    "Description": [],
    "Rationale": [],
    "Impact": [],
    "Audit": [],
    "Remediation": [],
    "Default Value": []
}
level = None

for page in reader.pages:
    lines = page.extract_text().split("\n")
    for line in lines:
        line = line.strip()

        match = rule_title_pattern.match(line)
        if match:
            if current_rule:
                for key in section_data:
                    value = section_data[key]
                    if key in ["Audit", "Remediation"]:
                        cmds = extract_commands_only(value)
                        current_rule[key.lower()] = "\n".join(cmds).strip() or None
                    else:
                        current_rule[key.lower().replace(" ", "_")] = "\n".join(value).strip() or None
                current_rule["level"] = level
                contenu_final.append(current_rule)

            titre_texte = match.group(2)
            commande_match = commande_extract_pattern.search(titre_texte)
            commande = commande_match.group(1).strip() if commande_match else None

            current_rule = {
                "titre": match.group(1),
                "titre_texte": titre_texte,
                "automated_or_manual": match.group(3),
                "level": None,
                "commande": commande
            }
            section_data = {k: [] for k in section_data}
            level = None
            current_section = None
            continue

        if not level:
            level_match = level_pattern.search(line)
            if level_match:
                level = f"Level {level_match.group(1)}"

        section_match = section_start_pattern.match(line)
        if section_match:
            new_section = section_match.group(1)
            current_section = new_section if new_section != "References" else None
            continue

        if current_section and current_section in section_data:
            section_data[current_section].append(line)

if current_rule:
    for key in section_data:
        value = section_data[key]
        if key in ["Audit", "Remediation"]:
            cmds = extract_commands_only(value)
            current_rule[key.lower()] = "\n".join(cmds).strip() or None
        else:
            current_rule[key.lower().replace(" ", "_")] = "\n".join(value).strip() or None
    current_rule["level"] = level
    contenu_final.append(current_rule)

# Création du dictionnaire indexé par "titre"
rules_dict = {item["titre"]: item for item in contenu_final}

with open(OUTPUT_YAML, "w", encoding="utf-8") as f:
    yaml.dump(rules_dict, f, sort_keys=False, allow_unicode=True)

print(f"{len(rules_dict)} règles enregistrées dans un dictionnaire indexé par 'titre'.")
