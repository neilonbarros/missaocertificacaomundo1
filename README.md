# missaocertificacaomundo1

## linux

com python instalado na maquina
no exemplo vou usar o 3.10

acessar o diretorio do projeto
```
$ cd /meu/diretorio/missaocertificacaomundo1
```

criar `.venv` onde ficarão armezados todas as dependencias necessárias para o projeto, sem afetar o python main
```
$ python3.10 -m venv .venv
```

ativar nosso python do projeto (`.venv`), já estando dentro do projeto `/meu/diretorio/missaocertificacaomundo1`
```
$ source .ven/bin/activate
```

o terminal passará a ficar assim:
```
(.venv)$
```

instalação e upgrade do `pip`, responsável por instalar e gerenciar dependência
```
(.venv)$ pip install --upgrade pip
```

instalação da dependência `poetry`, ela é que vai fazer todo o trabalho penoso de usar o `pip`:
```
(.venv)$ pip install poetry
```

agora faremos a instalações de todas as dependências necessárias para o projeto
```
(.venv)$ poetry install
```

agora que todas as dependências foram instaladas, faremos a configuração do projeto
```
(.venv)$ python manage.py makemigrations
(.venv)$ python manage.py migrate
```

e por fim iniciaremos o projeto
```
(.venv)$ python manage.py runserver
```

se a mensagem abaixo for apresentada, isso significa que iniciamos o projeto com sucesso
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 13, 2023 - 01:20:21
Django version 4.2.3, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

agora basta acessar [http://127.0.0.1:8000/](http://127.0.0.1:8000/) ou [http://localhost:8000/](http://localhost:8000/)