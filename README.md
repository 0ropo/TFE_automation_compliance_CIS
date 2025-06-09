![Ansible](https://img.shields.io/badge/ansible-automation-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![WIP](https://img.shields.io/badge/status-work--in--progress-orange)

> **Automatisation de la conformité des équipements de différents technologies avec Ansible**  
> Travail de fin d’études – EPHEC 2025

## Prérequis

- Configurer vos machines en connexion SSH par clé publique.

- Ajouter vos machines dans le fichier hosts.yml dans le dossier inventory et chiffrer le fichier avec Ansible Vault dans le cas ou vous utilisez un mot de passe au lieu d'une clé. Voici un exemple du contenu attendu:

- S'assurer que le module cisco.ios est bien installé avec Ansible-Galaxy.

- S'assurer que le fichier de référence contenant les bonnes pratiques CIS soit sous ce format et que pour un titre, on ait qu'une seule commande:


```
1.1.2:
  titre: 1.1.2
  titre_texte: Enable 'aaa authentication login'
  automated_or_manual: Automated
  level: Level 1
  commande: aaa authentication login
  description: Sets authentication, authorization and accounting (AAA) authentication at login.
  rationale: Using AAA authentication for interactive management access to the device provides consistent, centralized control of your network. The default under AAA (local or network)is to require users to log in using a valid user name and password. This rule applies for both local and network AAA. Fallback mode should also be enabled to allow emergency access to the router or switch in the event that the AAA server was unreachable, by utilizing the LOCAL keyword after the AAA server-tag.
  impact: Implementing Cisco AAA is significantly disruptive as former access methods are immediately disabled. Therefore, before implementing Cisco AAA, the organization should carefully review and plan their authentication methods such as logins and passwords, challenges and responses, and which token technologies will be used.
  audit: show run | incl aaa authentication login
  remediation: aaa authentication login {default | aaa_list_name} 
  default_value: null
```

Commande d'installtion du module cisco.ios:

```
ansible-galaxy collection install cisco.ios
```

Exemple de la déclaration d'un routeur R1 dans le fichier hosts.yml:
```
routers:
  children:
    R1:
      hosts:
        R1_ip:
  vars:
    ansible_connection: network_cli
    ansible_network_os: ios  
    ansible_user: enable_password
    ansible_ssh_pass: ssh_password
```

## Initialisation du projet

```
git clone https://github.com/0ropo/TFE_automation_compliance_CIS.git
cd TFE_automation_compliance_CIS
```

## Lancer le playbook principal

```
ansible-playbook playbook_detect_OS.yml
```
