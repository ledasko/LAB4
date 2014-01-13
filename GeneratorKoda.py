__author__ = 'Matko'

import sys

def nadiSlobodniRegistar():
    trenRegistar = -1
    for registar in zauzetostRegistara:
        if zauzetostRegistara[registar] == 0:
            trenRegistar = registar
            break
    return trenRegistar

def imaLiLabele(redak):
    global labele
    if redak in labele:
        return 1
    else:
        return 0

def ispisGreske(desnaStrana):
    pozicijaPrviDesni = desnaStrana[0][1]
    pozicijaLijevi = pozicijaPrviDesni - 1

    lijevaStrana = listaPrograma[pozicijaLijevi]
    lijevaStrana = lijevaStrana.strip()

    listaDesnaStrana = []

    for element in desnaStrana:
        listaDesnaStrana.append(element[0])

    novaListaDesneStrane = []

    for element in listaDesnaStrana:
        if element[0] == '<':
            novaListaDesneStrane.append(element)
            continue
        tmp = list(element)
        for i in range(len(tmp)):
            if tmp[i] == ' ':
                tmp.insert(i,"(")
                del tmp[i+1]
                break
        for i in range(len(tmp)):
            if tmp[i] == ' ':
                tmp.insert(i,",")
                del tmp[i+1]
                break
        tmp.append(")")
        tmp = ''.join(tmp)

        novaListaDesneStrane.append(tmp)

    desnastrana = ' '.join(novaListaDesneStrane)
    ispis = lijevaStrana+" ::= "+desnastrana
    print ispis
    exit(1)

def provjeriImplicitno(tip1,tip2):
    if tip1=="const(int)":
        if tip2=="int":
            return 1
    if tip1=="const(char)":
        if tip2=="char":
            return 1
    if tip1=="const(void)":
        if tip2=="void":
            return 1

    if tip1=="int":
        if tip2=="const(int)":
            return 1
    if tip1=="char":
        if tip2=="const(char)":
            return 1
    if tip1=="void":
        if tip2=="const(void)":
            return 1

    if tip1=="char":
        if tip2=="int":
            return 1
    if tip1=="niz(int)":
        if tip2=="niz(const(int))":
            return 1
    if tip1=="niz(char)":
        if tip2=="niz(const(char))":
            return 1
    if tip1=="niz(void)":
        if tip2=="niz(const(void))":
            return 1

    if tip1=="char":
        if tip2=="char":
            return 1
    if tip1=="int":
        if tip2=="int":
            return 1
    if tip1=="void":
        if tip2=="void":
            return 1

    if tip1 == "const(int)":
        if tip2=="const(int)":
            return 1
    if tip1 == "const(char)":
        if tip2=="const(char)":
            return 1
    if tip1 == "niz(const(int))":
        if tip2=="niz(const(int))":
            return 1
    if tip1 == "niz(const(char))":
        if tip2=="niz(const(char))":
            return 1

    if tip1 == "char":
        if tip2 == "niz(char)":
            return 1
    if tip1 == "int":
        if tip2 == "niz(int)":
            return 1

    if tip1 == "char":
        if tip2 == "niz(const(char))":
            return 1
    if tip1 == "int":
        if tip2 == "niz(const(int))":
            return 1

    if tip1 == "niz(int)":
        if tip2 == "niz(int)":
            return 1
    if tip1 == "niz(char)":
        if tip2 == "niz(char)":
            return 1


    return 0

def provjeriEksplicitno(tip1,tip2):
    if tip1=="int":
        if tip2=="char":
            return 1

    return provjeriImplicitno(tip1,tip2)

def provjeriNizX(tip):
    cmp1 = "niz(char)"
    cmp2 = "niz(const(char))"
    cmp3 = "niz(int)"
    cmp4 = "niz(const(int))"

    if tip == cmp1 or tip == cmp2 or tip == cmp3 or tip == cmp4:
        return True
    else:
        return False

def izvuciXizNiza(tip):

    tip = list(tip)

    del tip[-1]
    del tip[:4]

    tip = ''.join(tip)
    return tip

def zabiljeziDeklaracijuFunkcije(idn,tip,listaParametara):
    #oblik tablice {IDN:[0/1 - definirana,povratniTip,listaParametara]]...}

    value = []
    value.append(False) #nije definirana
    value.append(tip)
    if listaParametara == "void":
        value.append("void")
    else:
        value.append(listaParametara)

    listaTablica[aktualnaTablica][idn] = value

def zabiljeziDefinicijuFunkcije(idn,tip,listaParametara):
    #oblik tablice {IDN:[0/1 - definirana,povratniTip,listaParametara]]...}

    value = []
    value.append(True) #definirana je
    value.append(tip)
    if listaParametara == "void":
        value.append("void")
    else:
        value.append(listaParametara)

    listaTablica[aktualnaTablica][idn] = value

def zabiljeziIDN(idn,tip):

    global aktualnaTablica
    global listaTablica
    value = []
    value.append(0)#po defaultu nijedan IDN nije l_izraz
    value.append(tip)
    listaTablica[aktualnaTablica][idn] = value

def zabiljeziIDNkaol_izraz(idn,tip):
    global aktualnaTablica
    global listaTablica

    global aktualnaTablica
    global listaTablica
    value = []
    value.append(1)#po defaultu nijedan IDN nije l_izraz
    value.append(tip)
    listaTablica[aktualnaTablica][idn] = value

def jeliDeklariranoLokalno(idn):
    global aktualnaTablica
    global listaTablica

    if idn in listaTablica[aktualnaTablica]:
        return True

    else:
        return False

def jeliDeklariranoIgdje(idn):
    global aktualnaTablica
    global listaTablica

    ret = []

    i = aktualnaTablica

    while i >= 0:
        if idn in listaTablica[i]:
            ret.append(1)
            ret.append(i)
            return ret
        i -= 1

    ret.append(0)
    ret.append(0)
    return ret

def dohvatiTipIl_izraz(idn,mjestoDeklaracije):
    global aktualnaTablica
    global listaTablica

    ret = []

    l_izraz = listaTablica[mjestoDeklaracije][idn][0]
    tip = listaTablica[mjestoDeklaracije][idn][1]

    ret.append(l_izraz)
    ret.append(tip)
    return ret

def izluciIDN(elementDesneStrane):

    idn = elementDesneStrane
    idn = list(idn)
    for i in reversed(range(len(idn))):
        if idn[i] == ' ':
            del idn[:i+1]
            break
    idn = ''.join(idn)
    return idn

def nadiBrojRazmaka(pozicija):
    global listaPrograma

    tmp = listaPrograma[pozicija]
    list(tmp)
    br = 0
    for i in range(len(tmp)):
        if tmp[i] == ' ':
            br += 1
        else:
            break
    return br

def nadiDesnuStranu(pozicija):
    global listaPrograma
    desnaStrana = []
    element = []
    indeks = []

    #DEBUG
    #tip = type(pozicija)
    #
    #if tip != int:
    #    print pozicija

    brojRazmaka = nadiBrojRazmaka(pozicija)
    novaPozicija = pozicija + 1
    #while noviBrojRazmaka != brojRazmaka:
    while 1:
        #provjera kraja programa, jesmo li doli do kraja liste
        if novaPozicija < len(listaPrograma):
            noviBrojRazmaka = nadiBrojRazmaka(novaPozicija)
        else:
            break

        #provjeri jesmo li nasli sve elemente desne strane
        if noviBrojRazmaka <= brojRazmaka:
            break

        #provjeri je li to trazeni element
        elif noviBrojRazmaka == brojRazmaka + 1:
            tmp = listaPrograma[novaPozicija]
            tmp = tmp.strip()
            element.append(tmp)
            indeks.append(novaPozicija)

        #pomakni poziciju
        novaPozicija += 1

    desnaStrana = zip(element, indeks)
    return desnaStrana

def stvoriTablicu():

    global aktualnaTablica
    global listaTablica
    aktualnaTablica += 1
    dict = {}

    #ako treba pobrisi staru tablicu
    if len(listaTablica) >= aktualnaTablica + 1:
        listaTablica[aktualnaTablica] = {}
    else:
        listaTablica.append(dict)

def vratiSeTablicuNazad():

    global aktualnaTablica
    global listaTablica

    #listaTablica[aktualnaTablica] = {}

    aktualnaTablica -= 1

class PrijevodnaJedinica(object):

    def __init__(self, pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):

        #desna strana dobija listu stvorenu od elemenata od dva clana, prvi je element, a drugi pozicija u listi
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<vanjska_deklaracija>":
            vanjska_deklaracija = VanjskaDeklaracija(desnaStrana[0][1])
            vanjska_deklaracija.provjeri()

        elif desnaStrana[0][0] == "<prijevodna_jedinica>":
            prijevodna_jedinica = PrijevodnaJedinica(desnaStrana[0][1])
            prijevodna_jedinica.provjeri()

            vanjska_deklaracija = VanjskaDeklaracija(desnaStrana[1][1])
            vanjska_deklaracija.provjeri()

class VanjskaDeklaracija(PrijevodnaJedinica):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<definicija_funkcije>":
            definicija_funkcije = DefinicijaFunkcije(desnaStrana[0][1])
            definicija_funkcije.provjeri()

        elif desnaStrana[0][0] == "<deklaracija>":
            deklaracija = Deklaracija(desnaStrana[0][1])
            deklaracija.provjeri()

class SlozenaNaredba(VanjskaDeklaracija):

    def __init__(self, pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        stvoriTablicu()

    def zabiljeziParametre(self,listaParametara):
        #treba zabiljeziti i parametre u tablicu
        for element in listaParametara:
            idn = element[1]
            tip = element[0]
            zabiljeziIDNkaol_izraz(idn, tip)

    def provjeri(self):

        global aktualnaTablica

        #desna strana dobija listu stvorenu od elemenata od dva clana, prvi je element, a drugi pozicija u listi
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[1][0] == "<lista_naredbi>":
            lista_naredbi = ListaNaredbi(desnaStrana[1][1])
            rezultat = lista_naredbi.provjeri()
        else:
            lista_deklaracija = ListaDeklaracija(desnaStrana[1][1])
            rezultat1 = lista_deklaracija.provjeri()

            lista_naredbi = ListaNaredbi(desnaStrana[2][1])
            lista_naredbi.provjeri()

        vratiSeTablicuNazad()

class ListaDeklaracija(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<deklaracija>":
            deklaracija = Deklaracija(desnaStrana[0][1])
            deklaracija.provjeri()
        else:
            lista_deklaracija = ListaDeklaracija(desnaStrana[0][1])
            lista_deklaracija.provjeri()

            deklaracija = Deklaracija(desnaStrana[1][1])
            deklaracija.provjeri()

class Deklaracija(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        ime_tipa = ImeTipa(desnaStrana[0][1])
        tip = ime_tipa.provjeri()

        lista_init_deklaratora = ListaInitDeklaratora(desnaStrana[1][1])
        lista_init_deklaratora.provjeri(tip)

class ListaInitDeklaratora(Deklaracija):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self,ntip):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<init_deklarator>":
            init_deklarator = InitDeklarator(desnaStrana[0][1])
            init_deklarator.provjeri(ntip)
        else:
            lista_init_deklaratora = ListaInitDeklaratora(desnaStrana[0][1])
            lista_init_deklaratora.provjeri(ntip)

            init_deklarator = InitDeklarator(desnaStrana[2][1])
            init_deklarator.provjeri(ntip)

class InitDeklarator(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def jeliTiliconstT(self,tip):

        if tip == "int" or tip == "char" or tip == "const(int)" or tip == "const(char)":
            return True
        else:
            return False

    def jelinizTIliconstT(self,tip):
        if tip == "niz(int)" or tip == "niz(char)" or tip == "niz(const(int))" or tip == "niz(const(char))":
            return True
        else:
            return False

    def asmBroj(self,ime,broj):
        global trenutniRedIzlaza
        broj = str(broj)
        lbl = "G_"+ime
        labele[trenutniRedIzlaza] = lbl
        vrijednostLabele[lbl] = broj
        file.write(lbl+"\t\tDW %D "+broj+"\n")
        trenutniRedIzlaza += 1

    def provjeri(self,ntip):
        global BROJ
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        izravni_deklarator = IzravniDeklarator(desnaStrana[0][1])
        tip = izravni_deklarator.provjeri(ntip)
        ime = izravni_deklarator.getIdn()

        if len(desnaStrana) > 1:

            inicijalizator = Inicijalizator(desnaStrana[2][1])
            tipovi = inicijalizator.provjeri()

            dbrElem = izravni_deklarator.getBroj()
            ibrElem = inicijalizator.getbrElem()
            
            #3. tocka 3 slucaja
            tIliconstT = self.jeliTiliconstT(tip)
            nizTIliconstT = self.jelinizTIliconstT(tip)

            if tIliconstT:

                implicitno = provjeriImplicitno(tipovi[0],tip)
                if not implicitno:
                    ispisGreske(desnaStrana)


            elif nizTIliconstT:
                if ibrElem > dbrElem:
                    ispisGreske(desnaStrana)
                for tipI in tipovi:
                    implicitno = provjeriImplicitno(tipI,tip)
                    if not implicitno:
                        ispisGreske(desnaStrana)
            else:
                ispisGreske(desnaStrana)

        else:
            if "const" in tip:
                ispisGreske(desnaStrana)
            elif "niz(const" in tip:
                ispisGreske(desnaStrana)

        if tip == 'int':
            self.asmBroj(ime,BROJ)

class ListaIzrazaPridruzivanja(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tipovi = []
        self.br_elem = 0

    def getbrElem(self):
        return self.br_elem

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<izraz_pridruzivanja>":
            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[0][1])
            izraz_pridruzivanja.provjeri()

            self.br_elem = 1
            tip = izraz_pridruzivanja.getTip()
            self.tipovi.append(tip)

            return self.tipovi

        else:
            lista_izraza_pridruzivanja = ListaIzrazaPridruzivanja(desnaStrana[0][1])
            self.tipovi = lista_izraza_pridruzivanja.provjeri()

            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[2][1])
            izraz_pridruzivanja.provjeri()

            tip = izraz_pridruzivanja.getTip()

            self.tipovi.append(tip)
            self.br_elem = lista_izraza_pridruzivanja.getbrElem() + 1

            return self.tipovi

class Inicijalizator(Deklaracija):
    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.br_elem = 0

    def provjeriNizZnakova(self):
        trenPoz = self.pozicijaUprogramu

        while 1:
            trenPoz += 1
            brRazmaka = nadiBrojRazmaka(trenPoz)
            brRazmaka2 = nadiBrojRazmaka(trenPoz+1)
            if brRazmaka+1 == brRazmaka2:
                if listaPrograma[trenPoz+1][-1] != '>':
                    tmp = listaPrograma[trenPoz+1]
                    for i in tmp:
                        if i != ' ':
                            if i == 'N':
                                return trenPoz + 1
                            else:
                                return 0
            else:
                return 0

    def prebrojiNizZnakova(self,neobradeniClan):

        self.br_elem = 0

        neobradeniClan = list(neobradeniClan)

        #for i in reversed(range(len(neobradeniClan))):
        #    if neobradeniClan[i] == ' ':
        #        del neobradeniClan[:i+1]
        #        break

        #del neobradeniClan[0]

        for i in range(len(neobradeniClan)):
            if neobradeniClan[i] == '"':
                del neobradeniClan[:i+1]
                break

        del neobradeniClan[-1]

        self.br_elem = len(neobradeniClan) + 1

    def popuniListuCharovima(self):
        tipovi = []
        i = 0
        while i < self.br_elem:
            tipovi.append("char")
            i += 1
        return tipovi

    def getbrElem(self):
        return self.br_elem

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<izraz_pridruzivanja>":
            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[0][1])
            izraz_pridruzivanja.provjeri()

            jeNiz = self.provjeriNizZnakova()

            lokacijaNizaZnakova = jeNiz
            lokacijaNizaZnakova = int(lokacijaNizaZnakova)

            if jeNiz:
                lokacijaNizaZnakova = jeNiz
                neobradeniClan = listaPrograma[lokacijaNizaZnakova]
                self.prebrojiNizZnakova(neobradeniClan)
                tipovi = self.popuniListuCharovima()
                return tipovi

            else:
                tip = []
                tip.append(izraz_pridruzivanja.getTip())
                return tip
        else:
            lista_izraza_pridruzivanja = ListaIzrazaPridruzivanja(desnaStrana[1][1])
            tipovi = lista_izraza_pridruzivanja.provjeri()

            self.br_elem = lista_izraza_pridruzivanja.getbrElem()

            return tipovi

class IzravniDeklarator(SlozenaNaredba):


    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.broj=0
        self.idn = ""

    def getBroj(self):
        return self.broj

    def getIdn(self):
        return self.idn

    def nadiBrojProdukcjie(self,desnaStrana):

        if len(desnaStrana) == 1: return 1

        elif desnaStrana[2][0] == "<lista_parametara>": return 4

        tmp = desnaStrana[2][0]

        if tmp[0] == 'B': return 2

        return 3

    def provjeri(self,ntip):

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        brojProdukcije = self.nadiBrojProdukcjie(desnaStrana)

        self.idn = izluciIDN(desnaStrana[0][0])

        if brojProdukcije == 1:
            #IDN je sam
            if ntip == 'void':
                ispisGreske(desnaStrana)

            deklarirano = jeliDeklariranoLokalno(self.idn)

            if deklarirano:
                ispisGreske(desnaStrana)

            zabiljeziIDNkaol_izraz(self.idn,ntip)

            return ntip

        elif brojProdukcije == 2:
            if ntip == 'void':
                ispisGreske(desnaStrana)

            if jeliDeklariranoLokalno(self.idn):
                ispisGreske(desnaStrana)

            self.broj = izluciIDN(desnaStrana[2][0])

            self.broj = int(self.broj)

            if self.broj <= 0 or self.broj > 1024:
                ispisGreske(desnaStrana)

            tip = "niz("+ntip+")"

            zabiljeziIDN(self.idn,tip)

            return tip

        elif brojProdukcije == 3:
            zabiljeziDeklaracijuFunkcije(self.idn,ntip,"void")

            #nesto treba vratit
            return ntip

        elif brojProdukcije == 4:
            lista_parametara = ListaParametara(desnaStrana[2][1])
            #listaParametara je oblika lista listi koje imaju clanove [tip,ime]
            listaParametara = lista_parametara.provjeri()

            zabiljeziDeklaracijuFunkcije(self.idn,ntip,listaParametara)

            #nesto treba vratit
            return ntip
        
class ListaParametara(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tipovi_imena = []

    def asmJedanParam(self):
        global trenutniRedIzlaza

        reg = nadiSlobodniRegistar()

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("LOAD R"+str(reg)+", (R7+4)\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+str(reg)+"\n")
        trenutniRedIzlaza += 1

    def asmViseParam(self):
        pass

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<deklaracija_parametra>":
            deklaracija_parametara = DeklaracijaParametra(desnaStrana[0][1])
            deklaracija_parametara.provjeri()

            tmp = []
            tip = deklaracija_parametara.getTip()
            ime = deklaracija_parametara.getIdn()
            tmp.append(tip)
            tmp.append(ime)

            self.tipovi_imena.append(tmp)

            self.asmJedanParam()

            return self.tipovi_imena

        else:
            lista_parametara = ListaParametara(desnaStrana[0][1])
            self.tipovi_imena = lista_parametara.provjeri()

            deklaracija_parametara = DeklaracijaParametra(desnaStrana[2][1])
            deklaracija_parametara.provjeri()

            tmp = []
            tip = deklaracija_parametara.getTip()
            ime = deklaracija_parametara.getIdn()
            tmp.append(tip)
            tmp.append(ime)

            if ime in self.tipovi_imena:
                ispisGreske(desnaStrana)

            self.tipovi_imena.append(tmp)

            self.asmViseParam()

            return self.tipovi_imena

class DeklaracijaParametra(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""
        self.idn = ""

    def getTip(self):
        return self.tip

    def getIdn(self):
        return self.idn

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        ime_tipa = ImeTipa(desnaStrana[0][1])
        self.tip = ime_tipa.provjeri()

        if self.tip == "void":
            ispisGreske(desnaStrana)

        self.idn = izluciIDN(desnaStrana[1][0])

        #ako je niz oznaci tako u povratnoj vrijednosti
        if len(desnaStrana) == 4:
            self.tip = "niz("+self.tip+")"

class ListaNaredbi(SlozenaNaredba):
    
    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<naredba>":
            naredba = Naredba(desnaStrana[0][1])
            naredba.provjeri()

        else:
            lista_naredbi = ListaNaredbi(desnaStrana[0][1])
            lista_naredbi.provjeri()

            naredba = Naredba(desnaStrana[1][1])
            naredba.provjeri()

class Naredba(SlozenaNaredba):
    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<slozena_naredba>":
            slozena_naredba = SlozenaNaredba(desnaStrana[0][1])
            slozena_naredba.provjeri()
        elif desnaStrana[0][0] == "<izraz_naredba>":
            izraz_naredba = IzrazNaredba(desnaStrana[0][1])
            tip = izraz_naredba.provjeri()
        elif desnaStrana[0][0] == "<naredba_grananja>":
            naredba_grananja = NaredbaGrananja(desnaStrana[0][1])
            naredba_grananja.provjeri()
        elif desnaStrana[0][0] == "<naredba_petlje>":
            naredba_petlje = NaredbaPetlje(desnaStrana[0][1])
            naredba_petlje.provjeri()
        elif desnaStrana[0][0] == "<naredba_skoka>":
            naredba_skoka = NaredbaSkoka(desnaStrana[0][1])
            naredba_skoka.provjeri()

class IzrazNaredba(Naredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<izraz>":
            izraz = Izraz(desnaStrana[0][1])
            l_izraz = izraz.provjeri()
            tip = izraz.getTip()
            return tip
        else:
            return "int"

class NaredbaGrananja(Naredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        izraz = Izraz(desnaStrana[2][1])
        izraz.provjeri()

        tip = izraz.getTip()

        if not provjeriImplicitno(tip,"int"):
            ispisGreske(desnaStrana)

        naredba1 = Naredba(desnaStrana[4][1])
        naredba1.provjeri()

        if len(desnaStrana) == 7:
            naredba2 = Naredba(desnaStrana[6][1])
            naredba2.provjeri()

class NaredbaPetlje(Naredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        #oznaci ulazak u petlju
        uPetlji.append(1)

        if len(desnaStrana) == 5:
            izraz = Izraz(desnaStrana[2][1])
            izraz.provjeri()

            if jeliFja:
                ispisGreske(desnaStrana)

            tip = izraz.getTip()

            if not provjeriImplicitno(tip,"int"):
                ispisGreske(desnaStrana)

            naredba = Naredba(desnaStrana[4][1])
            naredba.provjeri()

        else:
            izraz_naredba1 = IzrazNaredba(desnaStrana[2][1])
            tip1 = izraz_naredba1.provjeri()

            if jeliFja:
                ispisGreske(desnaStrana)

            izraz_naredba2 = IzrazNaredba(desnaStrana[3][1])
            tip2 = izraz_naredba2.provjeri()

            if jeliFja:
                ispisGreske(desnaStrana)

            if not provjeriImplicitno(tip2,"int"):
                ispisGreske(desnaStrana)

            if len(desnaStrana) == 6:
                naredba = Naredba(desnaStrana[5][1])
                naredba.provjeri()
            else:

                izraz = Izraz(desnaStrana[4][1])
                izraz.provjeri()

                naredba = Naredba(desnaStrana[6][1])
                naredba.provjeri()
        #oznaci izlazak iz petlje
        del uPetlji[-1]

class NaredbaSkoka(Naredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def nadiBrojProdukcije(self,desnaStrana):
        if len(desnaStrana) == 3:
            return 4
        tmp = desnaStrana[0][0]
        tmp = list(tmp)
        for i in range(len(tmp)):
            if tmp[i] == ' ':
                del tmp[i:]
                break
        kljucnaRijec = ''.join(tmp)

        if kljucnaRijec == 'KR_CONTINUE':
            return 1
        elif kljucnaRijec == 'KR_BREAK':
            return 2
        elif kljucnaRijec == 'KR_RETURN':
            return 3

    def asmreturn(self):
        global trenutniRedIzlaza
        global IME

        lbl = "G_"+IME
        for red in labele:
            if labele[red] == lbl:
                vrijednost = vrijednostLabele[lbl]
                reg = nadiSlobodniRegistar()
                lbl1 = imaLiLabele(trenutniRedIzlaza)
                if not lbl1:
                    file.write("\t\t\t")
                file.write("LOAD R"+str(reg)+", ("+lbl+")\n")
                trenutniRedIzlaza += 1

                lbl1 = imaLiLabele(trenutniRedIzlaza)
                if not lbl1:
                    file.write("\t\t\t")
                file.write("PUSH R"+str(reg)+"\n")
                trenutniRedIzlaza += 1
                break


        zauzetostRegistara[6] = 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R6\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("RET\n")
        trenutniRedIzlaza += 1

        zauzetostRegistara[6] = 0

    def provjeri(self):
        global imeTrenutneFunkcije
        global IME

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)
        brojProdukcije = self.nadiBrojProdukcije(desnaStrana)

        if brojProdukcije == 1:
            if len(uPetlji) == 1:
                ispisGreske(desnaStrana)

        elif brojProdukcije == 2:
            if len(uPetlji) == 1:
                ispisGreske(desnaStrana)
        elif brojProdukcije == 3:
            rezultat = jeliDeklariranoIgdje(imeTrenutneFunkcije)
            mjestoDeklaracije = rezultat[1]
            tipFje = listaTablica[mjestoDeklaracije][imeTrenutneFunkcije][1]
            if tipFje != "void":
                ispisGreske(desnaStrana)
        elif brojProdukcije == 4:
            izraz = Izraz(desnaStrana[1][1])
            izraz.provjeri()

            tip = izraz.getTip()

            rezultat = jeliDeklariranoIgdje(imeTrenutneFunkcije)
            mjestoDeklaracije = rezultat[1]
            tipFje = listaTablica[mjestoDeklaracije][imeTrenutneFunkcije][1]

            implicitno = provjeriImplicitno(tip,tipFje)

            if not implicitno:
                ispisGreske(desnaStrana)

            self.asmreturn()

class Izraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<izraz_pridruzivanja>":
            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[0][1])
            l_izraz = izraz_pridruzivanja.provjeri()

            self.tip = izraz_pridruzivanja.getTip()

            return l_izraz

        else:
            izraz = Izraz(desnaStrana[0][1])
            izraz.provjeri()

            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[2][1])
            izraz_pridruzivanja.provjeri()

            self.tip = izraz_pridruzivanja.getTip()

            return 0

class IzrazPridruzivanja(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<log_ili_izraz>":
            log_ili_izraz = LogIliIzraz(desnaStrana[0][1])
            l_izraz = log_ili_izraz.provjeri()
            
            self.tip = log_ili_izraz.getTip()
            
            return l_izraz

        else:
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()

            if l_izraz != 1:
                ispisGreske(desnaStrana)
            
            self.tip = postfiks_izraz.getTip()

            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[2][1])
            l_izraz = izraz_pridruzivanja.provjeri()
            
            tip2 = izraz_pridruzivanja.getTip()
            
            if not provjeriImplicitno(tip2,self.tip):
                ispisGreske(desnaStrana)

            return 0

class LogIliIzraz(IzrazPridruzivanja):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)
        if desnaStrana[0][0] == "<log_i_izraz>":
            log_i_izraz = LogIIzraz(desnaStrana[0][1])
            l_izraz = log_i_izraz.provjeri()
            self.tip = log_i_izraz.getTip()
            return l_izraz
        else:
            log_ili_izraz = LogIliIzraz(desnaStrana[0][1])
            l_izraz = log_ili_izraz.provjeri()

            self.tip = log_ili_izraz.getTip()

            if not provjeriImplicitno(self.tip,"int"):
                ispisGreske(desnaStrana)

            log_i_izraz = LogIIzraz(desnaStrana[2][1])
            log_i_izraz.provjeri()

            self.tip = log_i_izraz.getTip()

            if not provjeriImplicitno(self.tip,"int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class LogIIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<bin_ili_izraz>":
            bin_ili_izraz = BinIliIzraz(desnaStrana[0][1])
            l_izraz = bin_ili_izraz.provjeri()
            self.tip = bin_ili_izraz.getTip()
            return l_izraz

        else:
            log_i_izraz = LogIIzraz(desnaStrana[0][1])
            l_izraz = log_i_izraz.provjeri()
            self.tip = log_i_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            bin_ili_izraz = BinIliIzraz(desnaStrana[2][1])
            bin_ili_izraz.provjeri()

            self.tip = bin_ili_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class BinIliIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def asmIli(self):
        global trenutniRedIzlaza

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg1)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg2)+'\n')
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")

        file.write("OR R"+str(reg2)+", R"+str(reg1)+", R"+str(reg3)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+str(reg3)+'\n')
        trenutniRedIzlaza += 1

        zauzetostRegistara[reg1] = 0
        zauzetostRegistara[reg2] = 0
        zauzetostRegistara[reg3] = 0

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<bin_xili_izraz>":
            bin_xili_izraz = BinXiliIzraz(desnaStrana[0][1])
            l_izraz = bin_xili_izraz.provjeri()
            self.tip = bin_xili_izraz.getTip()
            return l_izraz

        else:
            bin_ili_izraz = BinIliIzraz(desnaStrana[0][1])
            l_izraz = bin_ili_izraz.provjeri()
            self.tip = bin_ili_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            bin_xili_izraz = BinXiliIzraz(desnaStrana[2][1])
            bin_xili_izraz.provjeri()

            self.tip = bin_xili_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"

            self.asmIli()

            return 0

class BinXiliIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def asmXIli(self):
        global trenutniRedIzlaza

        reg1 = nadiSlobodniRegistar()
        zauzetostRegistara[reg1] = 1
        reg2 = nadiSlobodniRegistar()
        zauzetostRegistara[reg2] = 1
        reg3 = nadiSlobodniRegistar()
        zauzetostRegistara[reg3] = 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg1)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg2)+'\n')
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")

        file.write("XOR R"+str(reg2)+", R"+str(reg1)+", R"+str(reg3)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+str(reg3)+'\n')
        trenutniRedIzlaza += 1

        zauzetostRegistara[reg1] = 0
        zauzetostRegistara[reg2] = 0
        zauzetostRegistara[reg3] = 0

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<bin_i_izraz>":
            bin_i_izraz = BinIIzraz(desnaStrana[0][1])
            l_izraz = bin_i_izraz.provjeri()
            self.tip = bin_i_izraz.getTip()
            return l_izraz

        else:
            bin_xili_izraz = BinXiliIzraz(desnaStrana[0][1])
            l_izraz = bin_xili_izraz.provjeri()
            self.tip = bin_xili_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            bin_i_izraz = BinIIzraz(desnaStrana[2][1])
            bin_i_izraz.provjeri()

            self.tip = bin_i_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"

            self.asmXIli()

            return 0

class BinIIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def asmI(self):
        global trenutniRedIzlaza

        reg1 = nadiSlobodniRegistar()
        zauzetostRegistara[reg1] = 1
        reg2 = nadiSlobodniRegistar()
        zauzetostRegistara[reg2] = 1
        reg3 = nadiSlobodniRegistar()
        zauzetostRegistara[reg3] = 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg1)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg2)+'\n')
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")

        file.write("AND R"+str(reg2)+", R"+str(reg1)+", R"+str(reg3)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+str(reg3)+'\n')
        trenutniRedIzlaza += 1

        zauzetostRegistara[reg1] = 0
        zauzetostRegistara[reg2] = 0
        zauzetostRegistara[reg3] = 0

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<jednakosni_izraz>":
            jednakosni_izraz = JednakosniIzraz(desnaStrana[0][1])
            l_izraz = jednakosni_izraz.provjeri()
            self.tip = jednakosni_izraz.getTip()
            return l_izraz

        else:
            bin_i_izraz = BinIIzraz(desnaStrana[0][1])
            l_izraz = bin_i_izraz.provjeri()
            self.tip = bin_i_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            jednakosni_izraz = JednakosniIzraz(desnaStrana[2][1])
            jednakosni_izraz.provjeri()

            self.tip = jednakosni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"

            self.asmI()

            return 0

class JednakosniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        global jeliFja

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<odnosni_izraz>":
            odnosni_izraz = OdnosniIzraz(desnaStrana[0][1])
            l_izraz = odnosni_izraz.provjeri()
            self.tip = odnosni_izraz.getTip()
            return l_izraz
        else:
            jednakosni_izraz = JednakosniIzraz(desnaStrana[0][1])
            l_izraz = jednakosni_izraz.provjeri()
            self.tip = jednakosni_izraz.getTip()

            if jeliFja:
                ispisGreske(desnaStrana)

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            odnosni_izraz = OdnosniIzraz(desnaStrana[2][1])
            odnosni_izraz.provjeri()
            self.tip = odnosni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class OdnosniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<aditivni_izraz>":
            aditivni_izraz = AditivniIzraz(desnaStrana[0][1])
            l_izraz = aditivni_izraz.provjeri()
            self.tip = aditivni_izraz.getTip()
            return l_izraz
        else:
            odnosni_izraz = OdnosniIzraz(desnaStrana[0][1])
            l_izraz = odnosni_izraz.provjeri()
            self.tip = odnosni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            aditivni_izraz = AditivniIzraz(desnaStrana[2][1])
            l_izraz = aditivni_izraz.provjeri()
            self.tip = aditivni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class AditivniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def asmzbroji(self,operator):
        global trenutniRedIzlaza

        reg1 = nadiSlobodniRegistar()
        zauzetostRegistara[reg1] = 1
        reg2 = nadiSlobodniRegistar()
        zauzetostRegistara[reg2] = 1
        reg3 = nadiSlobodniRegistar()
        zauzetostRegistara[reg3] = 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg1)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("POP R"+str(reg2)+'\n')
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")

        if operator == '+':
            file.write("ADD ")
        else:
            file.write("SUB ")
        file.write("R"+str(reg2)+", R"+str(reg1)+", R"+str(reg3)+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+str(reg3)+'\n')
        trenutniRedIzlaza += 1

        zauzetostRegistara[reg1] = 0
        zauzetostRegistara[reg2] = 0
        zauzetostRegistara[reg3] = 0

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<multiplikativni_izraz>":
            multiplikativni_izraz = MultiplikativniIzraz(desnaStrana[0][1])
            l_izraz = multiplikativni_izraz.provjeri()
            self.tip = multiplikativni_izraz.getTip()
            return l_izraz
        else:
            aditivni_izraz = AditivniIzraz(desnaStrana[0][1])
            l_izraz = aditivni_izraz.provjeri()
            self.tip = aditivni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            multiplikativni_izraz = MultiplikativniIzraz(desnaStrana[2][1])
            multiplikativni_izraz.provjeri()
            self.tip = multiplikativni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"

            op = izluciIDN(desnaStrana[1][0])

            self.asmzbroji(op)

            return 0

class MultiplikativniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<cast_izraz>":
            cast_izraz = CastIzraz(desnaStrana[0][1])
            l_izraz = cast_izraz.provjeri()
            self.tip = cast_izraz.getTip()
            return l_izraz
        else:
            multiplikativni_izraz = MultiplikativniIzraz(desnaStrana[0][1])
            l_izraz = multiplikativni_izraz.provjeri()
            self.tip = multiplikativni_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            cast_izraz = CastIzraz(desnaStrana[2][1])
            cast_izraz.provjeri()
            self.tip = cast_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class CastIzraz(MultiplikativniIzraz):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<unarni_izraz>":
            unarni_izraz = UnarniIzraz(desnaStrana[0][1])
            l_izraz = unarni_izraz.provjeri()
            self.tip = unarni_izraz.getTip()
            return l_izraz

        else:
            ime_tipa = ImeTipa(desnaStrana[1][1])
            self.tip = ime_tipa.provjeri()

            cast_izraz = CastIzraz(desnaStrana[3][1])
            l_izraz = cast_izraz.provjeri()

            castTip = cast_izraz.getTip()

            if not provjeriEksplicitno(castTip,self.tip):
                ispisGreske(desnaStrana)

            return 0

class UnarniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""

    def getTip(self):
        return self.tip

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<postfiks_izraz>":
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()
            self.tip = postfiks_izraz.getTip()
            return l_izraz

        elif desnaStrana[1][0] == "<unarni_izraz>":
            unarni_izraz = UnarniIzraz(desnaStrana[1][1])
            l_izraz = unarni_izraz.provjeri()
            self.tip = unarni_izraz.getTip()

            if l_izraz != 1:
                ispisGreske(desnaStrana)

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0
        else:
            unarni_operator = UnarniOperator(desnaStrana[0][1])
            unarni_operator.provjeri()

            cast_izraz = CastIzraz(desnaStrana[1][1])
            l_izraz = cast_izraz.provjeri()
            self.tip = cast_izraz.getTip()

            if not provjeriImplicitno(self.tip, "int"):
                ispisGreske(desnaStrana)

            self.tip = "int"
            return 0

class UnarniOperator(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        global trenutniOperator
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        trenutniOperator = izluciIDN(desnaStrana[0][0])

class PostfiksIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""
        self.ime = ""

    def getTip(self):
        return self.tip

    def getIme(self):
        return self.ime

    def xConstT(self,x):
        if x == "const(int)" or x == "const(char)":
            return 0
        else:
            return 1

    def asmVoid(self,imeFje):
        global trenutniRedIzlaza
        global vrijednostRegistara

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("CALL "+imeFje+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R6\n")
        trenutniRedIzlaza += 1

    def asmParametri(self,imeFje):
        global trenutniRedIzlaza

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("CALL "+imeFje+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R6\n")
        trenutniRedIzlaza += 1


    def provjeri(self):

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<primarni_izraz>":
            primarni_izraz = PrimarniIzraz(desnaStrana[0][1])
            l_izraz = primarni_izraz.provjeri()
            self.tip = primarni_izraz.getTip()
            self.ime = primarni_izraz.getIme()
            return l_izraz

        elif len(desnaStrana) == 2:
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()
            self.tip = postfiks_izraz.getTip()

            if l_izraz != 1:
                ispisGreske(desnaStrana)

            implicitno = provjeriImplicitno(self.tip,"int")

            if not implicitno:
                ispisGreske(desnaStrana)

            return 0

        elif desnaStrana[2][0] == "<izraz>":
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()
            self.tip = postfiks_izraz.getTip()

            provjera = provjeriNizX(self.tip)

            if not provjera:
                ispisGreske(desnaStrana)

            izraz = Izraz(desnaStrana[2][1])
            l_izraz = izraz.provjeri()
            tipTmp= izraz.getTip()

            if not provjeriImplicitno(tipTmp,"int"):
                ispisGreske(desnaStrana)

            self.tip = izvuciXizNiza(self.tip)

            return self.xConstT(self.tip)


        elif len(desnaStrana) == 3:
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()
            self.tip = postfiks_izraz.getTip()

            imeFje = postfiks_izraz.getIme()

            rezultat = jeliDeklariranoIgdje(imeFje)

            mjestoDeklaracije = rezultat[1]

            tipFje = listaTablica[mjestoDeklaracije][imeFje][1]
            parametar = listaTablica[mjestoDeklaracije][imeFje][2]

            if self.tip != tipFje:
                ispisGreske(desnaStrana)

            if parametar != "void":
                ispisGreske(desnaStrana)

            self.tip = tipFje

            self.asmVoid(imeFje)

            return 0

        elif desnaStrana[2][0] == "<lista_argumenata>":
            postfiks_izraz = PostfiksIzraz(desnaStrana[0][1])
            l_izraz = postfiks_izraz.provjeri()
            self.tip = postfiks_izraz.getTip()

            imeFje = postfiks_izraz.getIme()

            rezultat = jeliDeklariranoIgdje(imeFje)

            mjestoDeklaracije = rezultat[1]

            lista_argumenata = ListaArgumenata(desnaStrana[2][1])
            listaArgumenata = lista_argumenata.provjeri()

            tipFje = listaTablica[mjestoDeklaracije][imeFje][1]

            if len(listaTablica[mjestoDeklaracije][imeFje]) == 2:
                if listaTablica[mjestoDeklaracije][imeFje][1] != "void":
                    ispisGreske(desnaStrana)

            listaParametara = listaTablica[mjestoDeklaracije][imeFje][2]
            listaTipova = []


            if self.tip != tipFje:
                ispisGreske(desnaStrana)

            for element in listaParametara:
                listaTipova.append(element[0])

            i = 0
            n = len(listaArgumenata)

            if len(listaTipova) != len(listaArgumenata):
                ispisGreske(desnaStrana)

            while i < n:
                implicitno = provjeriImplicitno(listaArgumenata[i],listaTipova[i])
                if not implicitno:
                    ispisGreske(desnaStrana)
                i += 1


            self.tip = tipFje

            self.asmParametri(imeFje)

            return 0

class PrimarniIzraz(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tip = ""
        self.ime = ""

    def getTip(self):
        return self.tip

    def getIme(self):
        return self.ime

    def nadiBrojProdukcije(self,desnaStrana):

        if len(desnaStrana) == 3:
            return 5
        else:
            tmp = desnaStrana[0][0]
            tmp = list(tmp)
            for i in range(len(tmp)):
                if tmp[i] == ' ':
                    del tmp [i:]
                    break
            tmp = ''.join(tmp)
            if tmp == 'IDN':
                return 1
            elif tmp == 'BROJ':
                return 2
            elif tmp == 'ZNAK':
                return 3
            elif tmp == 'NIZ_ZNAKOVA':
                return 4

    def asmBroj(self,broj):
        global trenutniRedIzlaza
        global trenutniOperator

        broj = str(broj)
        trenRegistar = nadiSlobodniRegistar()

        if trenRegistar < 0:
            print "Nema slobodnih registara"
            exit(-1)

        if trenutniOperator == '+':
            operator = ''
        else:
            operator  = '-'

        #oznaci trenutni registar kao zauzet i daj mu vrijednost
        #zauzetostRegistara[trenRegistar] = 1
        #vrijednostRegistara[trenRegistar] = operator+broj

        trenRegistar = str(trenRegistar)
        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("MOVE %D "+operator+broj+", R"+trenRegistar+"\n")
        trenutniRedIzlaza += 1

        lbl = imaLiLabele(trenutniRedIzlaza)
        if not lbl:
            file.write("\t\t\t")
        file.write("PUSH R"+trenRegistar+"\n")
        trenutniRedIzlaza += 1

    def asmZnak(self,znak):
        print znak

    def provjeri(self):
        global jeliFja
        global BROJ
        global IME

        IME = ""

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        brojProdukcije = self.nadiBrojProdukcije(desnaStrana)

        if brojProdukcije == 1:
            idn = izluciIDN(desnaStrana[0][0])

            self.ime = idn
            IME = idn

            rezultat = jeliDeklariranoIgdje(idn)

            deklarirano = rezultat[0]
            mjestoDeklaracije = rezultat[1]

            jeliFja = 0

            if len(listaTablica[mjestoDeklaracije][idn]) == 3:
                jeliFja = 1

            if not deklarirano:
                ispisGreske(desnaStrana)
            rezultat = dohvatiTipIl_izraz(idn,mjestoDeklaracije)

            l_izraz = rezultat[0]
            self.tip = rezultat[1]

            return l_izraz

        elif brojProdukcije == 2:

            broj = izluciIDN(desnaStrana[0][0])

            if len(broj) >= 2:
                if broj[1] == 'x':
                    broj = int(broj, 16)

            broj=int(broj)

            if broj < -2147483648 or broj > 2147483647:
                ispisGreske(desnaStrana)

            self.tip = "int"

            if uFji:
                self.asmBroj(broj)
            else:
                BROJ = broj

            return 0

        elif brojProdukcije == 3:
            znak=izluciIDN(desnaStrana[0][0])

            self.tip = "char"

            if len(znak)==3:
                return 0

            elif len(znak)==4:
                if znak[1]=='\\':
                    if znak[2]=='t' or znak[2]=='n' or znak[2]=='0' or znak[2]=="'" or znak[2]=='"' or znak[2]=='\\':
                        return 0
                    else:
                        ispisGreske(desnaStrana)

            else:
                ispisGreske(desnaStrana)

            self.asmZnak(znak)

        elif brojProdukcije == 4:
            niz_znakova=izluciIDN(desnaStrana[0][0])

            self.tip = "niz(const(char))"
            n=len(niz_znakova)
            i=0
            while i<n:
                p69=0
                if niz_znakova[i]=='\\':
                    if i==n-1:
                        ispisGreske(desnaStrana)
                        p69=1
                        exit(1)
                    if p69==0:
                        if niz_znakova[i+1]!='t' and niz_znakova[i+1]!='n' and niz_znakova[i+1]!='0' and niz_znakova[i+1]!="'" and niz_znakova[i+1]!='"' and niz_znakova[i+1]!='\\':
                            ispisGreske(desnaStrana)
                            p69=1
                            exit(1)
                    i=i+1
                i=i+1

            if p69==0:
                return 0


        elif brojProdukcije == 5:
            izraz = Izraz(desnaStrana[1][1])
            l_izraz = izraz.provjeri()

            self.tip = izraz.getTip()

            return l_izraz

class ListaArgumenata(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.tipovi = []

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<izraz_pridruzivanja>":
            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[0][1])
            izraz_pridruzivanja.provjeri()

            tip = izraz_pridruzivanja.getTip()
            self.tipovi.append(tip)

            return self.tipovi

        else:
            lista_argumenata = ListaArgumenata(desnaStrana[0][1])
            self.tipovi = lista_argumenata.provjeri()

            izraz_pridruzivanja = IzrazPridruzivanja(desnaStrana[2][1])
            izraz_pridruzivanja.provjeri()

            tip = izraz_pridruzivanja.getTip()

            self.tipovi.append(tip)

            return self.tipovi

class DefinicijaFunkcije(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def asmLabela(self,lbl):
        global labele
        global trenutniRedIzlaza
        if lbl == "main":
            file.write("F_MAIN\t\t")
        else:
            file.write(lbl+"\t\t")

        labele[trenutniRedIzlaza] = lbl

    def provjeri(self):
        global uFji
        global imeTrenutneFunkcije

        uFji = 1

        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        ime_tipa = ImeTipa(desnaStrana[0][1])
        tip = ime_tipa.provjeri()

        konst = ime_tipa.jeKonst()

        if konst:
            ispisGreske(desnaStrana)

        idn = izluciIDN(desnaStrana[1][0])

        imeTrenutneFunkcije = idn

        rezultat = jeliDeklariranoIgdje(imeTrenutneFunkcije)

        mjestoDeklaracije = rezultat[1]

        #provjeri je li definirana
        if idn in listaTablica[mjestoDeklaracije]:
            definirana = listaTablica[mjestoDeklaracije][idn][0]
            if definirana:
                ispisGreske(desnaStrana)

        self.asmLabela(idn)

        #DO OVE TOCKE ISTO JE ZA OBE PRODUKCIJE

        if desnaStrana[3][0] == "<lista_parametara>":
            lista_parametara = ListaParametara(desnaStrana[3][1])
            listaParametara = lista_parametara.provjeri()

            zabiljeziDefinicijuFunkcije(idn,tip,listaParametara)

            slozena_naredba = SlozenaNaredba(desnaStrana[5][1])
            slozena_naredba.zabiljeziParametre(listaParametara)
            slozena_naredba.provjeri()

        else:
            #ako postoji deklaracija vec od prije, ova zabiljeska ce je prepisati
            zabiljeziDefinicijuFunkcije(idn,tip,"void")

            slozena_naredba = SlozenaNaredba(desnaStrana[5][1])
            slozena_naredba.provjeri()

        uFji = 0

class ImeTipa(SlozenaNaredba):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu
        self.konst = False

    def jeKonst(self):
        return self.konst

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        if desnaStrana[0][0] == "<specifikator_tipa>":
            specifikator_tipa = SpecifikatorTipa(desnaStrana[0][1])
            tip = specifikator_tipa.provjeri()
            return tip
        else:
            specifikator_tipa = SpecifikatorTipa(desnaStrana[1][1])
            tip = specifikator_tipa.provjeri()
            self.konst = True
            if tip == "void":
                ispisGreske(desnaStrana)
            else:
                return "const("+tip+")"

class SpecifikatorTipa(ImeTipa):

    def __init__(self,pozicijaUprogramu):
        self.pozicijaUprogramu = pozicijaUprogramu

    def provjeri(self):
        desnaStrana = nadiDesnuStranu(self.pozicijaUprogramu)

        tmp = desnaStrana[0][0]
        tmp = list(tmp)

        for i in range(len(tmp)):
            if tmp[i] == ' ':
                kraj = i
                break

        del tmp[kraj:]
        tip = ''.join(tmp)

        if tip == 'KR_VOID':
            return "void"
        elif tip == 'KR_CHAR':
            return "char"
        elif tip == 'KR_INT':
            return "int"

def ucitajUlaz():
    #cmdLine = list(sys.argv)
    #ulaz = open(cmdLine[1],"r")
    ulaz = open("test.in","r")
    #ulaz = sys.stdin
    listaPrograma = ulaz.readlines()

    #makni LF
    for i in range(len(listaPrograma)):
        listaPrograma[i] = listaPrograma[i].rstrip()
    return listaPrograma

def otvoriFileZaIzlaz():
    global trenutniRedIzlaza
    global labele
    global file

    file = open("b.frisc","w")
    inicijalniZapis = "\t\t\tMOVE 40000, R7\n\t\t\tCALL F_MAIN\n\t\t\tHALT\n\n"
    file.write(inicijalniZapis)
    trenutniRedIzlaza = 5

def parametriGeneratora():
    global trenutniRedIzlaza
    global labele
    global zauzetostRegistara
    global vrijednostRegistara
    global trenutniOperator
    global uFji
    global vrijednostLabele

    trenutniOperator = '+'
    uFji = 0
    trenutniRedIzlaza = 0

    #key je redak, a value je labela
    labele = {}

    #key je labela, a value vrijednost
    vrijednostLabele = {}

    zauzetostRegistara = {}
    vrijednostRegistara = {}
    for i in range(0,7):
        zauzetostRegistara[i] = 0
        vrijednostRegistara[i] = 0
    zauzetostRegistara[7] = 1
    vrijednostRegistara[7] = 40000

def main ():

    parametriGeneratora()

    global listaPrograma
    global aktualnaTablica
    global listaTablica
    global imeTrenutneFunkcije
    global uPetlji
    global jeliFja


    jeliFja = 0

    uPetlji = []

    #na pocetku nismo u niti jednoj petlji
    uPetlji.append(0)

    imeTrenutneFunkcije = ""

    aktualnaTablica = -1
    listaTablica = []

    stvoriTablicu()

    listaPrograma = ucitajUlaz()

    otvoriFileZaIzlaz()

    #stvori inicijalni objekt
    prijevodna_jedinica = PrijevodnaJedinica(0)
    prijevodna_jedinica.provjeri()

    rezultat = jeliDeklariranoIgdje("main")

    deklariranoMain = rezultat[0]
    mjestoDeklaracije = rezultat[1]

    #provjeri ima li maina
    if not deklariranoMain:
        print "main"
        exit(1)

    elif listaTablica[mjestoDeklaracije]["main"][0] != 1 or listaTablica[mjestoDeklaracije]["main"][1] != "int" or listaTablica[mjestoDeklaracije]["main"][2] != "void":
        print "main"
        exit(1)

    #provjeri jesu li sve funkcije definirane
    for tablica in listaTablica:
        for idn in tablica:
            if len(tablica[idn]) == 3:
                #znaci da je funkcija, a ne varijabla
                if tablica[idn][0] != 1:
                    print "funkcija"
                    exit(1)

if __name__ == '__main__':
  main()