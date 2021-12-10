# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 23:24:36 2021

@author: elchaabi
"""
import random
import copy
import csv
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns 
from random import randint
sns.set()

"Tracer le graphe"
def graphe(chemin,distances):
    nbr_ville = len(chemin)
    G = nx.Graph()
    list_dist = list()
    for i in range(0,nbr_ville-1):
        list_dist.append(distances[chemin[i]-1][chemin[i+1]-1])
    list_dist.append(distances[chemin[0]-1][chemin[-1]-1])
    for i in range(1,nbr_ville+1):
        x = randint(1,10)
        y = randint(1,10)
        G.add_node(chemin[i-1],pos=(x,y))
    for i in range(0,nbr_ville-1):
        G.add_edge(chemin[i],chemin[i+1],weight=list_dist[i])
    G.add_edge(chemin[-1],chemin[0],weight=list_dist[-1]) 
    weight = nx.get_edge_attributes(G,'weight')
    pos = nx.get_node_attributes(G,'pos')
    plt.figure()
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edge_labels(G,pos,weight)

"lire l'inctance à partire du fichier excel"
def lecture_instance(f):
    tour=[]
    with open(f+".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        for row in csv_reader:
            tour.append(row)
        for n, i in enumerate(tour):
            for k, j in enumerate(i):
                tour[n][k] = int(j)
    return tour

"retourne une liste d'indices des villes"          
def indices_villes(graph):
    n=len(graph)
    l=list(range(n))
    return l

"retourne une chemin aléatoire"
def sequence_ville_aléatoire(graph):
    n=len(graph)
    list_ville=list()
    for i in range(n):
        list_ville.append(i)
    list_ville.pop(0)
    random.shuffle(list_ville)
    return [0]+list_ville+[0]

"génére une solution initiale"
def solution_initiale(graph):
    l=sequence_ville_aléatoire(graph)
    n=len(l)
    cout_initiale=0
    for i in range(n-1):
        cout_initiale+=graph[l[i]][l[i+1]]
    return cout_initiale,l

"structure voisinage 1 : permutation de 2 élts"
def permu_2_elts(l):
    n=len(l)
    for i in range(1,n) :
        for j in range(i+1,n):
            copie=copy.copy(l)
            copie[i],copie[j]=copie[j],copie[i]
            yield copie+[0]

"recherche locale dans la structure de voisinage 1"
def local_search_permute(graph):
    l=indices_villes(graph)
    for seq in permu_2_elts(l):
        n=len(seq)
        cout_seq=0
        for i in range(n-1):
            cout_seq+=graph[seq[i]][seq[i+1]]
        yield cout_seq,seq
 
"structure voisinage 2 : 2-opt"        
def deux_opt(chemin):
    chemin_inverse = list()
    for i in range(len(chemin)-1,-1,-1):
        chemin_inverse.append(chemin[i])
    for i in range(1, len(chemin)-2):
        for j in range(i+1, len(chemin)):
                    if j-i == 1: continue 
                    nouveau_chemin = chemin[:]
                    nouveau_chemin[i:j] = chemin[j-1:i-1:-1]
                    if nouveau_chemin !=chemin_inverse:
                        yield nouveau_chemin
                        
"recherche locale dans la structure de voisinage 2"                      
def local_search_deux_opt(graph):
    l=indices_villes(graph)
    l+=[0]
    for seq in deux_opt(l):
        n=len(seq)
        cout_seq=0
        for i in range(n-1):
            cout_seq+=graph[seq[i]][seq[i+1]]
        yield cout_seq,seq

"algorithme du VNS"
def VNS(graph):
    cout_min,chemin_min=solution_initiale(graph)
    for cout_seq,seq in local_search_deux_opt(graph):
        if cout_min > cout_seq :
            cout_min=cout_seq
            chemin_min=seq
    for cout_seq,seq in local_search_permute(graph):
        if cout_min > cout_seq :
            cout_min=cout_seq
            chemin_min=seq
    chemin_inverse=chemin_min[::-1]
    return cout_min,chemin_min,chemin_inverse

"retourne les combinaisons possible d une liste"
def comb(L):
    ville=list(L)
    nb=len(ville)-1 #Nombre de combinaisons
    if nb == 0 :
        return print(L)
    else:
        for i in range(1, nb + 1) :
            S=[ville[0]]
            S.append(ville[i])
            yield S

"permute le 1 ere élt avec un élt n"            
def permutations(L,n):
    ville=list(L)
    nb=len(ville)
    for i in range(1,nb) :
        if n == ville[i] :
            ville[0],ville[i] = ville[i], ville[0]
    return ville

"la fct objective "
def TSP_DYNAMIC(graph):
    nb = len(graph)
    indices_villes = []
    tour = [0, ]
    min = np.inf
    suivant=0
    cout_min=0
    for i in range(nb):
        indices_villes.append(i)
    while len(indices_villes) !=1:
        min = np.inf
        for j in comb(indices_villes):
            dist = graph[j[0]][j[1]]
            if min >= dist:
                min = dist
                suivant=j[1]
        cout_min += min
        tour.append(suivant)
        del indices_villes[0]
        indices_villes=permutations(indices_villes,suivant)
    cout_min+=graph[suivant][0]
    tour.append(0)
    tour_invers= tour[::-1]
    return tour_invers, tour,cout_min

"Format de la solution et la réprésentation graphique"
def TSP_SOL(graph,k):
    if k==1:
        ch2,ch1,cout=TSP_DYNAMIC(graph)
    else :
        cout,ch1,ch2=VNS(graph)    
    print("Le cout minimum est : ", cout)
    print("Le premier chemin est : ",ch1)
    print("Le deuxième chemin est : ",ch2)
    graphe(ch1,graph)

"Le menu"
def Menu():
    print("1.Résolution par la programmation dynamique")
    print("2.Résolution par la métaheuristique")
    print("0.Exit")
    k=int(input("Entrez votre choix : "))
    if k==1 :
        print("****** La programmation dynamique ******")
        print("1.instance_1")
        print("2.instance_2")
        print("3.instance_3")
        print("4.Menu principale")
        i=int(input("Entrez votre choix : "))
        if i==1 :
            f="instance_1"
            Y=lecture_instance(f)
            TSP_SOL(Y,k)
        elif i==2 :
            f="instance_2"
            Y=lecture_instance(f)
            TSP_SOL(Y,k)
        elif i==3 :
             f="instance_3"
             Y=lecture_instance(f)
             TSP_SOL(Y,k)
        elif i==4 :
            return Menu()
        else :
            print("Choix invalide")
    elif k==2 :
        print("****** La métaheuristique ******")
        print("1.instance_1")
        print("2.instance_2")
        print("3.instance_3")
        print("4.Menu principale")
        i = int(input("Entrez votre choix : "))
        if i == 1:
            f="instance_1"
            Y=lecture_instance(f)
            TSP_SOL(Y,k)
        elif i == 2:
            f="instance_2"
            Y=lecture_instance(f)
            TSP_SOL(Y,k)
        elif i == 3:
            f="instance_3"
            Y=lecture_instance(f)
            TSP_SOL(Y,k)
        elif i==4 :
            return Menu()
        else:
            print("Choix invalide")
    elif k==0 :
        print("Merci pour l'utilisation du programme")
    else:
        print("Choix invalide")

Menu()