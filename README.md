# 📚 PinyinCHN — Conversor Didático Chinês ⇄ Pinyin ⇄ PT-BR

[![Licença](https://img.shields.io/badge/Licença-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/Interface-Tkinter-2C3E50.svg)](https://docs.python.org/3/library/tkinter.html)

Uma ferramenta **didática** para aprendizado do idioma chinês que exibe simultaneamente:

> **Objetivo**: Transformar a experiência de estudo do chinês em algo visualmente claro, imersivo e prático. Indo muito além de um tradutor convencional.

---

## Motivo Base do Projeto?

Nos sistemas tradicionais (como o IME do Windows), digitamos **pinyin** para obter **ideogramas**

Entretanto... **quem está aprendendo chinês** enfrenta o problema típico de tentar saber a pronuncia e entonações certas junto com a tradução. 
Ao vê os ideogramas em livros, filmes ou jogos e precisa descobrir rapidamente o significado dela.
E esse programa está sendo focado para resolução de junção de tradução + pinyin + ideograma, tudo em um só lugar, de forma rápida e prática.


***Exemplo simples***

1. Qual o ideograma?  (ideograma)  (`我的哥哥`)
2. Como se pronuncia? (pinyin entonação)     (`wǒ de gēgē`)
3. Como se pronuncia? (pinyin s/ entonação)     (`wo de gege`)
4. Qual a tradução?   (PT-BR)      (`meu irmão mais velho`)

Este **App** penso em preencher essa lacuna com uma interface pensada **exclusivamente para estudantes e para uso didático**.

---

## Até o momento...
                                                
✍️ Conversão Hanzi → Pinyin
- Exibe entonações (`wǒ de gēgē`)
- Versão sem entonações (`wo de gege`)
- Tradução para português (`PT-BR`)

📡 Diagnóstico de Conexão
- Verificação automática de internet

🇨🇳 Renderização de caracteres
- Suporte completo a UTF-8 para ideogramas chineses

💻 Interface gráfica Tkinter
- App desktop leve e responsivo, para prototipagem inicial de modelo

📋 Cópia para área de transferência
- Um clique para salvar frases estudadas e podendo ser copiadas para qualquer lugar que você queira.

## 📁 Estrutura do Projeto
PinyinCHN/
├── app_pinyin.py # Interface gráfica Tkinter
├── core/
│ ├── init.py # Inicialização do módulo
│ ├── conversor.py # Lógica de conversão Hanzi → Pinyin
│ └── tradutor.py # Lógica de tradução Chinês → PT-BR
├── requirements.txt # Dependências Python
├── README.md # Este arquivo
└── LICENSE # Licença MIT

## ✨ **Vantagem da modularização**: 
A lógica em `core/` pode ser reutilizada em APIs web, apps mobile ou scripts independentes — sem depender da interface Tkinter.


## 🚀 Como Usar

### 1. Clonar o repositório
# bash
git clone https://github.com/seu-usuario/PinyinCHN.git
cd PinyinCHN

### 2. Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # Linux/Mac

### 3. Instalar dependências
pip install -r requirements.txt

### 4. Executar o app
python app_pinyin.py

## Usar a ferramenta
- Digite texto em chinês (我的哥哥)
- Clique em 🔄 Converter e Traduzir ou pressione Enter
- Veja o resultado com pinyin + tradução
- Clique em 📋 Copiar resultado para salvar
- 🔍 Dica: Se a tradução falhar, clique no botão 🔧 Diagnóstico para identificar o problema (conexão, firewall, limite de requisições, etc.)



#
[![Licença](https://img.shields.io/badge/Licença-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/Interface-Tkinter-2C3E50.svg)](https://docs.python.org/3/library/tkinter.html)
