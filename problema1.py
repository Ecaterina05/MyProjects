from problem import Problem
import random
from collections import deque

class corpul_problemei(Problem):
    def __init__(self):
        v=random.sample(range(3), random.randint(3, 3))
        VectorNume = ["George", "Alina", "Marius"]
        VectorActiune = ["vrea", "doreste" ,"are"]
        VectorObiect = ["masina", "banane", "vacanta"]
        data = [VectorNume[v[0]], VectorActiune[v[1]], VectorObiect[v[2]]]
        statement = 'Aveti la dispozitie 3 structuri de date: \n'
        statement += '  1 -> stiva \n'
        statement += '  2 -> coada \n'
        statement += '  3 -> stiva \n'
        statement += 'Operatii: \n'
        statement += '  caracter -> se introduce caracterul in prima stiva \n'
        statement += '  1 -> se scoate din structura 1 se introduce in structura 2 \n'
        statement += '  2 -> se scoate din structura 2 se introduce in structura 3 \n'
        statement += '  3 -> se scoate din structura 3 se introduce in structura 1 \n'
        statement += 'Scrieti un sir de operatii pentru a avea la sfarsit:\n'
        statement += '  1 -> '  +  VectorNume[v[0]]
        statement += '\n'
        statement += '  2 -> '  +  VectorActiune[v[1]]
        statement += '\n'
        statement += '  3 -> '  +  VectorObiect[v[2]]
        super().__init__(statement, data)

    def solve(self):
        solution = '    Creeam cele trei structuri de date in ordine: stiva coada stiva.\n'
        solution += 'Stiva1: |__________|\n'
        solution += 'Coada:  |__________|\n'
        solution += 'Stiva2: |__________|\n\n'

        stiva1 = []
        coada  = deque([])
        stiva2 = []

        sstiva1 = []
        ccoada = deque([])


        solution += 'PAS.1.\n'
        solution += '   Introducem literele primului cuvant in ordine in prima stiva folosind operatia caracter de mai multe ori\n'
        for i in range(0, len(self.data[0])):
            stiva1.append(self.data[0][i])
            sstiva1.append(self.data[0][i])
        solution += 'Stiva1: ' +" ".join(map(str,stiva1))
        solution += '\n'
        solution += 'Coada:  \n'
        solution += 'Stiva2: \n\n'



        solution += 'PAS.2.\n'
        solution += '   Introducem pe rand in prima stiva fiecare litera din al treilea cuvant efectuand operatiile 1 respectiv 2 de fiecare data:\n'
        for i in range(0,len(self.data[2])):
            solution += '   Introducem litera ' + self.data[2][i]
            solution += ' in prima stiva: \n'
            stiva1.append(self.data[2][i])
            sstiva1.append(self.data[2][i])
            solution += 'Stiva1: '+" ".join(map(str,stiva1))
            solution += '\n'
            solution += 'Coada:  \n'
            solution += 'Stiva2: '+ " ".join(map(str, stiva2))
            solution += '\n\n'
            solution += 'Efectuam operatia 1 \n'
            aux = sstiva1.pop()
            aux = '\u0336' + '\033[91m' + aux +'\033[0m'
            sstiva1.append(aux)
            solution += 'Stiva1: '+" ".join(map(str,stiva1))
            solution += '\n'
            coada.append(stiva1.pop())
            ccoada.append(self.data[2][i])
            solution += 'Coada:  '+" ".join(map(str,coada))
            solution += '\n'
            solution += 'Stiva2: ' + " ".join(map(str, stiva2))
            solution +='\n\n'
            solution += 'Efectuam operatia 2 \n'
            solution += 'Stiva1: ' + " ".join(map(str, stiva1))
            solution += '\n'
            aux = coada.popleft()
            ccoada[i] = '\u0336' +'\033[91m' + aux +'\033[0m'
            solution += 'Coada:  '
            solution += '\n'
            stiva2.append(aux)
            solution += 'Stiva2: '+ " ".join(map(str, stiva2))
            solution +='\n\n'


        solution += '\nPAS.3.\n'
        solution +='   Introducem pe rand in prima stiva fiecare litera din al doilea cuvant efectuand operatia caracter de fiecare data:\n'
        for i in range (0,len(self.data[1])):
            solution += '   Introducem litera ' + self.data[1][i]
            solution += ' in prima stiva: \n'
            stiva1.append(self.data[1][i])
            sstiva1.append(self.data[1][i])
            solution += 'Stiva1: ' + " ".join(map(str, stiva1))
            solution += '\n'
            solution += 'Coada:  ' + " ".join(map(str, coada))
            solution += '\n'
            solution += 'Stiva2: ' + " ".join(map(str, stiva2))
            solution += '\n\n'
            solution += 'Efectuam operatia 1 \n'
            aux = sstiva1.pop()
            aux = '\u0336'  +'\033[91m' + aux +'\033[0m'
            sstiva1.append(aux)
            coada.append(stiva1.pop())
            solution += 'Stiva1: ' + " ".join(map(str, stiva1))
            solution += '\n'

            ccoada.append(self.data[1][i])
            solution += 'Coada:  ' + " ".join(map(str, coada))
            solution += '\n'
            solution += 'Stiva2: ' + " ".join(map(str, stiva2))
            solution += '\n\n'


        solution += '   Sirul de operatii folosit: \n'
        for i in range(0, len(self.data[0])):
            solution += self.data[0][i] + ' \u0332' + 'c '
        for i in range(0, len(self.data[2])):
            solution +=self.data[2][i]  + ' \u0332' + 'c ' + ' \u0332' + '1 ' + ' \u0332' + '2 '
        for i in range(0, len(self.data[1])):
            solution += self.data[1][i] + ' \u0332' + 'c '  + ' \u0332' + '1 '
        solution += '\n\n'


        solution += 'Stiva1: ' + " ".join(map(str, sstiva1))
        solution +='\n'
        solution += 'Coada:  ' + " ".join(map(str, ccoada))
        solution +='\n'
        solution += 'Stiva2: ' + " ".join(map(str, stiva2))
        solution +="\n"
        return solution
