# Teste de Carga para Servidor DNS com Python

Este projeto é um script Python para realizar testes de carga do servidor DNS. Ele utiliza **threads** para enviar múltiplas consultas simultâneas e mede o tempo de resposta.

## 📌 Funcionalidades

- Realiza consultas **DNS** usando `dig`.
- Utiliza **multithreading** para testes de carga simultâneos.
- Mede o tempo de resposta e contabiliza consultas bem-sucedidas e falhadas.

## 🛠 Configuração & Instalação

### 1️⃣ Pré-requisitos

Certifique-se de ter o Python instalado e `dig` disponível no sistema.

### 2️⃣ Instalação

Clone o repositório e execute o script:

```sh
git clone https://github.com/heytulio/dns-starfish.git
cd dns-starfish/
python dns_load_test.py
```