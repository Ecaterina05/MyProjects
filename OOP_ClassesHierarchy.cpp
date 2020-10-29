#include <unordered_map>
#include <iostream>
#include <list>
#include <stdlib.h>
#include <cstring>
using namespace std;

///clasa data
class Data
{
private:
    int zi;
    string luna;
    int an;

public:
    friend class Cont;
    friend class Istoric;
    Data( int , string , int );
    ~Data() { };
    friend istream& operator>>(istream &in, Data& D); ///supraincarcare pe >>
    void citire(istream &in);
    friend ostream& operator<<(ostream &out, Data& D); ///supraincarcare pe <<
    void afisare(ostream &out);
    Data& operator=(Data &D); ///supraincarcarea operatorului de atribuire (doar ca metoda nu ca functie friend)
};

Data& Data::operator=(Data &D)
{
    zi=D.zi;
    luna=D.luna;
    an=D.an;
}

void Data::citire(istream &in)
{
    cout<<"Dati ziua: "<<endl;
    in>>zi;

    cout<<"Dati luna: "<<endl;
    in>>luna;

    cout<<"Dati anul: "<<endl;
    in>>an;

}

istream& operator>>(istream &in, Data& D)
{
    D.citire(in);
    return in;
}

void Data::afisare(ostream &out)
{
    //out<<"Data este:"<<endl;
    out<<zi<<"."<<luna<<"."<<an<<endl;

}

ostream& operator<<(ostream &out, Data& D)
{
    D.afisare(out);
    return out;

}

Data::Data( int zi=0, string luna="", int an=0 )
{
    this->zi=zi;
    this->luna=luna;
    this->an=an;
}

///clasa cont bancar
class Cont
{
protected:
    string nume_det;
    string prenume_det;
    Data data_deschidere;
    int sold;

public:
    Cont( string, string, Data, int );
    virtual ~Cont() {}; ///destructor virtual
    virtual void citire(istream &in);
    virtual void afisare(ostream &out);
    friend istream& operator>>(istream&, Cont&);
    friend ostream& operator<<(ostream&, Cont&);
    void exceptions();

};

void Cont::exceptions()
{
    try
    {
        int sold_eronat=-25;
        if(sold>0)
            cout<<"Banii au fost alocati in cont"<<endl;
        else
            throw(sold_eronat);

    }

    catch(int mySold)
    {
        cout<<"Nu puteti aloca un numar negativ de bani"<<endl;
        cout<<"Banii pe care ii doriti alocati: "<<mySold<<endl;
    }

}

Cont::Cont(string nume_det="", string prenume_det="", Data data_deschidere=Data(0,"",0), int sold=0)
{
    this->nume_det=nume_det;
    this->prenume_det=prenume_det;
    this->data_deschidere=data_deschidere;
    this->sold=sold;

}

void Cont::citire(istream &in)
{
    cout<<"Dati numele detinatorului contului: ";
    in>>nume_det;

    cout<<"Dati prenumele detinatorului contului: ";
    in>>prenume_det;

    cout<<"Dati data deschiderii contului: ";
    cout<<endl;
    in>>data_deschidere;

    cout<<"Dati soldul contului: ";
    in>>sold;

}

istream& operator>>(istream &in, Cont& C)
{
    C.citire(in);
    return in;
}

void Cont::afisare(ostream &out)
{
    out<<"Numele si prenumele detinatorului contului: "<<endl;
    out<<nume_det<<" "<<prenume_det<<endl;
    out<<"Data deschiderii contului: "<<endl;
    out<<data_deschidere;
    out<<"Soldul contului: "<<endl;
    out<<sold<<endl;

}

ostream& operator<<(ostream &out, Cont& C)
{
    C.afisare(out);
    return out;

}


///Clasa pentru istoricul soldurilor
class Istoric
{
private:
    Data data_curenta;
    int sold_curent;

public:
    friend class Economii;
    Istoric( Data , int );
    ~Istoric() {};
    friend istream& operator>>(istream &in, Istoric& ); ///supraincarcare pe >>
    void citire(istream &in);
    friend ostream& operator<<(ostream &out, Istoric& ); ///supraincarcare pe <<
    void afisare(ostream &out);
    Istoric& operator=(Istoric &I);
};

void Istoric::citire(istream &in)
{
    cout<<"Dati soldul : ";
    in>>sold_curent;

    cout<<" pe data de : ";
    cout<<endl;
    in>>data_curenta;
}

istream& operator>>(istream &in, Istoric& I)
{
    I.citire(in);
    return in;
}

void Istoric::afisare(ostream &out)
{
    out<<"Soldul  este: ";
    out<<sold_curent;
    out<<"  pe data de: ";
    out<<data_curenta;

}

ostream& operator<<(ostream &out, Istoric& I)
{
    I.afisare(out);
    return out;

}

Istoric::Istoric( Data data_curenta=Data(0,"",0), int sold_curent=0 )
{
    this->data_curenta=data_curenta;
    this->sold_curent=sold_curent;
}

Istoric& Istoric::operator=(Istoric &I)
{
    data_curenta=I.data_curenta;
    sold_curent=I.sold_curent;
}

list<Istoric> defaultList()
{
    Istoric Is;
    list<Istoric> temp;
    temp.push_back(Is);
    return temp;
}

///clasa cont economii
class Economii:public Cont
{
private:
    int rata;
    list<Istoric> ist;

public:
    friend class Curent;
    Economii( string, string ,Data , int, int, list<Istoric> );
    ~Economii() {};

    void citire(istream &in);
    void afisare(ostream &out);

    friend istream& operator>>(istream&, Economii&);
    friend ostream& operator<<(ostream&, Economii&);
    int rata_dobanda1();

};

int Economii::rata_dobanda1()
{
    if(rata==1)
        return 1;
    else
        return 0;
}

Economii::Economii(string nume_det="", string prenume_det="", Data data_deschidere=Data(0,"",0), int sold=0, int rata=0,
                   list<Istoric> is=defaultList()):Cont(nume_det,prenume_det,data_deschidere,sold)
{
    this->rata=rata;
    list<Istoric>::iterator i;
    for (i = is.begin(); i != is.end(); ++i)
        ist.push_back(*i);

}

void Economii::citire(istream &in)
{
    Cont::citire(in);
    cout<<"Dati rata ( 3, 6 sau 1 ): ";
    in>>rata;
    int n;
    cout<<"Dati numarul a cate date si solduri vreti pentru a forma istoricul: ";
    in>>n;
    cout<<"Dati istoricul contului: ";
    cout<<endl;
    while(n!=0)
    {
        Istoric I;
        in>>I;
        ist.push_back(I);
        n--;
    }
}

istream& operator>>(istream &in, Economii& E)
{
    E.citire(in);
    return in;
}

void Economii::afisare(ostream &out)
{
    Cont::afisare(out);
    if(rata==3)
        out<<"Rata este de 3 luni. "<<endl;
    if(rata==6)
        out<<"Rata este de 6 luni. "<<endl;
    if(rata==1)
        out<<"Rata este de 1 an. "<<endl;
    if(rata!=3 && rata!=6 && rata!=1)
        out<<"Ati introdus o rata invalida. "<<endl;

    out<<"Istoricul contului este: "<<endl;
    out<<endl;
    list<Istoric>::iterator i;
    for (i = ist.begin(); i != ist.end(); ++i)
        out<<(*i)<<endl;

}

ostream& operator<<(ostream &out, Economii& E)
{
    E.afisare(out);
    return out;

}


list<string> defaultList2()
{
    list<string> temp2;
    temp2.push_back("***");
    return temp2;
}

///clasa cont curent
class Curent:public Cont
{
private:
    int nr_tranzactii_gratuite;
    list<string> actiuni;
public:
    Curent( string, string ,Data , int, int, list<string> );
    ~Curent() {};

    void citire(istream &in);
    void afisare(ostream &out);

    friend istream& operator>>(istream&, Curent&);
    friend ostream& operator<<(ostream&, Curent&);
    void afisare2();

};

Curent::Curent(string nume_det="", string prenume_det="", Data data_deschidere=Data(0,"",0), int sold=0, int nr_tranzactii_gratuite=0, list<string> a=defaultList2())
        :Cont(nume_det,prenume_det,data_deschidere,sold)
{
    this->nr_tranzactii_gratuite=nr_tranzactii_gratuite;

    list<string>::iterator i;
    for (i = a.begin(); i != a.end(); ++i) {
        actiuni.push_back(*i);
    }
    if (*actiuni.begin() == "***")
        actiuni.pop_front();

}

void Curent::citire(istream &in)
{
    Cont::citire(in);
    unordered_map<int, list<string>> umap;

    cout<<"Dati nr de tranzactii gratuite: ";
    in>>nr_tranzactii_gratuite;

    string actiune;
    cout<<"Dati actiunile pe care le veti face asupra contului: "<<endl;
    cout<<"Optiunile: depunere, retragere, cumparare_online. "<<"Apasati 'x' cand ati terminat de introdus optiunile. "<<endl;

    string s="x";
    while(actiune!=s)
    {
        in>>actiune;
        actiuni.push_back(actiune);
    }

    actiuni.pop_back();

    static int i=0;
    umap[i]=actiuni;
    i++;
}

istream& operator>>(istream &in, Curent& Cu)
{
    Cu.citire(in);
    return in;
}

void Curent::afisare(ostream &out)
{
    Cont::afisare(out);
    out<<"Nr de tranzactii gratuite este: ";
    out<<nr_tranzactii_gratuite<<endl;

    out<<"Actiunile facute asupra contului sunt: "<<endl;
    list<string>::iterator i;
    for (i = actiuni.begin(); i != actiuni.end(); ++i)
        out<<(*i)<<", ";
    out<<endl;

    for (i = actiuni.begin(); i != actiuni.end(); ++i)
    {
        if((*i)=="depunere")
            out<<"Depunerea este gratuita."<<endl;

        if((*i)=="retragere" && nr_tranzactii_gratuite!=0)
        {
            out<<"Retragerea este gratuita, nr de tranzactii gratuite nu a fost depasit."<<endl;
            nr_tranzactii_gratuite--;
        }

        if((*i)=="retragere" && nr_tranzactii_gratuite==0)
            out<<"Retragerea costa, nr de tranzactii gratuite a fost depasit."<<endl;

        if((*i)=="cumparare_online")
            out<<"Cumpararea online a fost taxata."<<endl;
    }

}

ostream& operator<<(ostream &out, Curent& Cu)
{
    Cu.afisare(out);
    return out;

}

void Curent::afisare2()
{
    unordered_map<int, list<string>> umap;
    unordered_map<int, list<string>>:: iterator itr;
    cout<<"Id-urile conturilor curente si operatiunile facute pe fiecare sunt: "<<endl;

    for (itr = umap.begin(); itr != umap.end(); itr++)
    {
        cout << (itr->first) << "   :";
        list<string>::iterator i;
        for (i = (itr->second).begin(); i != (itr->second).end(); ++i)
            cout<<(*i)<<", ";
        cout<<endl;
    }
}


///meniul
void menu_output()
{
    cout<<" Baltatescu Elena-Ecaterina Grupa 211 - Proiect 3 - Tema 7: "<<endl;
    cout<<" MENIU: "<<endl;
    cout<<"===========================================";
    cout<<endl;
    cout<<"1. Deschideti un cont obisnuit: "; cout<<endl;
    cout<<"2. Deschideti un cont de economii: "; cout<<endl;
    cout<<"3. Deschideti un cont curent: "; cout<<endl;
    cout<<"4. Afisati id-urile conturilor curente si operatiunile facute asupra lor: "; cout<<endl;
    cout<<"5. Afisati conturile de economii cu rata de 1 an: "; cout<<endl;
    cout<<"0. Iesire."; cout<<endl;
}

void menu()
{
    int option; ///optiunea aleasa din meniu
    option=0;
    int ok=0;
    Cont C;
    Economii E;
    Curent Cu;
    list<Economii> rata1;

    do
    {
        menu_output();

        cout<< " Introduceti numarul actiunii: ";
        cin>>option;

        if (option==1)
        {
            cin>>C;
            C.exceptions();
            cout<<"Contul introdus este: "<<endl;
            cout<<C;
        }

        if (option==2)
        {
            cin>>E;
            E.exceptions();
            cout<<"Contul introdus este: "<<endl;
            cout<<E;
            int ok= E.rata_dobanda1();
            if(ok==1)
                rata1.push_back(E);

        }

        if (option==3)
        {
            cin>>Cu;
            Cu.exceptions();
            cout<<"Contul introdus este: "<<endl;
            cout<<Cu;
            ok=1;
        }

        if (option==4)
        {
            if(ok==1)
                Cu.afisare2();
            else
                cout<<"Nu ati deschis niciun cont curent.";
        }

        if (option==5)
        {
            list<Economii>::iterator i;
            for (i = rata1.begin(); i != rata1.end(); ++i)
                cout<<(*i)<<endl;
        }

        if (option==0)
        {
            cout<<"EXIT!"<<endl;
        }

        if (option<0||option>5)
        {
            cout<<"Selectie invalida"<<endl;
        }
        cout<<endl;
        system("pause"); ///Pauza - Press any key to continue...
        system("cls");   ///Sterge continutul curent al consolei
    }
    while(option!=0);
}

int main()
{
    menu();
    return 0;
}


