#!/bin/bash

# Mise à jour et installation des paquets
apt-get update &&
apt-get upgrade -y &&
apt-get install -y git libgl1-mesa-glx libxcb-icccm4 nano iputils-ping python3 python3-pip iproute2 libglib2.0-0

# Installation des modules Python
pip3 install pymongo scapy requests flask PyQt5 matplotlib waitress

# Installation de gnupg et ajout de la clé MongoDB
sudo apt-get install gnupg -y
wget -qO - https://www.mongodb.org/static/pgp/server-${MONGO_VERSION}.asc | sudo apt-key add -
cd /etc/apt/sources.list.d/
sudo touch mongodb-org-${MONGO_VERSION}.list
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/${MONGO_VERSION} multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-${MONGO_VERSION}.list
sudo apt-get update

# Installation de MongoDB
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
