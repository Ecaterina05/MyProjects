import random
from random import sample
from problem import Problem


class Problem17(Problem):
    def __init__(self):
        statement = "Se da sirul "
        l = random.randint(9, 15)  # l = lungimea sirului
        v = sample(range(1, 100), l)
        statement += str(v)
        statement += "\nRezolvati urmatoarea cerinta:\n"
        k = random.randint(1, 8)  # Poz pe care o dorim
        statement += "\nAplicati o partitionare a lui QS pentru a gasi care este al " + str(
            k) + "-lea element, daca vectorul ar fi sortat si exemplificati algoritmul.\n"
        data = [v, k, l]
        self.solution1 = ""
        super().__init__(statement, data)

    def partition(self, sir, low, high):
        i = low  # cel mai la stanga element
        j = high  # cel mai la dreapta element
        pivot = sir[random.randint(low, high)]
        poz_pivot = sir.index(pivot)
        l = len(sir)

        self.solution1 += "\n" + " Am ales random pivotul: " + str(pivot) + "\n"
        self.solution1 += " Vectorul dupa partitionarea cu pivotul " + str(pivot) + " arata asa: \n"

        while i < j:
            # incrementare i daca e mai mic
            if sir[i] < pivot:
                i = i + 1
            elif sir[j] > pivot:
                j = j - 1
                # self.solution1 += "\n" + str(sir) + "\n"
            else:
                sir[i], sir[j] = sir[j], sir[i]
        self.solution1 += str(sir) + "\n"
        return j

    def quickSort_modif(self, sir, low, high, k):
        if low < high:
            poz_pivot = Problem17.partition(self, sir, low, high)

            # modificam doar partea care contine elementul dorit
            # astfel avem compexitate O(n)
            if poz_pivot == k:
                self.solution1 += "Am gasit elementul de pe pozitia " + str(k + 1) + ", acesta este " + str(
                    sir[k]) + ".\n "
                return
            elif poz_pivot < k:
                Problem17.quickSort_modif(self, sir, poz_pivot + 1, high, k)
            else:
                Problem17.quickSort_modif(self, sir, low, poz_pivot - 1, k)
        else:
            self.solution1 += " Am gasit elementul de pe pozitia " + str(k + 1) + ", acesta este " + str(sir[k]) + ".\n "

    def solve(self):
        sir = self.data[0]
        k = self.data[1] - 1
        l = self.data[2]
        self.solution1 +="Cautam elementul de pe pozitia " + str(k+1) + ".\n"
        self.solution1 += "Aplicam quick sort modificat.\n"
        Problem17.quickSort_modif(self, sir, 0, l - 1, k)
        # solution = str(sir)
        return  self.solution1