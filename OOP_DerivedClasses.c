#include <iostream>
#include <string>
#include <cstring>
#include <stdlib.h> ///permite executia functiei system(...)
using namespace std;

///Clasa Data
class Data
{
private:
    int zi;
    char *luna = new char[10];
    int an;

public:
    friend class Angajat;
    friend class Part_Time;
    friend class Permanent;

    Data(int zi, const char* luna, int an);

    Data(const Data& data);

    ~Data();

    friend istream& operator>>(istream &in, Data& D); ///supraincarcare pe >>

    void citire(istream &in);

    friend ostream& operator<<(ostream &out, Data& D); ///supraincarcare pe <<

    void afisare(ostream &out);

    Data& operator=(Data &D); ///supraincarcarea operatorului de atribuire (doar ca metoda nu ca functie friend)
};

Data& Data::operator=(Data &D)
{
    zi = D.zi;
    strcpy(luna, D.luna);
    an = D.an;
    return *this;
}

void Data::citire(istream &in)
{
    cout << "Dati ziua: " << endl;
    in >> zi;
    cout << endl;

    cout << "Dati luna(scrisa cu litere mici): " << endl;
    cin >> luna;
    cout << endl;

	cout<<"Dati anul: ";
    cin >> an;
    cout << endl;
}

istream& operator>>(istream &in, Data& D)
{
        D.citire(in);
        return in;
}

void Data::afisare(ostream &out)
{
    //out << "Data este:" <<endl;
    out << zi << "." << luna << "." << an << endl;
}

ostream& operator<<(ostream &out, Data& D)
{
        D.afisare(out);
        return out;
}

Data::Data(int zi = 0, const char *luna = "0", int an = 0)
{
    this->zi = zi;
    strcpy(this->luna, luna);
    this->an = an;
}

Data::Data(const Data& data) {
    Data(data.zi, data.luna, data.an);
}

Data::~Data() {
    delete[] luna;
}


///Clasa Angajat
class Angajat
{
protected:
    string nume;
    string prenume;
    float salariu;
    Data data_angajare;

public:
    Angajat(string, string, float, Data);

    virtual ~Angajat() { };

    virtual void citire(istream &in);

    virtual void afisare(ostream &out);

    friend istream& operator>>(istream&, Angajat&);

    friend ostream& operator<<(ostream&, Angajat&);

};

void Angajat::citire(istream &in)
{
    cout << "Dati numele angajatului: ";
    in >> nume;
    cout << endl;

    cout << "Dati prenumele angajatului: ";
    in >> prenume;
    cout << endl;

	cout << "Dati salariul angajatului: ";
	in >> salariu;
    cout << endl;

	cout << "Dati data angajarii: "<<endl;
	in >> data_angajare;
    cout << endl;

}

istream& operator>>(istream &in, Angajat& A)
{
        A.citire(in);
        return in;
}

void Angajat::afisare(ostream &out)
{
    out << "Numele si prenumele angajatului: ";
    out << nume << " " << prenume << endl;
    out << "Salariul: ";
    out << salariu << endl;
    out << "Data angajarii: ";
    out << data_angajare <<endl;

}

ostream& operator<<(ostream &out, Angajat& A)
 {
        A.afisare(out);
        return out;
 }

Angajat::Angajat(string nume = "", string prenume = "", float salariu = 0, Data data_angajare = Data(0,"0",0))
{
    this->nume = nume;
    this->prenume = prenume;
    this->salariu = salariu;
    this->data_angajare = data_angajare;
}


///Clasa Part_Time
class Part_Time : public Angajat
{
private:
   int nr_ore_zi;
   Data final_contract;
   static int n1;

public:
     Part_Time(string, string ,float , Data, int, Data );

    ~Part_Time() = default;

    void citire(istream &in);

    void afisare(ostream &out);

    friend istream& operator>>(istream&, Part_Time&);

    friend ostream& operator<<(ostream&, Part_Time&);

    void salariu_part_time();

    static void numarObiecte() /// metoda statica de afisare a numarului de obiecte
        {cout<<n1;}
};

void Part_Time::salariu_part_time()
{ float  sal=salariu;
    if (final_contract.zi < 31 && strcmp(final_contract.luna, "decembrie") == 0 && final_contract.an == 2020)
      {
       cout<<"Salariul primit este: ";
       sal = (3 * sal) / 4;
       cout << sal << endl;
      }
    else
      {
       cout<<"Salariul primit este: ";
       cout << salariu << endl;
      }

}

int Part_Time::n1=0;
Part_Time::Part_Time(string nume = "", string prenume = "", float salariu = 0, Data data_angajare = Data(0,"0",0), int nr_ore_zi = 0, Data final_contract = Data(0, "0" ,0))
    : Angajat(nume, prenume, salariu, data_angajare)
{
    this->nr_ore_zi=nr_ore_zi;
    this->final_contract=final_contract;
    n1++;
}

void Part_Time::citire(istream &in)
{
    Angajat::citire(in);
    cout<<"Dati numarul de ore lucrate pe zi: "<<endl;
    in>>nr_ore_zi;
    cout<<"Dati data finalizarii contractului: "<<endl;
    in>>final_contract;
}

istream& operator>>(istream& in, Part_Time& PT)
{
    PT.citire(in);
    return in;
}

void Part_Time::afisare(ostream &out)
{
    Angajat::afisare(out);
    out<<"Numarul orelor lucrate pe zi: "<<endl;
    out<<nr_ore_zi<<endl;
    out<<"Data finalizarii contractului: "<<endl;
    out<<final_contract<<endl;
}

ostream& operator<<(ostream& out, Part_Time& PT)
{
    PT.afisare(out);
    return out;
}


///Clasa Permanent
class Permanent : public Angajat
{
private:
   int nr_minori_intretinere;

public:
     Permanent(string, string ,float , Data, int );

    ~Permanent() = default;

    void citire(istream &in);

    void afisare(ostream &out);

    friend istream& operator>>(istream&, Permanent&);

    friend ostream& operator<<(ostream&, Permanent&);

    void salariu_permanent();
};

void Permanent::salariu_permanent()
{
    int n = 2020 - data_angajare.an;
    float bonus = 0;
    int nrmin=nr_minori_intretinere;
    while (nrmin != 0)
    {
        bonus += (n * salariu) / 100;
        nrmin--;
    }

     float  salariufin=salariu+bonus;
     cout<<"Salariul+bonusul: ";
     cout<<salariufin<<endl;
}

Permanent::Permanent(string nume = "", string prenume = "", float salariu = 0, Data data_angajare = Data(0,"0",0), int nr_minori_intretinere=0 )
    : Angajat(nume, prenume, salariu, data_angajare)
{
    this->nr_minori_intretinere=nr_minori_intretinere;
}

void Permanent::citire(istream &in)
{
    Angajat::citire(in);
    cout << "Dati numarul de minori pentru intretinere: " << endl;
    in >> nr_minori_intretinere;
}

istream& operator>>(istream& in,Permanent& P)
{
    P.citire(in);
    return in;
}

void Permanent::afisare(ostream &out)
{
    Angajat::afisare(out);
    out << "Numarul de minori este: " ;
    out << nr_minori_intretinere << endl;
}

ostream& operator<<(ostream& out, Permanent& P)
{
    P.afisare(out);
    return out;
}


void menu_output()
{
    cout<<" Baltatescu Elena-Ecaterina Grupa 211 - Proiect - Tema 3: "<<endl;
    cout<<" MENIU: "<<endl;
    cout<<"===========================================";
    cout<<endl;
    cout<<"1. Cititi un angajat part_time: "<<endl;
    cout<<"2. Cititi un angajat permanent: "<<endl;
    cout<<"3. Afisati angajatul permanent si salariul+bonusul acestuia:"<<endl;
    cout<<"4. Afisati angajatul part_time si salariul acestuia: "<<endl;
    cout<<"5. Calculati numarul de angajati part_time cititi: "; cout<<endl;
    cout<<"0. Iesire."; cout<<endl;
}


void menu()
{
    int option; ///optiunea aleasa din meniu
    option=0;
    Permanent P;
    Part_Time PT;
    int ok1=0;///verifica daca a fost introdus un angajat part_time
    int ok2=0;///verifica daca a fost introdus un angajat permanent

    do
    {
        menu_output();

        cout<< " Introduceti numarul actiunii: ";
        cin>>option;

        if (option==1)
        {
            cin>>PT;
            ok1=1;
        }

        if (option==2)
        {
            cin>>P;
            ok2=1;
        }

        if (option==3)
        {
            if(ok2!=0)
            {
             P.salariu_permanent();
             cout<<P;
            }
            else
                cout<<"Nu ati introdus niciun angajat permanent"<<endl;
        }

        if (option==4)
        {
           if(ok1!=0)
           {
            PT.salariu_part_time();
            cout<<PT;
           }
            else
                cout<<"Nu ati introdus niciun angajat part_time"<<endl;
        }

        if (option==5)
        {
           cout<<"Numarul de angajati part_time introdusi: ";
           Part_Time::numarObiecte();
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

        ///downcast(nu il folosesc), le-am comentat deoarece imi incurca calcularea numarului de angajati
        ///Part_Time *pt=(Part_Time*)new Angajat;
        ///Permanent *p=(Permanent*)new Angajat;
    }
    while(option!=0);
}

int main()
{
    menu();
    return 0;
}


