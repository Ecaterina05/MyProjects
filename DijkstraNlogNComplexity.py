import random
import heapq
from dataclasses import dataclass
from random import sample
from problem import Problem


# muchie cu cost
@dataclass
class muchie_cu_cost:
    x: int
    y: int
    cost: int


# pereche de doua valori(folosit in minheap pe post de distanta/tata)
@dataclass
class pereche:
    distanta: int
    tata: int


# nodul are o lista de muchii(ca o lista de adiacente)
@dataclass
class node:
    muchii: list


# de schimbat cu nr problemei corecte
class Problem43(Problem):
    def __init__(self):

        # constructie graf muchii random cu cost random
        nr_noduri = random.randint(5, 12)

        muchii = []
        nr = 0
        cerinta = "Se da graful:\n"
        cerinta += "nr. de noduri= " + str(nr_noduri) + "\n"
        for i in range(0, nr_noduri):
            for j in range(i + 1, nr_noduri):
                k = random.randint(0, 1)
                if (k == 1):
                    cost = random.randint(1, 15)
                    muchii.append(muchie_cu_cost(i, j, cost))
                    nr = nr + 1
                    cerinta += str(i) + " " + str(j) + " " + str(cost) + "\n"


        # cerinta += str(muchii)
        cerinta += "\nRezolvati urmatoarea cerinta:\n"
        cerinta += "\nAplicati algoritmul lui dijkstra pentru a calcula drumurile si distantele minime de la primul nod catre toate celelalte\n"
        # data memoreaza graful
        data = [muchii, nr_noduri]
        self.solution1 = ""
        super().__init__(cerinta, data)

    def solve(self):
        # Creare lista de adiacenta(asa se rezolva dijkstra optim)
        noduri = []
        # redimensioneaza noduri[] la n
        for i in range(self.data[1]):
            noduri.append(node([]))
        # face lista de adiacenta
        for e in self.data[0]:
            noduri[e.x].muchii.append(e)
            noduri[e.y].muchii.append(e)

        # Folosim un vector de perechi pentru rezultat
        # initial distanta catre noduri e infinit(aici am pus 9999 pentru ca nu poate sa ajunga atat de mare(deci e ca un infinit))
        answer = []
        for i in range(self.data[1]):
            answer.append(pereche(9999, -1))
        # nodul de start e la distanta 0 si este propriul parinte
        answer[0].distanta = 0
        answer[0].parinte = -1
        # Vector de marcaj pentru noduri extrase, initial nu am extras pe nimeni
        extras = [False] * self.data[1]
        # min heap pentru a extrage intotdeauna nodul cel mai apropiat
        minheap = []
        # adaugare nod initial in minheap(nodul 0,distanta 0)
        heapq.heappush(minheap, (0, 0))
        # i e numarul de noduri extrase(ne oprim dupa ce le scoatem pe toate(n))

        while len(minheap) > 0:
            # Scoate nodul cu distanta minima(acum nod calculat corect)
            nod = heapq.heappop(minheap)

            # verifica sa nu fi fost deja extras(in minheap putem sa avem dubluri)
            if not (extras[nod[1]]):
                # Marcheaza nodul ca extras si creste nr de noduri extrase
                extras[nod[1]] = True

                # Am extras un nod cu distanta "infinit", inseamna ca toate care au mai ramas sunt infinit => am terminat
                if answer[nod[1]].distanta == 9999:
                    break
                # Relaxeaza toate muchiile nodului ales
                for e in noduri[nod[1]].muchii:
                    # Relaxeaza daca nodul catre care duce muchia inca nu a fost ales si daca noua distanta e mai mica decat cea deja calculata
                    if not (extras[e.y]) and (answer[e.y].distanta > answer[e.x].distanta + e.cost):
                        # Seteaza noua distanta
                        answer[e.y].distanta = answer[e.x].distanta + e.cost
                        # Seteaza noul tata
                        answer[e.y].tata = nod[1]
                        # Pune nodul in minheap(de aici pot aparea dubluri, el poate sa fie deja acolo, de aia verificam extras[])
                        heapq.heappush(minheap, (answer[e.y].distanta, e.y))
        # am terminat, afisam distantele si tatii


        self.solution1 = str(answer)
        # solution = str(sir)
        cerinta = self.statement
        return self.solution1

#test_probl = Problem43()
#[print(x) for x in test_probl.solve()]