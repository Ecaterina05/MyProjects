import copy
import time
import os

import numpy as np


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join(linie) + "\n"
        return sir

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join(linie) + "\n"
        return sir


def cautaPozElemMatr(matr, elemCautat):
    for i, linie in enumerate(matr):
        for j, elem in enumerate(linie):
            if elem == elemCautat:
                return i, j
    return -1


def testeaza_scop2(infoNod):
    i = 0
    j = len(infoNod[0]) - 1
    nr = len(infoNod[0])
    while i != j:
        coli = [val[i] for val in infoNod]
        colj = [val[j] for val in infoNod]
        for k in range(nr):
            if coli[k] != colj[k]:
                return False
        i = i + 1
        j = j - 1

    return True

class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        f = open(nume_fisier, "r")
        textFisier = f.read()
        listaSiruriLinii = textFisier.strip().split("\n")  # ["0 3 2","1 2 4","4 3 1"]

        self.start = []
        for linie in listaSiruriLinii:
            self.start.append(linie.strip().split(" "))

        print(self.start)

    def testeaza_scop(self, nodCurent):
        infoNod = copy.deepcopy(nodCurent.info)
        i = 0
        j = len(infoNod[0]) - 1
        nr = len(infoNod[0])
        while i != j:
            coli = [val[i] for val in infoNod]
            colj = [val[j] for val in infoNod]
            for k in range(nr):
                if coli[k] != colj[k]:
                    return False
            i = i + 1
            j = j - 1

        return True

    def existentaSolutie(self, infoNod):
        nr = len(infoNod[0])
        M = (nr * nr - 1) // 2
        frecventa = [0] * (M + 1)
        for i in range(nr):
            for j in range(nr):

                if infoNod[i][j] == '0':
                    continue

                for k in range(1, M + 1):
                    if int(infoNod[i][j]) == k:
                        frecventa[k] = frecventa[k] + 1

        for l in range(1, M + 1):
            if frecventa[l] > 2:
                return False

        return True

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):

        listaSuccesori = []
        # lista de directii pentru sus, jos, stanga, dreapta, diagonala stanga sus, diagonala stanga jos, diagonala dreapta sus, diagonala dreapta jos
        directii = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, 1], [1, -1], [-1, -1], [1, 1]]

        numarNod = copy.deepcopy(nodCurent.info)
        nr = len(numarNod)

        # caut gol
        linieGol, coloanaGol = cautaPozElemMatr(nodCurent.info, '0')
        for dl, dc in directii:

            linieVecin = linieGol + dl
            coloanaVecin = coloanaGol + dc
            try:
                if linieVecin < 0 or coloanaVecin < 0 or linieVecin > nr - 1 or coloanaVecin > nr - 1:
                    continue
                infoNodNou = copy.deepcopy(nodCurent.info)
                infoNodNou[linieGol][coloanaGol] = infoNodNou[linieVecin][coloanaVecin]
                valoareLinie = linieVecin
                infoNodNou[linieVecin][coloanaVecin] = '0'

                # print(infoNodNou)
                pare = 0
                impare = 0

                # numar cati vecini pari si cati impari are ( nu vrem sa il punem pe 0 la socoteala )
                for dl2, dc2 in directii:
                    i = linieGol + dl2
                    j = coloanaGol + dc2
                    try:
                        if i < 0 or j < 0 or i > nr - 1 or j > nr - 1:
                            continue
                        if int(infoNodNou[i][j]) % 2 == 0 and infoNodNou[i][j] != '0':
                            pare = pare + 1
                        elif int(infoNodNou[i][j]) % 2 != 0 and infoNodNou[i][j] != '0':
                            impare = impare + 1

                    except IndexError:
                        pass

                #print(pare)
                # print("Impare")
                #print(impare)

                elementeDeSus = []
                # verific daca exista un element in vecinii de sus de paritate diferita care sa fie mai mare decat elementul mutat si in acelasi timp,
                # daca avem vecini de paritate diferita de paritatea elementului mai multi decat vecinii cu aceeasi paritate ca a elementului mutat
                if linieGol == 0:
                    elementeDeSus = []

                elif coloanaGol == 0 and linieGol > 0:
                    if int(infoNodNou[linieGol - 1][coloanaGol]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol]))
                    if int(infoNodNou[linieGol - 1][coloanaGol + 1]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol + 1]))

                elif coloanaGol == len(infoNodNou[0]) - 1 and linieGol > 0:
                    if int(infoNodNou[linieGol - 1][coloanaGol]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol]))
                    if int(infoNodNou[linieGol - 1][coloanaGol - 1]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol - 1]))

                else:
                    if int(infoNodNou[linieGol - 1][coloanaGol]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol]))
                    if int(infoNodNou[linieGol - 1][coloanaGol - 1]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol - 1]))
                    if int(infoNodNou[linieGol - 1][coloanaGol + 1]) != 0:
                        elementeDeSus.append(int(infoNodNou[linieGol - 1][coloanaGol + 1]))

                #print(elementeDeSus)

                ok = 1
                for element in elementeDeSus:
                    if int(infoNodNou[linieGol][coloanaGol]) % 2 == 0 and impare > pare and \
                            element > int(infoNodNou[linieGol][coloanaGol]) and element % 2 != 0:
                        ok = 0
                        #print("aici1")
                    elif int(infoNodNou[linieGol][coloanaGol]) % 2 != 0 and pare > impare and \
                            element > int(infoNodNou[linieGol][coloanaGol]) and element % 2 == 0:
                        ok = 0
                        #print("aici2")


                if ok == 1:
                    infoNodCorect = copy.deepcopy(infoNodNou)
                    #print("InfoNodCorect")
                    #print(infoNodCorect)

                    if not nodCurent.contineInDrum(infoNodCorect):
                        listaSuccesori.append(NodParcurgere(infoNodCorect, nodCurent, nodCurent.g + valoareLinie +
                                                            int(infoNodCorect[linieGol][coloanaGol]),
                                                            self.calculeaza_h(infoNodCorect, tip_euristica)))
            except IndexError:
                pass
        # print(listaSuccesori)
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if testeaza_scop2(infoNod) is False:
                return 1
            return 0

        # in euristica urmatoare voi numara cate placute NU sunt la locul lor
        if tip_euristica == "euristica nebanala1":
            hTotal = 0
            mijloc = len(infoNod[0]) // 2
            for cPlacutaC in range(mijloc):
                for lPlacutaC in range(len(infoNod[cPlacutaC])):
                    if infoNod[lPlacutaC][cPlacutaC] == '0':
                        continue
                    nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])
                    # vedem ce avem pe placuta de pe pozitia simetrica
                    nrPlacutaSim = int(infoNod[lPlacutaC][2 * mijloc - cPlacutaC])
                    if nrPlacuta != nrPlacutaSim:
                        hTotal += 1
            return hTotal

        # in euristica urmatoare voi numara cati pasi face fiecare dublura de placuta pentru a ajunge
        # pe pozitia simetrica
        if tip_euristica == "euristica nebanala2":
            hTotal = 0
            nr = len(infoNod[0])
            M = (nr * nr - 1) // 2
            verificareP = [0] * (M+1)
            mijloc = nr // 2

            for cPlacutaC in range(mijloc):
                for lPlacutaC in range(len(infoNod[cPlacutaC])):
                    if infoNod[lPlacutaC][cPlacutaC] == '0':
                        continue

                    nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])

                    if verificareP[nrPlacuta] == 0:
                        verificareP[nrPlacuta] += 1

                    if verificareP[nrPlacuta] == 2:
                        continue

                    # in caz ca dublura e pe aceeasi coloana, dar dedesubt
                    for i in range(lPlacutaC + 1, nr):
                        nrPlacuta2 = int(infoNod[i][cPlacutaC])

                        if nrPlacuta == nrPlacuta2:
                            verificareP[nrPlacuta] += 1
                            linieCopie = i
                            coloanaCopie = cPlacutaC

                            linieFinish = lPlacutaC
                            coloanaFinish = 2 * mijloc - cPlacutaC

                            nrPasi = 0

                            while linieCopie != linieFinish and coloanaCopie != coloanaFinish:
                                linieCopie = linieCopie - 1
                                coloanaCopie += 1
                                nrPasi += 1

                            while linieCopie != linieFinish:
                                linieCopie = linieCopie - 1
                                nrPasi += 1

                            while coloanaCopie != coloanaFinish:
                                coloanaCopie += 1
                                nrPasi += 1

                            hTotal = hTotal + nrPasi

                    # in caz ca dublura se afla pe urmatoarele coloane
                    for j in range(cPlacutaC + 1, nr):
                        for i in range(len(infoNod[j])):
                            nrPlacuta2 = int(infoNod[i][j])

                            if nrPlacuta == nrPlacuta2:
                                verificareP[nrPlacuta] += 1
                                linieCopie = i
                                coloanaCopie = j

                                linieFinish = lPlacutaC
                                coloanaFinish = 2 * mijloc - cPlacutaC

                                nrPasi = 0

                                while linieCopie != linieFinish and coloanaCopie != coloanaFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                while linieCopie != linieFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    nrPasi = nrPasi + 1

                                while coloanaCopie != coloanaFinish:
                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                hTotal = hTotal + nrPasi


            # verific si pe coloanele din dreapta spre mijloc
            for cPlacutaC in range(nr - 1, mijloc - 1, -1):
                for lPlacutaC in range(len(infoNod[cPlacutaC])):
                    nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])

                    if verificareP[nrPlacuta] == 0:
                        verificareP[nrPlacuta] += 1

                    if verificareP[nrPlacuta] == 2:
                        continue

                    # in caz ca dublura e pe aceeasi coloana, dar dedesubt
                    for i in range(lPlacutaC + 1, nr):
                        nrPlacuta2 = int(infoNod[i][cPlacutaC])

                        if nrPlacuta == nrPlacuta2:
                            verificareP[nrPlacuta] += 1
                            linieCopie = i
                            coloanaCopie = cPlacutaC

                            linieFinish = lPlacutaC
                            coloanaFinish = 2 * mijloc - cPlacutaC

                            nrPasi = 0

                            while linieCopie != linieFinish and coloanaCopie != coloanaFinish:
                                linieCopie = linieCopie - 1
                                coloanaCopie = coloanaCopie - 1
                                nrPasi += 1

                            while linieCopie != linieFinish:
                                linieCopie = linieCopie - 1
                                nrPasi += 1

                            while coloanaCopie != coloanaFinish:
                                coloanaCopie = coloanaCopie - 1
                                nrPasi += 1

                            hTotal = hTotal + nrPasi

                    # in caz ca dublura se afla pe urmatoarele coloane ( pana la mijloc inclusiv )
                    for j in range(cPlacutaC - 1, mijloc - 1, -1):
                        for i in range(len(infoNod[i])):
                            nrPlacuta2 = int(infoNod[i][j])

                            if nrPlacuta == nrPlacuta2:
                                verificareP[nrPlacuta] += 1
                                linieCopie = i
                                coloanaCopie = j

                                linieFinish = lPlacutaC
                                coloanaFinish = 2 * mijloc - cPlacutaC

                                nrPasi = 0

                                while linieCopie != linieFinish and coloanaCopie != coloanaFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                while linieCopie != linieFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    nrPasi = nrPasi + 1

                                while coloanaCopie != coloanaFinish:
                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                hTotal = hTotal + nrPasi

            return hTotal


        if tip_euristica == "euristica neadmisibila":
            hTotal = 0
            nr = len(infoNod[0])
            M = (nr * nr - 1) // 2
            verificareP = [0] * (M+1)
            mijloc = nr // 2

            for cPlacutaC in range(mijloc):
                for lPlacutaC in range(len(infoNod[cPlacutaC])):
                    if infoNod[lPlacutaC][cPlacutaC] == '0':
                        continue

                    nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])

                    if verificareP[nrPlacuta] == 0:
                        verificareP[nrPlacuta] += 1

                    if verificareP[nrPlacuta] == 2:
                        continue

                    # in caz ca dublura e pe aceeasi coloana, dar dedesubt
                    for i in range(lPlacutaC + 1, nr):
                        nrPlacuta2 = int(infoNod[i][cPlacutaC])

                        if nrPlacuta == nrPlacuta2:
                            verificareP[nrPlacuta] += 1
                            linieCopie = i
                            coloanaCopie = cPlacutaC

                            linieFinish = lPlacutaC
                            coloanaFinish = 2 * mijloc - cPlacutaC

                            nrPasi = 0

                            while coloanaCopie != coloanaFinish:
                                coloanaCopie += 1
                                nrPasi += 1

                            while linieCopie != linieFinish:
                                linieCopie = linieCopie - 1
                                nrPasi += 1

                            hTotal = hTotal + nrPasi

                    # in caz ca dublura se afla pe urmatoarele coloane
                    for j in range(cPlacutaC + 1, nr):
                        for i in range(len(infoNod[j])):
                            nrPlacuta2 = int(infoNod[i][j])

                            if nrPlacuta == nrPlacuta2:
                                verificareP[nrPlacuta] += 1
                                linieCopie = i
                                coloanaCopie = j

                                linieFinish = lPlacutaC
                                coloanaFinish = 2 * mijloc - cPlacutaC

                                nrPasi = 0

                                while coloanaCopie != coloanaFinish:
                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                while linieCopie != linieFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    nrPasi = nrPasi + 1

                                hTotal = hTotal + nrPasi

            # verific si pe coloanele din dreapta spre mijloc
            for cPlacutaC in range(nr - 1, mijloc - 1, -1):
                for lPlacutaC in range(len(infoNod[cPlacutaC])):
                    nrPlacuta = int(infoNod[lPlacutaC][cPlacutaC])

                    if verificareP[nrPlacuta] == 0:
                        verificareP[nrPlacuta] += 1

                    if verificareP[nrPlacuta] == 2:
                        continue

                    # in caz ca dublura e pe aceeasi coloana, dar dedesubt
                    for i in range(lPlacutaC + 1, nr):
                        nrPlacuta2 = int(infoNod[i][cPlacutaC])

                        if nrPlacuta == nrPlacuta2:
                            verificareP[nrPlacuta] += 1
                            linieCopie = i
                            coloanaCopie = cPlacutaC

                            linieFinish = lPlacutaC
                            coloanaFinish = 2 * mijloc - cPlacutaC

                            nrPasi = 0

                            while linieCopie != linieFinish:
                                linieCopie = linieCopie - 1
                                nrPasi += 1

                            while coloanaCopie != coloanaFinish:
                                coloanaCopie = coloanaCopie - 1
                                nrPasi += 1

                            hTotal = hTotal + nrPasi

                    # in caz ca dublura se afla pe urmatoarele coloane ( pana la mijloc inclusiv )
                    for j in range(cPlacutaC - 1, mijloc - 1, -1):
                        for i in range(len(infoNod[i])):
                            nrPlacuta2 = int(infoNod[i][j])

                            if nrPlacuta == nrPlacuta2:
                                verificareP[nrPlacuta] += 1
                                linieCopie = i
                                coloanaCopie = j

                                linieFinish = lPlacutaC
                                coloanaFinish = 2 * mijloc - cPlacutaC

                                nrPasi = 0

                                while linieCopie != linieFinish:
                                    if linieCopie > linieFinish:
                                        linieCopie = linieCopie - 1
                                    else:
                                        linieCopie = linieCopie + 1

                                    nrPasi = nrPasi + 1

                                while coloanaCopie != coloanaFinish:
                                    if coloanaCopie > coloanaFinish:
                                        coloanaCopie = coloanaCopie - 1
                                    else:
                                        coloanaCopie = coloanaCopie + 1

                                    nrPasi = nrPasi + 1

                                hTotal = hTotal + nrPasi

            return hTotal


def __repr__(self):
    sir = ""
    for (k, v) in self.__dict__.items():
        sir += "{} = {}\n".format(k, v)
    return (sir)


def uniform_cost(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)

    if not gr.existentaSolutie(gr.start):
        print("Nu avem solutii pentru exemplul dat.")
        return

    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    tic = time.perf_counter()

    while len(c) > 0:
        nodCurent = c.pop(0)

        tak = time.perf_counter()
        sec = tak - tic
        if sec > 650:
            print("Programul ruleaza prea mult!")
            break

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)

            toc = time.perf_counter()
            print(f"Solutia a fost rulata in {toc - tic:0.4f} secunde")
            print("\n----------------\n")

            nrSolutiiCautate -= 1

            if nrSolutiiCautate == 0:
                return

        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g >= s.g:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)

    if not gr.existentaSolutie(gr.start):
        print("Nu avem solutii pentru exemplul dat.")
        return

    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    tic = time.perf_counter()

    while len(c) > 0:
        nodCurent = c.pop(0)

        tak = time.perf_counter()
        sec = tak - tic
        if sec > 650:
            print("Programul ruleaza prea mult!")
            break

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            toc = time.perf_counter()
            print(f"Solutia a fost rulata in {toc - tic:0.4f} secunde")
            print("\n----------------\n")
            # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star_optimizat(gr, tip_euristica):

    if not gr.existentaSolutie(gr.start):
        print("Nu avem solutii pentru exemplul dat.")
        return

    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    tic = time.perf_counter()
    l_closed = []

    # l_open contine nodurile candidate pentru expandare
    # l_closed contine nodurile expandate

    while len(l_open) > 0:

        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)

        tak = time.perf_counter()
        sec = tak - tic
        if sec > 650:
            print("Programul ruleaza prea mult!")
            break

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            toc = time.perf_counter()
            print(f"Solutia a fost rulata in {toc - tic:0.4f} secunde")
            print("\n----------------\n")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)


def ida_star(gr, nrSolutiiCautate, tip_euristica):

    if not gr.existentaSolutie(gr.start):
        print("Nu avem solutii pentru exemplul dat.")
        return

    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f

    while True:

        print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, tip_euristica)

        if rez == "gata":
            break
        if rez == float('inf'):
            print("Nu exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)



def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, tip_euristica):

    print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, tip_euristica)
        if rez == "gata":
            return 0, "gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim



gr = Graph("input.txt")
NodParcurgere.gr = gr

'''
print("\n\n##################\nSolutii obtinute cu UCS:")
nrSolutiiCautate = 3
uniform_cost(gr, nrSolutiiCautate=3, tip_euristica="euristica banala")
'''


print("\n\n##################\nSolutii obtinute cu A*:")
nrSolutiiCautate = 2
a_star(gr, nrSolutiiCautate=2, tip_euristica="euristica nebanala2")


'''
print("\n\n##################\nSolutie obtinute cu A* optimizat:")
a_star_optimizat(gr, tip_euristica="euristica neadmisibila")
'''

'''
print("\n\n##################\nSolutii obtinute cu IDA:")
nrSolutiiCautate = 3
ida_star(gr, nrSolutiiCautate=3, tip_euristica="euristica nebanala2")
'''
