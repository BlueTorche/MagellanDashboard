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

# Script Powershell et Task Windows

## Requête HTTP 

Le dashboard se base sur la réception d'une requête HTTP pour fonctionner. 
Cette requête doit contenir dans son body au minimum les infos suivantes : 

> { "User" : "" ; "Computer" = "" }

Ces infos sont sous la forme d'un body HTTP json classique. 

## Script Powershell 

Afin d'envoyer les données en HTTP, plusieurs méthodes sont possibles.
J'ai personnellement décider d'utiliser un script Powershell, car ça permet de faire plein d'autres choses.
Voici le script utilisé :

```
$User = (Get-WmiObject -Class Win32_ComputerSystem).UserName
$uri = "http://0.0.0.0/api/endpoint"
$body = @{
    "User" = $User
    "Computer" = $env:COMPUTERNAME
}
$jsonBody = $body | ConvertTo-Json

Invoke-RestMethod -Uri $uri -Method Post -Body $jsonBody -ContentType "application/json"
```

Notez que le `0.0.0.0` du script doit être remplacé par l'adresse IP du serveur web. 

## Plannification de tâches 

Le serveur web doit recevoir les données des PC fréquemment pour être utile.
Il faut donc programmer les PC pour exécuter le script Powershell ci-dessus de manière périodique.
La manière la plus simple de faire est d'utiliser la plannification de tâches Windows. 
Pour des raisons de sécurité, je ne décrirais pas exactement ce que fait la tâche ici, 
mais globalement elle se contente d'exécuter le script ci-dessus toutes les 10min. 
Je ferai un document dans le Drive Magellan décrivant la tâches.

Cette tâches est également trouvable en format XML dans le drive Magellan. 
Pour importer la tâches sur un PC, il suffit de la télécharger en local et de rentrer la commande suivante : 

```
schtasks /create /tn "AutomationScript" /xml C:\chemin\vers\la\tache.xml
```

Evidemment, il faut remplacer `C:\chemin\vers\la\tache.xml` par le chemin absolu du ficier XML de la tâche.

Notez que la tâche peut prendre jusqu'à 24h pour se lancer la première fois, et ensuite effectuer la répétition. 
Si vous souhaitez forcer la répétition à commencer immédiatement, vous pouvez entrez la commande : 

```
schtasks /run /tn "AutomationScript"
```
