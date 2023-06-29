# VectorRace
O VectorRace é um jogo de simulação de uma corrida de carros, que possui um conjunto de movimentos e normas associadas.  A deslocação do carro no VectorRace é simples, as ações que são efetuadas pelo veículo são equivalentes a um conjunto de acelereações. Num determinado instante da corrida, o carro pode acelerar **-1, 0** ou **1** unidades em cada direção (**linha** e **coluna**).

A figura seguinte ilustra a UI da aplicação desenvolvida.

<p align="center">
  <img width="450" height="450" src="https://github.com/joseluisgomes/VectorRace/assets/70901488/f2c682cf-28bb-468f-836d-6617dd8e7c83">
</p>

## Movimento do carro
O movimento de um carro no VectorRace é simples, qualquer movimento efetuado pelo veículo resultará numa variação do seu conjunto de acelerações.

Num determinado instante, o carro poderá acelerar -1, 0 ou 1 unidades em cada direção (linha e coluna). O carro movimenta-se ao longo do plano **cartesiano**, isto é, desloca-se segundo o eixo (positivo) das abcissas e segundo o eixo das oordenadas.

Considerando a notação **l**, que representa a linha e **c** a coluna para os vetores, num determinado instante, o carro pode acelerar -1 ,0 ou 1 unidades em cada direção (linha e coluna). Consequentemente, para cada uma das direções o conjunto de acelerações possíveis é Acel = {-1, 0, +1}, com a =(al,ac) a representar a aceleração de um carro nas duas direções num determinado instante.

Tendo em conta que **p** como tuplo que indica a posição de um carro numa determinada jogada j ($p_j = (p_l, p_c)$), e **v** o tuplo que indica a velocidade do carro nessa jogada ($v_j = (v_l,v_c)$) , na seguinte jogada o carro estará na posição:
$$\left(p_l^{j+1} \right) = \left(p_l^{j} + v_l^j + a_l \right)$$
$$\left(p_c^{j+1} \right) = \left(p_c^{j} + v_c^j + a_c \right)$$

A velocidade do carro num determinado instante é calculada:
$$\left(v_l^{j+1} \right) = \left(v_l^{j} + a_l \right)$$
$$\left(v_c^{j+1} \right) = \left(v_c^j + a_c \right)$$

### Custos relativos à deslocação do veículo
Sendo uma simulação de corrida de carros, existe a probabilidade do carro sair fora dos limites da pista. Caso ocorra a situação citada, o carro terá que voltar para a posição anterior com
velocidade nula. 

Para uma determinada jogada, cada deslocação do carro de uma certa posição para outra, terá o custo de 1 unidade e caso saia fora dos limites da pista, o custo aplicado será de **25** unidades.

## Circuito gerado
O circuito gerado pelo grupo encontra-se representado pela figura abaixo.

<p align="center">
  <img width="500" height="150" src="https://github.com/joseluisgomes/VectorRace/assets/70901488/c42e6ebc-9e86-426b-a60b-dac0453c87fb">
</p>

Neste exemplo é apresentado uma pista de 20 colunas e 7 linhas, onde o ‘-‘ representa a **pista**, o ‘X’ representa o **obstáculo/fora** da pista, o P a posição **inicial** e o F as posições **finais** (meta).

## Exemplo de execução do programa
![execucao](https://user-images.githubusercontent.com/70901488/205396287-bb8b9a63-6b72-47e9-a33f-fc971e1ddbd7.png)
