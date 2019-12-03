import statistics
import time
import sys
import csv

#Constroi o grafo a partir da csv 
def build_graph(filename):
    g = []
    with open(filename) as f:
        rows = f.read().split('\n')[:-1]
        for row in rows:
            g.append([int(x)-1 for x in row.split(',')[1:]])
    return g

#Verifica se o argumento do programa tah certo
if len(sys.argv) == 1:
    print('Error! To use this script you should pass the csv filename as argument!')
    print('ex: python dsatur.py grafo.csv')
    sys.exit()

G = build_graph(sys.argv[1]) #build graph here

#Numero de vertices
n_v = len(G)
#Lista de vertices
V = [i for i in range(n_v)]
#Lista de cores
colors = [None] * n_v
#funcao que retorna o grau do vertice
order = lambda v: len(v[1][v[0]])

#Funcao que retorna o grau de saturacao do vertice
def d_sat(v):
    c = set()
    for _v in G[v]:
        c.add(colors[_v])
    return len(c) - 1

#Retorna o grau do grafo
def max_d_sat(v_list):
    r = {v: d_sat(v) for v in v_list}
    max_sat = 0
    for v in r:
       max_sat =r[v] if r[v] > max_sat else max_sat
    r = [v for v in r if r[v] == max_sat]
    return r

#Ordena o grafo com base no grau
def max_order(v_list,g):
    bigger = [v_list[0],0]
    for _v in v_list:
        bigger = [_v, order([_v, g])] if order([_v, g]) > bigger[1] else bigger
    return bigger[0]

#Retorna o proximo vertice a ser colorido
def next(v_list, g):
    if len(v_list) == 0:
        return None
    return max_order(max_d_sat(v_list),g)

#Remove as arestas de um vertice
def remove_rel(v, g):
    for e in g:
        if v in g[e]:
            g[e].remove(v)
    return g

#transforma de lista para hash(dict)
def hash_graph(g):
    return { i: g[i] for i in range(len(g)) }

#retorna a cor minima do vertice
def min_color(v):
    possible_colors = { x: None for x in range(5)}#no more than 5 different colors
    c = [colors[_v] for _v in G[v]]
    for _c in c:
        possible_colors.update({_c : 1})
    for _c in possible_colors:
        if possible_colors[_c] is None:
            return _c
    return 0

#O algoritmo em si, que retorna um array de cores onde cada index representa
#um vertice, comecando pelo index 1 ao inves do 0
def dsatur(V, g):
    #_g eh o grafo
    _g = hash_graph(list(list(i) for i in g))
    #_next eh o vertice com maior grau de saturacao
    _next = max_order(V,_g)
    #a cor do primeiro eh 0
    colors[_next] = 0
    print(_next, 'cor: 0')
    #remove o primeiro da lista de vertices
    V.remove(_next) 
    #escolhe o proximo vertice
    _next = next([_v for _v in _g[_next] if colors[_v] is None], _g)
    #remove ele do grafo
    _g = remove_rel(_next, _g)
    while len(V) > 0:
        print(_next, 'cor: ' + str(min_color(_next)) ) 
        #define a cor do vertice como a menor cor possivel
        colors[_next] = min_color(_next)
        #Remove o vertice da lista de vertices
        V.remove(_next)
        #escolhe o proximo vertice
        _next = next( [_v for _v in V if colors[_v] is None], _g)
        #remove ele do grafo
        _g = remove_rel(_next, _g)
    #retorna o array de cores
    return colors

#conta o tempo de execucao
start_time = time.time()
#roda o algoritmo
result_colors = dsatur(V,G)
#conta o tempo de execucao
elapsed_time = time.time() - start_time
#printa o array resultante
print('Result colors:')
print(result_colors)

print('Time execution: %f s' % elapsed_time)

#Escreve no .csv a resposta do programa ao grafo,
#com cada row correspondendo a um par Vertice, Cor

#Abre o arquivo .csv
f = open("tabelaResposta.csv", "w")
try:
    #Cria o writer
    writer = csv.writer(f)
    #Para cada vertice do grafo
    for i in range(n_v):
	#Escreve uma linha com Vertice, Cor
        #Eh usado i+1 pq a identificacao dos vertices comeca em 1 ao inves de 0
        writer.writerow( (i+1, result_colors[i]) )

finally:
    #Fecha o arquivo .csv
    f.close()

#Ve os graus de cada vertice
graus = {i: len(G[i]) for i in range(len(G))}

#Procura por grau maximo, minimo, medio e desvio padrao dos graus, alem de numero de cores
#graus
minimo = 2147483646
maximo = 0
medio = 0
desvio_padrao = 0
#max de cores
max_cores = -1
for i in range( len(graus) ):
    if result_colors[i] > max_cores:
        max_cores = result_colors[i] 
    if graus[i] < minimo:
        minimo = graus[i]
    if graus[i] > maximo:
        maximo = graus[i]
    medio += graus[i]
medio /= len(graus)

#imprime os valores
print("Minimo: " + str(minimo) + " Maximo: " + str(maximo) + " Medio: " + str(medio) + " Desvio Padrao: " + str(statistics.pstdev(graus)) )
print("Numero de vertices: " + str( len(graus) ) + " Numero de cores: " + str(max_cores +1) )

