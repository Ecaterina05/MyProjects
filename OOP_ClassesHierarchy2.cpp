#include <unordered_map>
#include <iostream>
#include <list>
#include <vector>
#include <stdlib.h>
#include <cstring>
using namespace std;

///Clasa Persoana
class Persoana
{
protected:
    int id;
    string nume;

public:
    Persoana(int, string);
    virtual ~Persoana() { };
    Persoana(const Persoana&);

    virtual void citire(istream &in);
    friend istream& operator>>(istream& in, Persoana&);

    virtual void afisare(ostream &out);
    friend ostream& operator<<(ostream& out, Persoana&);

    virtual Persoana& operator=(Persoana &P);

    ///getteri pt id si nume
    int getID()
    {
        return id;
    }

    string getNume()
    {
        return nume;
    }

};

Persoana::Persoana(int id=0, string nume="")
{
    this->id=id;
    this->nume=nume;
}

Persoana::Persoana(const Persoana &P)
{
    this->id=P.id;
    this->nume=P.nume;
}

void Persoana::citire(istream &in)
{
    cout<<"Dati id-ul persoanei: "<<endl;
    in>>id;
    cout<<"Dati numele persoanei: "<<endl;
    in>>nume;
}

istream& operator>>(istream& in, Persoana& P)
{
    P.citire(in);
    return in;
}

void Persoana::afisare(ostream &out)
{
    out<<"Id-ul persoanei cu numele "<<nume<<" este: "<<id<<endl;
}

ostream& operator<<(ostream& out, Persoana& P)
{
    P.afisare(out);
    return out;
}

Persoana& Persoana::operator=(Persoana &P)
{
   this->id=P.id;
   this->nume=P.nume;
}

///Clasa Abonat
class Abonat: public Persoana
{
protected:
    string numar_telefon;

public:
    Abonat(int, string, string);
    virtual ~Abonat() { };
    Abonat(const Abonat&);

    virtual void citire(istream &in);
    friend istream& operator>>(istream& in, Abonat&);

    virtual void afisare(ostream &out);
    friend ostream& operator<<(ostream& out, Abonat&);

    virtual Abonat& operator=(const Abonat &A);
    void exceptions();
};

void Abonat::exceptions()
{
    try
    {
        int ok=1;

        for(int i=0;i<numar_telefon.size();i++)
            if(numar_telefon[i]!='0' && numar_telefon[i]!='1' && numar_telefon[i]!='2' && numar_telefon[i]!='3' && numar_telefon[i]!='4'
               && numar_telefon[i]!='5' && numar_telefon[i]!='6' && numar_telefon[i]!='7' && numar_telefon[i]!='8' && numar_telefon[i]!='9')
                ok=0;

            if(ok==1)
            cout<<"Numarul de telefon a fost introdus corect."<<endl;
            else
            throw(numar_telefon);

    }

    catch(string myNumber)
    {
        cout<<"Nu puteti avea decat cifre in numarul de telefon."<<endl;
        cout<<"Numarul pe care doriti sa il introduceti: "<<myNumber<<endl;
    }

}

Abonat::Abonat(int id=0, string nume="", string numar_telefon=""):Persoana(id, nume)
{
    this->numar_telefon=numar_telefon;
}

Abonat::Abonat(const Abonat &A):Persoana(A)
{
    this->numar_telefon=A.numar_telefon;
    this->id=A.id;
    this->nume=A.nume;
}

Abonat& Abonat::operator=(const Abonat &A)
{
    this->numar_telefon=A.numar_telefon;
    this->id=A.id;
    this->nume=A.nume;
}

void Abonat::citire(istream &in)
{
    Persoana::citire(in);
    cout<<"Dati numarul de telefon: "<<endl;
    in>>numar_telefon;
}

istream& operator>>(istream& in, Abonat& A)
{
    A.citire(in);
    return in;
}

void Abonat::afisare(ostream &out)
{
    Persoana::afisare(out);
    out<<"Numarul de telefon este: "<<numar_telefon<<endl;

}

ostream& operator<<(ostream& out, Abonat& A)
{
    A.afisare(out);
    return out;

}

///Clasa Abonat_Skype
class Abonat_Skype: public Abonat
{
protected:
    string id_skype;

public:
    Abonat_Skype(int, string, string, string);
    virtual ~Abonat_Skype() { };
    Abonat_Skype(const Abonat_Skype&);

    virtual void citire(istream &in);
    friend istream& operator>>(istream& in, Abonat_Skype&);

    virtual void afisare(ostream &out);
    friend ostream& operator<<(ostream& out, Abonat_Skype&);

    virtual Abonat_Skype& operator=(const Abonat_Skype &S);
};

Abonat_Skype::Abonat_Skype(int id=0, string nume="", string numar_telefon="", string id_skype="" ):Abonat(id, nume, numar_telefon)
{
    this->id_skype=id_skype;
}

Abonat_Skype::Abonat_Skype(const Abonat_Skype &S):Abonat(S)
{
    this->numar_telefon=S.numar_telefon;
    this->id=S.id;
    this->nume=S.nume;
    this->id_skype=S.id_skype;
}

void Abonat_Skype::citire(istream &in)
{
    Abonat::citire(in);
    cout<<"Dati id-ul de skype al abonatului: "<<endl;
    in>>id_skype;
}

istream& operator>>(istream& in, Abonat_Skype& S)
{
    S.citire(in);
    return in;
}

void Abonat_Skype::afisare(ostream &out)
{
    Abonat::afisare(out);
    out<<"Id-ul de skype al abonatului este: "<<id_skype<<endl;
}

ostream& operator<<(ostream& out, Abonat_Skype& S)
{
    S.afisare(out);
    return out;
}

Abonat_Skype& Abonat_Skype::operator=(const Abonat_Skype &S)
{
    this->numar_telefon=S.numar_telefon;
    this->id=S.id;
    this->nume=S.nume;
    this->id_skype=S.id_skype;
}

///Clasa Abonat_Skype_Romania

class Abonat_Skype_Romania: public Abonat_Skype
{
private:
    string adresa_email;

public:
    Abonat_Skype_Romania(int, string, string, string, string);
    ~Abonat_Skype_Romania() { };
    Abonat_Skype_Romania(const Abonat_Skype_Romania&);

    void citire(istream &in);
    friend istream& operator>>(istream& in, Abonat_Skype_Romania&);

    void afisare(ostream &out);
    friend ostream& operator<<(ostream& out, Abonat_Skype_Romania&);

    Abonat_Skype_Romania& operator=(const Abonat_Skype_Romania &R);
};

Abonat_Skype_Romania::Abonat_Skype_Romania(int id=0, string nume="", string numar_telefon="", string id_skype="", string adresa_email=""):
    Abonat_Skype(id, nume, numar_telefon, id_skype)
{
    this->adresa_email=adresa_email;
}

Abonat_Skype_Romania::Abonat_Skype_Romania(const Abonat_Skype_Romania &R):Abonat_Skype(R)
{
    this->numar_telefon=R.numar_telefon;
    this->id=R.id;
    this->nume=R.nume;
    this->id_skype=R.id_skype;
    this->adresa_email=R.adresa_email;
}

void Abonat_Skype_Romania::citire(istream &in)
{
    Abonat_Skype::citire(in);
    cout<<"Dati adresa de email: "<<endl;
    in>>adresa_email;
}

istream& operator>>(istream& in, Abonat_Skype_Romania& R)
{
    R.citire(in);
    return in;
}

void Abonat_Skype_Romania::afisare(ostream &out)
{
    Abonat_Skype::afisare(out);
    out<<"Adresa de email este: "<<adresa_email<<endl;
}

ostream& operator<<(ostream &out, Abonat_Skype_Romania& R)
{
    R.afisare(out);
    return out;
}

Abonat_Skype_Romania& Abonat_Skype_Romania::operator=(const Abonat_Skype_Romania &R)
{
    this->numar_telefon=R.numar_telefon;
    this->id=R.id;
    this->nume=R.nume;
    this->id_skype=R.id_skype;
    this->adresa_email=R.adresa_email;
}

///Clasa Abonat_Skype_Extern

class Abonat_Skype_Extern: public Abonat_Skype
{
private:
    string tara;

public:
    Abonat_Skype_Extern(int, string, string, string, string);
    ~Abonat_Skype_Extern() { };
    Abonat_Skype_Extern(const Abonat_Skype_Extern&);

    void citire(istream &in);
    friend istream& operator>>(istream& in, Abonat_Skype_Extern&);

    void afisare(ostream &out);
    friend ostream& operator<<(ostream& out, Abonat_Skype_Extern&);

    Abonat_Skype_Extern& operator=(const Abonat_Skype_Extern &E);
};

Abonat_Skype_Extern::Abonat_Skype_Extern(int id=0, string nume="", string numar_telefon="", string id_skype="", string tara=""):
    Abonat_Skype(id, nume, numar_telefon, id_skype)
{
    this->tara=tara;
}

Abonat_Skype_Extern::Abonat_Skype_Extern(const Abonat_Skype_Extern &E):Abonat_Skype(E)
{
    this->numar_telefon=E.numar_telefon;
    this->id=E.id;
    this->nume=E.nume;
    this->id_skype=E.id_skype;
    this->tara=E.tara;
}

void Abonat_Skype_Extern::citire(istream &in)
{
    Abonat_Skype::citire(in);
    cout<<"Dati tara abonatului: "<<endl;
    in>>tara;
}

istream& operator>>(istream& in, Abonat_Skype_Extern& E)
{
    E.citire(in);
    return in;
}

void Abonat_Skype_Extern::afisare(ostream &out)
{
    Abonat_Skype::afisare(out);
    out<<"Tara abonatului este: "<<tara<<endl;
}

ostream& operator<<(ostream &out, Abonat_Skype_Extern& E)
{
    E.afisare(out);
    return out;
}

Abonat_Skype_Extern& Abonat_Skype_Extern::operator=(const Abonat_Skype_Extern &E)
{
    this->numar_telefon=E.numar_telefon;
    this->id=E.id;
    this->nume=E.nume;
    this->id_skype=E.id_skype;
    this->tara=E.tara;
}

///Clasa Agenda

vector <Abonat_Skype> defaultVector()
{
    Abonat_Skype A;
    vector<Abonat_Skype> temp;
    temp.push_back(A);
    return temp;
}

class Agenda
{
private:
    vector<Abonat_Skype> ag;

public:
     Agenda( vector<Abonat_Skype> );
    ~Agenda() { };
    Agenda(const Agenda&);

    void FillAgenda();
    void afisareAgenda();
    string& operator[](int);
};

Agenda::Agenda( vector<Abonat_Skype> age=defaultVector())
{
    for(int i=1; i<age.size(); i++)
    ag.push_back(age[i]);
}

Agenda::Agenda(const Agenda &AG)
{
    for(int i=0; i<ag.size(); i++)
        ag.push_back(AG.ag[i]);
}

void Agenda::FillAgenda()
{
    int option=0;
    cout<<"Pentru a introduce abonati in agenda, introduceti: "<<endl;
    cout<<"1 (Pentru a introduce un abonat skype din Romania) "<<endl;
    cout<<"2 (Pentru a introduce un abonat skype extern) "<<endl;
    cin>>option;

    if(option==1)
    {
        Abonat_Skype_Romania R;
        cin>>R;
        ag.push_back(R);
    }

    if(option==2)
    {
        Abonat_Skype_Extern E;
        cin>>E;
        ag.push_back(E);
    }

    if(option<1 || option>2)
        cout<<"Selectie invalida"<<endl;

}

void Agenda::afisareAgenda()
{
    cout<<"Abonatii din agenda sunt: "<<endl;
    for(int i=0; i<ag.size(); i++)
    {
        cout<<ag[i]<<endl;
        ag[i].exceptions();
    }
}

string& Agenda::operator[](int idul)
    {
        string numele;
        for(int i=1;i<ag.size();i++)
            if(idul==ag[i].getID())
                numele=ag[i].getNume();
                return numele;
    }


void menu_output()
{
    cout<<" MENIU: "<<endl;
    cout<<"===========================================";
    cout<<endl;
    cout<<"1. Introduceti date in agenda de abonati:"; cout<<endl;
    cout<<"2. Afisati agenda de abonati:"; cout<<endl;
    cout<<"3. Aflati numele abonatilor dupa id. "<<endl;
    cout<<"0. Iesire."; cout<<endl;
}

void menu()
{
    int option; ///optiunea aleasa din meniu
    option=0;
    Agenda AG;

    do
    {
        menu_output();

        cout<< " Introduceti numarul actiunii: ";
        cin>>option;

        if (option==1)
        {
            int nr;
            cout<<"Dati numarul de abonati pe care vreti sa ii introduceti: "<<endl;
            cin>>nr;
            while(nr!=0)
            {
                AG.FillAgenda();
                nr--;
            }

        }

        if (option==2)
        {
            AG.afisareAgenda();
        }

        if (option==3)
        {
            cout<<"Dati id-ul angajatului pentru a afla numele lui: "<<endl;
            int idul;
            cin>>idul;
            cout<<AG[idul];
        }

        if (option==0)
        {
            cout<<"EXIT!"<<endl;
        }

        if (option<0||option>3)
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
