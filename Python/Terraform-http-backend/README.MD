# Terraform Centralized HTTP Backend

Ce script Python (`tf-backend.py`) fournit un backend HTTP distant pour Terraform. 
Il permet de centraliser le fichier d'état (*state*), facilitant le travail collaboratif 
et l'intégration dans des chaînes CI/CD.

## Fonctionnalités clés

* **Persistance :** Stockage du state dans un fichier local sur le serveur (ex: `xenomorph.state`).
* **Verrouillage (Locking) :** Gestion de l'exclusivité via les méthodes `POST` pour éviter les corruptions de données en cas d'accès concurrents.
* **Audit :** Historique complet des accès dans `tf-backend.log`.

## Utilisation

### Lancer le serveur backend

```bash
python3 tf-backend.py
``` 

Le serveur écoute par défaut sur le port 9961.

### Configurer votre projet Terraform

Créez un fichier *backend.tf* dans votre répertoire de travail :

```hcl
terraform {
  backend "http" {
    # Remplacez 'xenomorph' par le nom unique de votre projet
    address        = "[http://192.168.1.9:9961/v1/state/xenomorph](http://192.168.1.9:9961/v1/state/xenomorph)"
    lock_address   = "[http://192.168.1.9:9961/v1/lock/xenomorph](http://192.168.1.9:9961/v1/lock/xenomorph)"
    unlock_address = "[http://192.168.1.9:9961/v1/unlock/xenomorph](http://192.168.1.9:9961/v1/unlock/xenomorph)"
    lock_method    = "POST"
    unlock_method  = "POST"
  }
}

## Détails du stockage

Pour chaque requête pointant vers l'identifiant {name}, le script génère :

* {name}.state : Le contenu du Terraform State et les informations de verrouillage.
* tf-backend.log : Journalisation de tous les accès (IP, date, action).

[!IMPORTANT]

En cas d'utilisation en production ou sur un réseau ouvert, assurez-vous de sécuriser l'accès au serveur (HTTPS/Auth), 
car le state Terraform peut contenir des informations sensibles (mots de passe, clés d'API).
