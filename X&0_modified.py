import time
import copy
import pygame
import sys


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    GOL = '#'
    NR_LINII = None
    NR_COLOANE = None

    @classmethod
    def initializeaza(cls, display, NR_LINII=6, NR_COLOANE=7, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_LINII):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE
            coloana = ind % self.__class__.NR_COLOANE

            if marcaj == ind:
                # daca am o patratica selectata, o desenez cu rosu
                culoare = (255, 0, 0)
            else:
                # altfel o desenez cu alb
                culoare = (255, 255, 255)  # alb
            pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind])
            if self.matr[linie][coloana] == 'x':
                self.__class__.display.blit(self.__class__.x_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == '0':
                self.__class__.display.blit(self.__class__.zero_img, (
                    coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()
        # pygame.display.update()

    def __init__(self, matr=None, NR_LINII=None, NR_COLOANE=None):

        if matr:
            # e data tabla, deci suntem in timpul jocului
            self.matr = matr
        else:
            # nu e data tabla deci suntem la initializare
            self.matr = [[self.__class__.GOL] * NR_COLOANE for i in range(NR_LINII)]

            if NR_LINII is not None:
                self.__class__.NR_LINII = NR_LINII
            if NR_COLOANE is not None:
                self.__class__.NR_COLOANE = NR_COLOANE

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def parcurgere(self):
        nr_x = 0
        nr_0 = 0

        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE
            coloana = ind % self.__class__.NR_COLOANE

            if self.matr[linie][coloana] == 'x':
                nr_x = nr_x + 1
            elif self.matr[linie][coloana] == '0':
                nr_0 = nr_0 + 1
            else:
                continue

        return nr_x, nr_0

    def final(self):
        rez = False
        i, j = self.parcurgere()

        if i + j == self.__class__.NR_COLOANE * self.__class__.NR_LINII:
            if i > j:
                rez = 'x'
            elif i < j:
                rez = '0'
            else:
                rez = 'remiza'

        if rez:
            return rez
        else:
            return False

    def mutari(self, jucator):
        l_mutari = []
        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE
            coloana = ind % self.__class__.NR_COLOANE
            if self.matr[linie][coloana] == self.__class__.GOL:
                matr_tabla_noua = copy.deepcopy(self.matr)
                matr_tabla_noua[linie][coloana] = jucator
                l_mutari.append(Joc(matr_tabla_noua))

        return l_mutari

    def numara_aparitii(self, simbol):
        nr_aparitii = 0
        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE
            coloana = ind % self.__class__.NR_COLOANE

            if self.matr[linie][coloana] == simbol:
                nr_aparitii = nr_aparitii + 1

        return nr_aparitii

    def numar_casute(self, simbol):
        nr_vecini = 0
        directii = [[0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1], [1, 0], [-1, 0]]
        for ind in range(self.__class__.NR_COLOANE * self.__class__.NR_LINII):
            linie = ind // self.__class__.NR_COLOANE
            coloana = ind % self.__class__.NR_COLOANE
            if self.matr[linie][coloana] == Joc.GOL:
                for dr1, dr2 in directii:
                    linieVecin = linie + dr1
                    coloanaVecin = coloana + dr2

                    if linieVecin < 0 or coloanaVecin < 0 or linieVecin > Joc.NR_LINII - 1 or coloanaVecin > Joc.NR_COLOANE - 1:
                        continue

                    if self.matr[linieVecin][coloanaVecin] == simbol:
                        nr_vecini = nr_vecini + 1
                    else:
                        continue

        return nr_vecini

    #daca nu e stare finala, estimarea o calculam prin nr de simboluri pt JMAX(calculatorul) minus
    #nr de simboluri pt JMIN(jucatorul)
    def estimeaza_scor1(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.numara_aparitii(self.__class__.JMAX) - self.numara_aparitii(self.__class__.JMIN))

    # daca nu e stare finala, estimarea o calculam prin nr de simboluri pt JMAX(calculatorul) minus
    # nr de simboluri pt JMIN(jucatorul) + nr de vecini JMAX al casutelor goale - nr de vecini JMIN al casutelor goale
    def estimeaza_scor2(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.numara_aparitii(self.__class__.JMAX) - self.numara_aparitii(self.__class__.JMIN)
                    + self.numar_casute(self.__class__.JMAX) - self.numar_casute(self.__class__.JMIN))

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        sir += "\n".join([str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) for i in range(len(self.matr))])
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir

    def __repr__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor2(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


""" Algoritmul Alfa-Beta """


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor2(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(89, 134, 194),
                 culoareFundalSel=(102, 0, 51), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="x", valoare="x"),
            Buton(display=display, w=35, h=30, text="zero", valoare="0")
        ],
        indiceSelectat=0)
    btn_dif = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Incepator", valoare="Incepator"),
            Buton(display=display, w=80, h=30, text="Mediu", valoare="Mediu"),
            Buton(display=display, w=80, h=30, text="Avansat", valoare="Avansat")
        ],
        indiceSelectat=0)

    ok = Buton(display=display, top=230, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_dif.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_dif.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                tabla_curenta.deseneaza_grid()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_dif.getValoare()
        pygame.display.update()


def main():
    # setari interf grafica
    pygame.init()
    pygame.display.set_caption("Baltatescu Elena-Ecaterina")
    # dimensiunea ferestrei in pixeli
    nl = 6
    nc = 7
    w = 50
    ecran = pygame.display.set_mode(size=(nc * (w + 1) - 1, nl * (w + 1) - 1))  # N *w+ N-1= N*(w+1)-1
    Joc.initializeaza(ecran, NR_LINII=nl, NR_COLOANE=nc, dim_celula=w)

    # initializare tabla
    tabla_curenta = Joc(NR_LINII=6, NR_COLOANE=7)
    Joc.JMIN, tip_algoritm, tip_dificultate = deseneaza_alegeri(ecran, tabla_curenta)
    print(Joc.JMIN, tip_algoritm, tip_dificultate)

    if tip_dificultate == "Incepator":
        ADANCIME_MAX = 2
    if tip_dificultate == "Mediu":
        ADANCIME_MAX = 3
    if tip_dificultate == "Avansat":
        ADANCIME_MAX = 4

    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    de_mutat = False
    tabla_curenta.deseneaza_grid()

    while True:

        if (stare_curenta.j_curent == Joc.JMIN):

            t_inainte = int(round(time.time() * 1000))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # iesim din program
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()  # coordonatele cursorului la momentul clickului

                    for np in range(len(Joc.celuleGrid)):

                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // Joc.NR_COLOANE
                            coloana = np % Joc.NR_COLOANE

                            ###############################
                            if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                                if de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]:
                                    # daca am facut click chiar pe patratica selectata, o deselectez
                                    de_mutat = False
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                else:
                                    de_mutat = (linie, coloana)
                                    # desenez gridul cu patratelul marcat
                                    stare_curenta.tabla_joc.deseneaza_grid(np)

                            if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                if de_mutat:
                                    #### eventuale teste legate de mutarea simbolului
                                    stare_curenta.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.GOL
                                    de_mutat = False
                                # plasez simbolul pe "tabla de joc"
                                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN

                                directii = [[0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1], [1, 0], [-1, 0]]
                                verificare = True
                                while verificare:
                                    ok = 0
                                    for ind in range(Joc.NR_COLOANE * Joc.NR_LINII):
                                        linie = ind // Joc.NR_COLOANE
                                        coloana = ind % Joc.NR_COLOANE
                                        nr_simbol = 0
                                        nr_celalalt_simbol = 0
                                        if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                            for dr1, dr2 in directii:
                                                linieVecin = linie + dr1
                                                coloanaVecin = coloana + dr2

                                                if linieVecin < 0 or coloanaVecin < 0 or linieVecin > Joc.NR_LINII - 1 or coloanaVecin > Joc.NR_COLOANE - 1:
                                                    continue

                                                if stare_curenta.tabla_joc.matr[linieVecin][coloanaVecin] == Joc.JMIN:
                                                    nr_simbol = nr_simbol + 1
                                                elif stare_curenta.tabla_joc.matr[linieVecin][
                                                    coloanaVecin] != Joc.JMIN and \
                                                        stare_curenta.tabla_joc.matr[linieVecin][
                                                            coloanaVecin] != Joc.GOL:
                                                    nr_celalalt_simbol = nr_celalalt_simbol + 1
                                                else:
                                                    continue

                                            if nr_simbol >= 4 and nr_celalalt_simbol < 4:
                                                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                                ok = 1

                                    if ok == 0:
                                        verificare = False

                                # afisarea starii jocului in urma mutarii utilizatorului
                                print("\nTabla dupa mutarea jucatorului")
                                print(str(stare_curenta))
                                t_dupa = int(round(time.time() * 1000))
                                print("Jucatorul a gandit timp de " + str(t_dupa - t_inainte) + " milisecunde.\n")

                                stare_curenta.tabla_joc.deseneaza_grid()
                                # testez daca jocul a ajuns intr-o stare finala
                                # si afisez un mesaj corespunzator in caz ca da
                                if (afis_daca_final(stare_curenta)):
                                    break

                                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)



        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == 'minimax':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc

            directii = [[0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1], [1, 0], [-1, 0]]
            verificare = True
            while verificare:
                ok = 0
                for ind in range(Joc.NR_COLOANE * Joc.NR_LINII):
                    linie = ind // Joc.NR_COLOANE
                    coloana = ind % Joc.NR_COLOANE
                    nr_simbol = 0
                    nr_celalalt_simbol = 0
                    if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                        for dr1, dr2 in directii:
                            linieVecin = linie + dr1
                            coloanaVecin = coloana + dr2

                            if linieVecin < 0 or coloanaVecin < 0 or linieVecin > Joc.NR_LINII - 1 or coloanaVecin > Joc.NR_COLOANE - 1:
                                continue

                            if stare_curenta.tabla_joc.matr[linieVecin][coloanaVecin] == Joc.JMAX:
                                nr_simbol = nr_simbol + 1
                            elif stare_curenta.tabla_joc.matr[linieVecin][coloanaVecin] != Joc.JMAX and \
                                    stare_curenta.tabla_joc.matr[linieVecin][coloanaVecin] != Joc.GOL:
                                nr_celalalt_simbol = nr_celalalt_simbol + 1
                            else:
                                continue

                        if nr_simbol >= 4 and nr_celalalt_simbol < 4:
                            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMAX
                            ok = 1

                if ok == 0:
                    verificare = False

            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            stare_curenta.tabla_joc.deseneaza_grid()

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    toc = time.perf_counter()
    print(f"Jocul a durat timp de {toc - tic:0.4f} secunde")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
