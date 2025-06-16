![Ansible](https://img.shields.io/badge/ansible-automation-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![WIP](https://img.shields.io/badge/status-work--in--progress-orange)

> **Automatisation de la conformité des équipements de différents technologies avec Ansible**  
> Travail de fin d’études – EPHEC 2025

## Prérequis

- Configurer vos machines en connexion **SSH par clé publique**.

- Configurer le fichier ansible.cfg pour lui indiquer le chemin vers votre inventaire.

- S'assurer que la collection `cisco.ios` est bien installée avec Ansible-Galaxy.

- S'assurer que le fichier de référence soit appelé "cis_ios17_complet.yml" et qu'il contient les bonnes pratiques CIS soit sous le format suivant et que pour un titre, on ait qu'une seule commande:


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

- Remarque si plusieurs commandes de remédiation sont présentes pour un même titre dans le pdf CIS:
```
2.2.1:
remédiation:
  hostname(config)#archive
  hostname(config-archive)#log config
  hostname(config-archive-log-cfg)#logging enable
  hostname(config-archive-log-cfg)#end
```

Je vous conseille de créer un numéro séparé pour chaque commande dans le fichier de référence comme ceci:  
'''
2.2.1.1:
  titre: 2.2.1.1
  ...
  commande: archive
  ...
2.2.1.2:
  titre: 2.2.1.2
  ...
  commande: log config
  ...
2.2.1.3:
  titre: 2.2.1.3
  commande: logging enable
  ...
etc,
'''


Commande d'installtion de la collection `cisco.ios`:

```
ansible-galaxy collection install cisco.ios
```

- Ajouter vos machines dans le fichier `hosts.yml` dans le dossier `inventory` et chiffrer le fichier avec **Ansible Vault** dans le cas ou vous utilisez un mot de passe au lieu d'une clé. Voici un exemple du contenu attendu:
- 
Exemple de la déclaration d'un routeur R1 dans le fichier `hosts.yml`:
```
routers:
  children:
    R1:
      hosts:
        R1_ip:
  vars:
    ansible_connection: network_cli
    ansible_network_os: cisco.ios.ios (if cisco else see Ansible Documentations)  
    ansible_user: user_for_ssh
    ansible_ssh_pass: ssh_password ou private_key_file: location_private_key
    ansible_network_cli_ssh_type: libssh (dans le cas ou vous utilisez un routeur cisco IOS 15 et que la clé utilise du ssh-rsa)
```

## Chiffrement des fichiers sensibles 

Pour certains fichiers sensibles, il est nécessaire de chiffrer ces fichiers avec Ansible-vault, exemple avec le fichier hosts.yml qui contient les credentials de connexion:
```
ansible-vault encrypt hosts.yml
```


## Initialisation du projet

```
git clone https://github.com/0ropo/TFE_automation_compliance_CIS.git
cd TFE_automation_compliance_CIS
```

## Lancer le playbook principal

```
ansible-playbook playbook_detect_OS.yml --ask-vault-pass ou --vault-password-file /path/to/my/vault-password-file (si vous utilisez un fichier contenant des mots de passes ansible-vault)
```
