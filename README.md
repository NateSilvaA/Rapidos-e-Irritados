# 🚗 Rápidos e Irritados

## 🎮 Sobre o projeto

**Rápidos e Irritados** é uma demonstração de jogo 2D desenvolvida em **Python com Pygame**, na qual o jogador controla um carro em uma rodovia e precisa desviar do trânsito enquanto mantém uma velocidade adequada para alcançar a distância necessária para vencer.

O jogo foi desenvolvido como atividade acadêmica da disciplina **Linguagem de Programação Aplicada**, no curso de Engenharia de Software da UNINTER.

O projeto combina elementos de programação, lógica de jogos, interação com o teclado, gerenciamento de estados, colisões, efeitos visuais e reprodução de áudio.

## 🎯 Objetivo

O objetivo do jogo é percorrer uma distância determinada sem perder todas as vidas disponíveis.

### Condições de vitória

* Percorrer a distância necessária para completar a corrida.

### Condições de derrota

* Perder todas as vidas ao colidir com os veículos do trânsito.

Quanto maior a velocidade do jogador e a distância percorrida, mais intenso se torna o trânsito, aumentando o desafio durante a partida.

## 🎥 Demonstração

![Demonstração do jogo](assets/gameplay.gif)

## 🕹️ Controles

| Tecla   | Ação                            |
| ------- | ------------------------------- |
| `←` `→` | Trocar de faixa                 |
| `↑`     | Acelerar                        |
| `↓`     | Frear                           |
| `ENTER` | Iniciar / continuar / reiniciar |
| `P`     | Pausar / continuar              |
| `ESC`   | Pausar ou sair                  |

## 🛠️ Tecnologias utilizadas

* **Python**
* **Pygame**
* Programação Orientada a Objetos
* Manipulação de eventos
* Detecção de colisões
* Geração de partículas
* Reprodução de áudio
* Gerenciamento de arquivos e recursos

## ⚙️ Principais funcionalidades

### 🚘 Sistema de movimentação

O jogador pode controlar o veículo horizontalmente e ajustar sua velocidade utilizando o teclado.

### 🚦 Trânsito dinâmico

Os veículos inimigos são gerados de forma aleatória e sua quantidade aumenta conforme a velocidade do jogador e a distância percorrida.

### 💥 Sistema de colisão

As colisões entre o veículo do jogador e os veículos inimigos são detectadas utilizando `pygame.Rect`.

Após uma colisão:

* Uma vida é perdida;
* A velocidade do jogador é reduzida;
* O veículo fica temporariamente invulnerável;
* São geradas partículas para representar o impacto;
* Um efeito de tremor é aplicado à tela;
* Um efeito sonoro de colisão é reproduzido.

### ❤️ Sistema de vidas

O jogador começa com três vidas. A partida termina quando todas são perdidas.

### 🏆 Sistema de vitória e derrota

O jogo possui diferentes estados para controlar o fluxo da partida:

* Menu
* Jogo
* Pausa
* Vitória
* Derrota

Essa estrutura permite separar o comportamento e a interface de cada etapa do jogo.

### 🔊 Sistema de áudio

O projeto possui efeitos sonoros para o motor e colisões. O som do motor é sincronizado com o estado atual da partida e é interrompido quando o jogo está pausado ou finalizado.

### ✨ Efeitos visuais

O jogo possui partículas geradas durante colisões e um efeito de tremor de tela para aumentar a sensação de impacto.

## 📁 Estrutura de recursos

Os arquivos de áudio utilizados pelo jogo são armazenados na pasta `assets`.

O projeto utiliza uma função de gerenciamento de caminhos relativos para localizar os recursos, incluindo suporte para execução a partir de ambientes empacotados.

```text
Rápidos-e-Irritados/
├── assets/
│   ├── motor.wav
│   └── colisao.wav
├── main.py
└── README.md
```

## ▶️ Como executar

### 1. Instale o Python

Certifique-se de possuir o Python instalado no computador.

### 2. Instale o Pygame

```bash
pip install pygame
```

### 3. Execute o projeto

```bash
python main.py
```

O jogo será iniciado em uma janela de 800 × 600 pixels.

## 📚 Conceitos aplicados

Durante o desenvolvimento foram aplicados conceitos relacionados a:

* Programação Orientada a Objetos;
* Classes e métodos;
* Estruturas condicionais e de repetição;
* Manipulação de eventos;
* Geração de elementos aleatórios;
* Detecção de colisões;
* Gerenciamento de estados;
* Controle de entrada pelo teclado;
* Manipulação de áudio;
* Gerenciamento de recursos externos;
* Animações e efeitos visuais;
* Organização e reutilização de código.

## 🎓 Contexto acadêmico

Projeto desenvolvido para a disciplina **Linguagem de Programação Aplicada**, no curso de **Engenharia de Software — UNINTER**.

O projeto teve como objetivo aplicar conceitos de programação na construção de uma aplicação interativa utilizando Python e Pygame.

## 👨‍💻 Autor

**Natan Alves da Silva**

Estudante de Engenharia de Software interessado em desenvolvimento de software e desenvolvimento web.
