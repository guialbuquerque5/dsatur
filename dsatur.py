import time
import sys

G = [
        [1, 2, 3, 4, 8],#1
        [0, 2, 3, 8, 9],#2
        [0, 4, 1],#3
        [0, 1, 4, 6],#4
        [0, 2, 3, 6, 5, 7],#5
        [4, 7, 8],#6
        [3, 4, 8, 9],#7
        [5, 8, 4],#8
        [0, 7, 5, 6, 1, 9],#9
        [6, 1, 8],#10
    ]
        
def build_graph(filename):
    g = []
    with open(filename) as f:
        rows = f.read().split('\n')[:-1]
        for row in rows:
            g.append([int(x)-1 for x in row.split(',')[1:]])
    return g

if len(sys.argv) == 1:
    print('Error! To use this script you should pass the csv file name as argument!')
    print('ex: python dsatur.py grafo.csv')
    sys.exit()

G = build_graph(sys.argv[1])

n_v = len(G)
V = [i for i in range(n_v)]
colors = [None] * n_v

order = lambda (v,g): len(g[v])

def d_sat(v):
    c = set()
    for _v in G[v]:
        c.add(colors[_v])
    return len(c) - 1

def max_d_sat(v_list):
    r = {v: d_sat(v) for v in v_list}
    max_sat = 0
    for v in r:
       max_sat =r[v] if r[v] > max_sat else max_sat
    r = [v for v in r if r[v] == max_sat]
    return r
    
def max_order(V,g):
    bigger = [V[0],0]
    for _v in V:
        bigger = [_v, order((_v, g))] if order((_v, g)) > bigger[1] else bigger
    return bigger[0]

def next(v_list, g):
    if len(v_list) == 0:
        return None
    return max_order(max_d_sat(v_list),g)

def remove_rel(v, g):
    t =  g
    for e in t:
        if v in t[e]:
            t[e].remove(v)
    return t

def hash_graph(g):
    return { i: g[i] for i in range(len(g)) }
    
def min_color(v):
    possible_colors = { x: None for x in range(5)}#no more than 5 different colors
    c = [colors[_v] for _v in G[v]]
    for _c in c:
        possible_colors.update({_c : 1})
    for _c in possible_colors:
        if possible_colors[_c] is None:
            return _c
    return 0

def dsatur(V, g):
    _g = hash_graph(list(list(i) for i in g))
    _next = max_order(V,_g)
    colors[_next] = 0
    print(_next, 'cor: 0')
    V.remove(_next) 
    _next = next([_v for _v in _g[_next] if colors[_v] is None], _g)
    _g = remove_rel(_next, _g)
    while len(V) > 0:
        print(_next, 'cor: ' + str(min_color(_next)) ) 
        colors[_next] = min_color(_next)
        V.remove(_next)
        _next = next( [_v for _v in V if colors[_v] is None], _g)
        _g = remove_rel(_next, _g)

start_time = time.time()
dsatur(V,G)
elapsed_time = time.time() - start_time

print('Result colors:')
print(colors)

print('Time execution: %f s' % elapsed_time)
