# Scripts de Segurança em Python

Este repositório contém scripts Python focados em práticas e demonstrações de segurança.

## Como Executar

Inicialmente instale UV (manager de dependencias)

```bash
pip install uv
uv sync
````

Cada arquivo `.py` neste repositório pode ser executado individualmente usando Python:

```bash
python nome_do_script.py
```

Todo Script ira informar as necessidades de Entrada de dados conforme necessario
Substitua `nome_do_script.py` pelo nome do script específico que você deseja executar.

### Exercicios

#### Cifra de Ceaser

```bash
python Ceasarcifra.py
```

é requisitado a mensagem e o quanto de shift é usado

#### Cifra de Feistel

```bash
python Feistelcifra.py
```

é requisitada a mensagem

#### RBAC

```bash
python RBAC.py
```

abre um servidor flask em [http://127.0.0.1:5000](http://127.0.0.1:5000)
tem um menu superior com os diferentes tipos de usuario e suas ações possiveis
é reiniciado depois de cada execução (não tem um arquivo de memoria permamente)

#### Diffie-Hellman

```bash
python Diffie-Hellman.py
```

é dada a opção de usar os valores padroes ou usar outros
para fazer modificado usar a tecla "C"
para manter os padrões P

### Requisitos

- Python 3.13 instalado
- Quaisquer dependências adicionais específicas para cada script
