# Servidor DNS BIND9 Dockerizado

Este projeto fornece um servidor DNS BIND9 em container Docker usando uma imagem baseada em Debian. Desenvolvido para o starfish.com.br

## 📌 Funcionalidades

- Utiliza Debian Bullseye Slim como imagem base.
- Instala BIND9, bind9utils e dnsutils para funcionalidade DNS completa.
- Pré-carrega configurações personalizadas de `BIND_CONFIG/bind/` para `/etc/bind/`.
- Suporta conexões TCP e UDP na porta 53.

## 🛠 Configuração & Instalação

### 🔄 Passo 0: Preparar Configurações Personalizadas

Copie suas configurações do BIND para o diretório `/etc/bind/` do container:

```sh
# Certifique-se que suas configurações estão em ./BIND_CONFIG/bind/
cp -R ./BIND_CONFIG/bind/* /etc/bind/
```
1️⃣ Construir a Imagem Docker
```sh
docker build -t bind9 .
```
2️⃣ Executar o Container
```sh
docker run -d --name bind9 -p 53:53/udp -p 53:53/tcp --dns=192.168.0.5 bind9
```
3️⃣ Testar Resolução DNS
```sh
nslookup www.starfish.com.br 127.0.0.1
# OU
dig @127.0.0.1 www.starfish.com.br
```

### Endereços compativeis para o teste

```
www.starfish.com.br -> 192.168.0.100
mail.starfish.com.br -> 192.168.0.101
```