# Vector Race

## Fomulação do problema
- Problema de pesquisa
- Estado **Inicial**: P
- Estado **Objetivo**: F
- Operadores:
  - Pré-Condições: 
    - O carro pode acelerar {-1, 0, 1} unidades em cada direção (linha e coluna).
    - O carro **pode sair da pista**: terá que voltar para a posição anterior com velocidade **nula**.
    - Custo de deslocação do carro de uma posição _x_ para uma posição _y_: **1 unidade**.
      - Fora dos limites da pista: **25 unidades**.


- Custo da solução: c(s, a, s’)
  - **s** representa o estado atual.
  - **a** equivale à ação que foi executada pelo agente para atingir o estado **s'**.