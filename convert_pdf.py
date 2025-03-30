from pypdf import PdfReader as pread
import re
import yaml 

pages = pread("./cis_pdf/cis_ios17.pdf").pages
contenu_final=[]

pattern_regex=r"(\d+\.\d+\.\d+)\s+(Enable|Set|Require)\s+(?:'([^']*)'|(.+))"
for page in pages:
    text=page.extract_text()
    for ligne in text.split("\n"):
        trouve=re.search(pattern_regex, ligne)
        if trouve:
            dico={
                "titre":trouve.group(1),
                "commande":trouve.group(3),
            }
            if dico["commande"] is not None:
                contenu_final.append(dico)
print(contenu_final)


with open("cis_ios17.yml", "w") as f:
    yaml.dump(contenu_final, f)