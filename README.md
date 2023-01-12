
## Rokme

Simple tool for Ngrok Automation

###### Install ngrok via **apt**
```sh
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```
###### Install ngrok via **snap**
```sh
snap install ngrok
```

###### Download **.TGZ** file
```sh
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
```
then
```sh
sudo tar xvzf ~/Downloads/ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
```
or you can vistit to the official [Download](https://ngrok.com/download) page on Ngrok website

---

###### Add authtoken

```sh
 ngrok config add-authtoken <token>
```
## Categories

![](images/01.png)
![](images/03.png)
![](images/04.png)
![](images/05.png)
![](images/06.png)

## Status

![](images/08.png)
![](images/07.png)
![](images/02.png)