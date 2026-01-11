
# Projet VirtOS  

**BELASRI Ayman & Ourrais Youssef**

## Objectif

Créer une infrastructure avec plusieurs VMs et conteneurs Docker qui communiquent entre eux **sans Internet**, avec un **relay**, de la **crypto**, et un **registry local**.

## Machines

- **VM1**  
  - `keygen` → génère les clés RSA  
  - `encryptor` → chiffre les messages  

- **VM3**  
  - `relay` → route les messages  
  - `hasher` → vérifie l’intégrité (hash)  
  - `registry` → stocke les images Docker  

- **Windows**  
  - `authority.py` → envoie les commandes et reçoit les résultats  

## Fonctionnement

1. Windows envoie `START`
2. VM1 chiffre le message
3. VM3 vérifie le hash
4. Windows reçoit le résultat

## Lancer

**VM3**
cd vm3-compose
docker compose up --build

**VM1**
cd vm1-compose
docker compose up --build

**Windows**
python authority.py
