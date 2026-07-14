# Sistema de Inventário de Ativos e Vulnerabilidades - Cibersegurança (UFU)

Este projeto consiste em uma aplicação de Linha de Comando (CLI) robusta desenvolvida em Python para o gerenciamento centralizado de ativos de rede (equipamentos) e o mapeamento de suas respectivas vulnerabilidades de segurança. 

A solução foi reestruturada integralmente utilizando o paradigma de **Orientação a Objetos Avançada** (aplicando encapsulamento rigoroso, herança, polimorfismo e injeção de dependência) e é distribuída de forma totalmente isolada e segura por meio de **conteinerização com Docker**.

---

## 🏗️ Arquitetura e Padrões de Projeto Aplicados

* **Encapsulamento e Validação:** Atributos protegidos por decorators `@property` e `@setter` com validações em tempo de execução para garantir a integridade dos dados inseridos.
* **Polimorfismo e Injeção de Dependência:** O gerenciamento do ciclo de vida dos dados usa uma interface abstrata (`PersistenciaInventario`), permitindo que a aplicação salve em arquivos JSON ou seja facilmente migrada para bancos de dados SQL sem alterar as regras de negócio.
* **Performance ($O(1)$):** Utilização de Tabelas Hash (dicionários Python) para indexação dos ativos, garantindo que buscas e validações de ID duplicado ocorram instantaneamente, independentemente do volume de dados.
* **Segurança de Infraestrutura (Hardening):** O ambiente do Docker aplica patches de atualização automatizados no sistema base durante a compilação da imagem para mitigar vulnerabilidades de pacotes herdados.

---

## 🛠️ Requisitos e Pré-requisitos

A aplicação foi projetada para rodar sem dependências de pacotes externos, utilizando apenas a biblioteca padrão do Python 3 (`json`, `os`, `sys`, `abc`).

* **Necessário para execução:** Ter o **Docker** instalado e ativo na máquina.

---

## 🐋 Como Executar a Aplicação com Docker

Abra o terminal do seu sistema operacional (Terminal no Linux, Prompt de Comando ou PowerShell no Windows) dentro da pasta raiz do projeto (`Cyber_ativos`) e siga os passos abaixo:

### Passo 1: Construir a Imagem Docker
Este comando compila a aplicação e aplica todas as atualizações de segurança internas:
```bash
docker build -t inventario-cyber-seguranca .

### Passo 2: no ambiente linux (Executar o Container (Com Persistência de Dados)
Este comando roda a imagem utilizando parâmetros -it porque será necessário interação  do usuário com a CLI e será adicionada um comando para salvar o arquivo de texto no repositório.

docker run -it --name app-inventario -v $(pwd)/inventario.json:/app/inventario.json inventario-cyber-seguranca

### Passo 2: no ambiente Windows (Executar o Container (Com Persistência de Dados)
no PowerShell
docker run -it --name app-inventario -v ${PWD}/inventario.json:/app/inventario.json inventario-cyber-seguranca

no Prompt de Comando - CMD
docker run -it --name app-inventario -v %cd%/inventario.json:/app/inventario.json inventario-cyber-seguranca