# Podcast Glesin API

O projeto consiste no desenvolvimento de uma API (Interface de Programação de Aplicativos) para um Sistema de Gerenciamento de Podcasts, com o objetivo de permitir aos usuários criar, visualizar, atualizar e deletar podcasts em suas listas pessoais. A API será construída utilizando tecnologias web modernas e seguirá os princípios REST (Representational State Transfer) para garantir a comunicação eficiente entre o cliente e o servidor.

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
git clone https://github.com/Michel-Rooney/podcast-glesin.git
```

Entre na pasta:

```
cd podcast-glesin
```

Crie um ambiente virtual:

```python
python3 -m venv venv
```

Ative o ambiente virtual:

```
source venv/bin/activate

# Quando ativo, irar aparecer (venv) no inicio
(venv) user@maquina ~/podcast-glesin$
```

**Note:** Para desativar rode o comando
```
source deactivate
```

Instale as dependencias:

```python
pip install -r requirements.txt
```

Inicie o projeto:

```python
python manage.py runserver
```

## 🛠️ Construído com

* [Python](https://www.python.org/) - Linguagem
* [Django](https://www.djangoproject.com/) - Framework Python
* [Django Rest Framework](https://www.django-rest-framework.org/) - Framework Rest para API's
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - Biblioteca de authenticação

## ✒️ Autores

* [Michel-Roney](https://github.com/Michel-Rooney/) - *Dev. Backend*
