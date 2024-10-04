# MagellanDashboard
Dashboard des PCs du 500

# Installation du serveur 
Créer une machine virtuelle Ubuntu server.

Mettez à jour le serveur et installez docker et docker-compose : 


```
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl enable docker && sudo systemctl start docker
sudo apt-get install docker-compose
```

Vérification de la bonne installation des dépendances : 

```
docker --version
docker-compose --version
```

Importez le github (potentiellement, le lien vers le git changera si je met le repo sur le github du magellan un jour) : 


```
git clone https://github.com/BlueTorche/MagellanDashboard.git
```

Lancez le container docker : 

```
cd MagellanDashboard
sudo docker-compose up --build -d
```

Si tout fonctionne bien, vous arriverez à accéder au site web en local.
Il faudra ensuite effectuer la redirection des requête du serveur à l'aide d'un DNS et d'un Reverse Proxy, 
afin de rediriger un URL vers la machine locale (port 80). Pensez également à configurer l'HTTPS 
(normalement ce sera à faire sur le reverse proxy, mais ça dépend de votre configuration).  

# Mise à jour du serveur
Après vous être connecté à la VM (par SSH ou depuis l'hyperviseur) entrez ces commandes : 

```
cd /home/magellan/MagellanDashboard
git pull origin main 
sudo docker-compose stop magellan-logs
sudo docker rm magellan-logs && sudo docker rmi magellandashboard_magellan-logs 
sudo docker-compose up -d --build magellan-logs
```



Notez que ça ne supprimera pas la DB. 
Il existe surement de meilleure manière de l'update, mais je ne suis pas doué en docker :) .