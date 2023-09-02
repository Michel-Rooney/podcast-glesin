# TeenPod API

O projeto consiste no desenvolvimento de uma API (Interface de Programação de Aplicativos) para um Sistema de Gerenciamento de Podcasts, com o objetivo de permitir aos usuários criar, visualizar, atualizar e deletar podcasts em suas listas pessoais. A API será construída utilizando tecnologias web modernas e seguirá os princípios REST (Representational State Transfer) para garantir a comunicação eficiente entre o cliente e o servidor.

### 📋 Documentação
[TeenPod API - DOCS](https://documenter.getpostman.com/view/23133439/2s9Xy5LW2t)

### 📌 On Air
[TeenPod API - Deploy](https://teenpod.pythonanywhere.com/)

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

### 📋 Pré-requisitos

Você precisa do [Python](https://www.python.org/downloads/) instaldo na sua máquina

```
# Verificar se está instaldo
# Linux
python3 --version

# Windows
python --version
```

**Note:** Os comandos abaixo seram na maioria relacionados a linux

### 🔧 Instalação

Clone o repositório do projeto:

```git
git clone https://github.com/Michel-Rooney/teen-pod.git
```

Entre na pasta:

```
cd teen-pod
```

Crie um ambiente virtual:

```
python3 -m venv venv
```

Ative o ambiente virtual:

```
source venv/bin/activate

# Quando ativo, irar aparecer (venv) no inicio
(venv) user@maquina ~/teen-pod$
```

**Note:** Para desativar rode o comando
```
source deactivate
```

Instale as dependencias:

```
pip install -r requirements.txt
```

Copie o arquivo .env-example para .env:

```
cp .env-example .env

# No arquivo .env substitua a SECRET_KEY para qualquer coisa
```

Inicie o projeto:

```
python manage.py runserver
```

## 🛠️ Construído com

* [Python](https://www.python.org/) - Linguagem
* [Django](https://www.djangoproject.com/) - Framework Python
* [Django Rest Framework](https://www.django-rest-framework.org/) - Framework Rest para API's
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - Biblioteca de authenticação

## ✒️ Autores

* [Michel-Rooney](https://github.com/Michel-Rooney/) - *Dev. Backend*
