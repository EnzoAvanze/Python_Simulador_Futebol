# Python_Simulador_Futebol

⚽ Simulador World Soccer Champs (Flet UI)
Um simulador de partidas de futebol interativo e assíncrono inspirado na mecânica de tomada de decisão do jogo World Soccer Champs. Desenvolvido em Python utilizando a biblioteca Flet para a interface gráfica e asyncio para o controle do tempo real do jogo.

🚀 Funcionalidades
Simulação em Tempo Real: Relógio regressivo de 0 a 90+ minutos simulando o ritmo de uma partida real.

Tomada de Decisão Interativa: O jogo pausa quando seu time entra no ataque, permitindo escolher a jogada:

⚽ Chutar ao Gol: Arriscado (40% de chance de gol direto), mas rápido.

🤝 Tocar a Bola: Mais trabalhado (70% de chance de acerto no passe, gerando 80% de chance de gol se concluído).

Logs de Eventos ao Vivo: Feed de texto que descreve narrações, defesas, falhas e gols à medida que acontecem.

Interface Responsiva: UI em modo escuro otimizada para layouts móbile/desktop simples.

🛠️ Tecnologias Utilizadas
Python 3.8+

Flet: Framework para construção de interfaces em Python baseadas em Flutter.

Asyncio: Para gerenciamento do loop da partida e pausa de ações do usuário sem travar a interface.


🎮 Como Jogar
Clique no botão "Iniciar Partida".

Acompanhe a cronologia e os eventos no feed.

Quando o Brasil criar uma oportunidade de ataque, a simulação irá pausar e dois botões surgirão na tela:

Escolha "Chutar ao Gol" ou "Tocar a Bola".

A partida continuará imediatamente após a sua decisão até o apito final aos 90'+.

🤝 Contribuição
Sinta-se à vontade para abrir uma issue ou enviar um pull request com melhorias, tais como:

Seleção de novos times e atributos personalizados.

Adição de cartões amarelos, vermelhos e substituições.

Efeitos sonoros e animações visuais.
