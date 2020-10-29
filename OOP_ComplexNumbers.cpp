#include <iostream>
#include <string>
#include <cstring>
#include <math.h>
#include <list>
#include <stdlib.h> ///permite executia functiei system(...)
using namespace std;

///Clasa Numar Complex
class Complex
{
private:
    double re;
    double im;

public:
    friend class VectorC;
    Complex(double , double );
    Complex(const Complex&); ///constructor de copiere
    ~Complex() {}; ///destructor

    ///setter and getter
    void setRe(int r){
        re=r;
    }

    int getRe(){
        return re;
    }

     void setIm(int i){
        im=i;
    }

    int getIm(){
        return im;
    }
    ///

    void citire(istream &in);
    friend istream& operator>>(istream &in, Complex& C); ///supraincarcare pe >>

    void afisare(ostream &out);
    friend ostream& operator<<(ostream &out, Complex& C); ///supraincarcare pe <<

    void modul_Complex(double &modul);
    friend Complex& operator+(Complex& C1, Complex& C2);
    friend Complex& operator*(Complex& C1, Complex& C2);
    friend Complex& operator/(Complex& C1, Complex& C2);

};

Complex::Complex(double re=0, double im=0) {
    this->re=re;
    this->im=im;
}

Complex::Complex(const Complex& C){
    this->re = C.re;
    this->im = C.im;
}

void Complex::citire(istream &in)
{
    cout<<"Dati partea reala: "<<endl;
    in>>re;
    cout<<"Dati partea imaginara: "<<endl;
    in>>im;
}

istream& operator>>(istream &in, Complex& C)
{
    C.citire(in);
    return in;
}

void Complex::afisare(ostream &out)
{
    out<<"Partea reala este: "<<re;
    out<<endl;
    out<<"Partea imaginara este: "<<im;
    out<<endl;
    out<<"i*(partea reala) este: i*"<<re;
    out<<endl;
    out<<"-i*(partea reala) este: -i*"<<re;
    out<<endl;
    out<<"Numarul complex este: "<<re<<"+i*"<<im;
    out<<endl;
    out<<"Numarul complex conjugat este: "<<re<<"-i*"<<im;
    out<<endl;
}

ostream& operator<<(ostream &out, Complex& C)
{
        C.afisare(out);
        return out;
}

void Complex::modul_Complex(double &modul)
{
    modul=sqrt(re*re+im*im);
}

inline Complex& operator+(Complex& C1, Complex& C2)
{
    Complex *C3=new Complex;
    C3->re=C1.re+C2.re;
    C3->im=C1.im+C2.im;
}

inline Complex& operator*(Complex& C1, Complex& C2)
{
    Complex *C3=new Complex;
    C3->re=C1.re*C2.re-C1.im*C2.im;
    C3->im=C1.re*C2.im+C1.im*C2.re;
}

inline Complex& operator/(Complex& C1, Complex& C2)
{
    Complex *C3=new Complex;
    double jos;
    jos=C2.re*C2.re+C2.im*C2.im;
    C3->re=(C2.re*C1.re+C1.im*C2.im)/jos;
    C3->im=(C1.im*C2.re-C2.im*C1.re)/jos;
}

///Clasa Vector Complex


list<Complex> defaultList()
{
    list<Complex> temp;
    temp.push_back(Complex(0,0));
    return temp;
}

class VectorC
{
private:
    int n;
    list<Complex> v;

public:
    VectorC(int , list<Complex> );
    VectorC(VectorC&); ///constructor de copiere
    ~VectorC() {}; ///destructor

    void citire(istream &in);
    friend istream& operator>>(istream &in, VectorC& V); ///supraincarcare pe >>

    void afisare(ostream &out);
    friend ostream& operator<<(ostream &out, VectorC& V); ///supraincarcare pe <<

    void modul_vector();
    void suma_elem();
};

VectorC::VectorC(int n=0, list<Complex> vec=defaultList() )
{
    this->n=n;
    list<Complex>::iterator i;
    for (i = vec.begin(); i != vec.end(); ++i)
        v.push_back(*i);
}

VectorC::VectorC(VectorC& V)
{
    this->n=V.n;
    list<Complex>::iterator i;
    for (i = V.v.begin(); i != V.v.end(); ++i)
       this->v.push_back(*i);
}

void VectorC::citire(istream &in)
{

    cout<<"Dati numarul de elemente ale vectorului: "<<endl;
    in>>n;
    cout<<"Dati elementele vectorului: "<<endl;
    int l=n;

    while(l!=0)
        {
            Complex C;
            in>>C;
            v.push_back(C);
            l--;
        }

}

istream& operator>>(istream &in, VectorC& V)
{
    V.citire(in);
    return in;
}

void VectorC::afisare(ostream &out)
{
    out<<"Numarul de elem ale vectorului este: "<<n<<endl;
    out<<"Vectorul este: "<<endl;
    list<Complex>::iterator i;
    for (i = v.begin(); i != v.end(); ++i)
        out<<(*i)<<endl;
}

ostream& operator<<(ostream &out, VectorC& V)
{
    V.afisare(out);
    return out;
}

void VectorC::modul_vector()
{
    double m[n];
    int j=0;
    double modulul;
    list<Complex>::iterator i;
    for (i = v.begin(); i != v.end(); ++i)
        {
            (*i).modul_Complex(modulul);
            m[j]=modulul;
            j++;
        }

    cout<<"Vectorul modulelor numerelor complexe este: "<<endl;
    for(int k=0;k<j;k++)
        cout<<m[k]<<" ";
        cout<<endl;
}

void VectorC::suma_elem()
{
    list<Complex>::iterator i;
    Complex rezultat;
    for (i = v.begin(); i != v.end(); ++i)
        rezultat=rezultat+(*i);

    cout<<rezultat;

}
void menu_output()
{
    cout<<" MENIU: "<<endl;
    cout<<"===========================================";
    cout<<endl;
    cout<<"1. Cititi doua numere complexe:"; cout<<endl;
    cout<<"2. Afisati despre primul:"; cout<<endl;
    cout<<"3. Modulul numarului complex este:"; cout<<endl;
    cout<<"4. Numerele complexe adunate dau:"; cout<<endl;
    cout<<"5. Numerele complexe inmultite dau:"; cout<<endl;
    cout<<"6. Numerele complexe impartite dau:"; cout<<endl;
    cout<<"7. Cititi vectorul de elem nr complexe:"; cout<<endl;
    cout<<"8. Afisati vectorul de elem nr complexe:"; cout<<endl;
    cout<<"9. Aflati vectorul modulelor numerelor complexe:"; cout<<endl;
    cout<<"10. Aflati suma elementelor din vector:"; cout<<endl;
    cout<<"0. Iesire."; cout<<endl;
}

void menu()
{
    int option; ///optiunea aleasa din meniu
    option=0;
    Complex C1;
    Complex C2;
    VectorC V;
    int ok=0;

    do
    {
        menu_output();

        cout<< " Introduceti numarul actiunii: ";
        cin>>option;

        if (option==1)
        {
            cin>>C1;
            cin>>C2;
        }

        if (option==2)
        {
            cout<<C1;
        }

        if (option==3)
        {
            double modulul;
            C1.modul_Complex(modulul);
            cout<<"Modulul numarului complex este: "<<modulul;
        }

        if (option==4)
        {
           Complex C3=C1+C2;
           cout<<C3;
        }

        if (option==5)
        {
           Complex C3=C1*C2;
           cout<<C3;
        }

        if (option==6)
        {
           Complex C3=C1/C2;
           cout<<C3;
        }

        if (option==7)
        {
           cin>>V;
           ok=1;
        }

        if (option==8)
        {
            if(ok==1)
                cout<<V;
        }

         if (option==9)
        {
            V.modul_vector();
        }

         if (option==10)
        {
            V.suma_elem();
        }

        if (option==0)
        {
            cout<<"EXIT!"<<endl;
        }

        if (option<0||option>10)
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
