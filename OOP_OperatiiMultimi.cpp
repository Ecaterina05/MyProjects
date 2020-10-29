///Tema 8 - Baltatescu Elena-Ecaterina - Grupa 211
#include <iostream>
using namespace std;
class Multime {
private:
    int v[101]; ///vectorul propriu zis corespunzator multimii
    int n; ///numarul de elemente ale vectorului

public:
    Multime(int v[],int n); ///constructor de initializare cu parametri

    Multime(); ///constructor de initializare fara parametri

    Multime(Multime&); ///constructor de copiere

    ~Multime() {}; ///destructor

    void transformare(); ///transforma un vector intr-o multime, eliminand duplicatele

    Multime& operator=(Multime &z); ///supraincarcarea operatorului = (ca metoda)

    friend Multime& operator+(Multime& A, Multime& B); ///supraincarcare operator + ( reuniunea a doua multimi )

    friend Multime& operator*(Multime& A, Multime& B); ///supraincarcare operator * ( intersectia a doua multimi )

    friend Multime& operator/(Multime& A, Multime& B); ///supraincarcare operator / ( diferenta a doua multimi )

    friend istream& operator>>(istream &in, Multime& A); ///supraincarcare pe >>

    void citire(istream &in);

    friend ostream& operator<<(ostream &out, Multime& A); ///supraincarcare pe <<


};

void Multime::citire(istream &in){
    cout<<"Cititi numarul de elemente: ";
    in>>n;
    cout<<"Cititi vectorul: ";
    for (int i = 1; i<=n; i++)
        in>>v[i];
}

istream& operator>>(istream &in, Multime& A){
        A.citire(in);
        return in;
}

ostream& operator<<(ostream &out, Multime& A) {
    for (int i = 1; i<=A.n; i++)
        out<<A.v[i]<<' ';
        out<<endl;
        return out;
}

Multime::Multime()
{
   n=1;
   v[1]=0;

}

Multime::Multime(int v[], int n) {
    this->n=n;
    for(int i=1; i<=n; i++)
        this->v[i]=v[i];
}

Multime::Multime(Multime& A){
    this->n=A.n;
    for(int i=1; i<=n; i++)
    this->v[i]=A.v[i];
}

void Multime::transformare()
{   int i,j;
    for(i=1;i<n;i++)
        for(j=i+1;j<=n;j++)
            if(v[i]>v[j])
                swap(v[i],v[j]);

     i=1;
    while(i<n)
    {if(v[i]==v[i+1])
    {
        for(int k=i+1;k<n;k++)
            v[k]=v[k+1];
            n--; i--;
    }
    i++;
    }
}

Multime& Multime::operator=(Multime &A)
{
     this->n=A.n;
    for(int i=1; i<=n; i++)
    this->v[i]=A.v[i];
}

inline Multime& operator+(Multime& A, Multime& B)
{
    int m=0;
    Multime *C=new Multime;

   for(int i=1;i<=A.n;i++)
       {    int ok=1;
           for(int j=1;j<=B.n;j++)
                if(A.v[i]==B.v[j])
                    ok=0;

           if(ok==1)
            {
                m++;
                C->v[m]=A.v[i];

            }
       }


   for(int i=1;i<=B.n;i++)
       {    int ok=1;
           for(int j=1;j<=A.n;j++)
                if(B.v[i]==A.v[j])
                    ok=0;

           if(ok==1)
            {
                m++;
                C->v[m]=B.v[i];

            }
       }

    for(int i=1;i<=A.n;i++)
        for(int j=1;j<=B.n;j++)
            if(A.v[i]==B.v[j])
            {
                m++;
                C->v[m]=A.v[i];

            }


    C->n=m;
}

inline Multime& operator*(Multime& A, Multime& B)
{
    int m=0;
    Multime *C=new Multime;
    for(int i=1;i<=A.n;i++)
        for(int j=1;j<=B.n;j++)
            if(A.v[i]==B.v[j])
            {
                m++;
                C->v[m]=A.v[i];
            }

    C->n=m;
}

inline Multime& operator/(Multime& A, Multime& B)
{
    int m=0;
    Multime *C=new Multime;

    for(int i=1;i<=A.n;i++)
       {    int ok=1;
           for(int j=1;j<=B.n;j++)
                if(A.v[i]==B.v[j])
                    ok=0;

           if(ok==1)
            {
                m++;
                C->v[m]=A.v[i];

            }
       }

    C->n=m;
}
void menu_output()
{
    cout<<" Baltatescu Elena-Ecaterina Grupa 211 - Proiect - Tema 8: "<<endl;
    cout<<" MENIU: "<<endl;
    cout<<"===========================================";
    cout<<endl;
    cout<<"1. Cititi doua numere naturale si doi vectori"; cout<<endl;
    cout<<"2. Transformati vectorii in multimi eliminand duplicatele"; cout<<endl;
    cout<<"3. Faceti reuniunea celor doua multimi"; cout<<endl;
    cout<<"4. Faceti intersectia celor doua multimi"; cout<<endl;
    cout<<"5. Faceti diferenta celor doua multimi"; cout<<endl;
    cout<<"0. Iesire."; cout<<endl;
}

void menu()
{
    int option; ///optiunea aleasa din meniu
    option=0;
    int ok=0; ///verifica daca au fost introduse date de la tastatura cu care sa se lucreze
    int ok1=0; ///verifica daca cei doi vectori sunt multimi, altfel nu se pot efectua operatiile cu multimi
    Multime A;
    Multime B;

    do
    {
        menu_output();

        cout<< " Introduceti numarul actiunii: ";
        cin>>option;

        if (option==1)
        {
          cin>>A;
          cin>>B;
          ok=1;
        }

        if (option==2)
        {   if(ok==1)
                {
                  A.transformare();
                  cout<<A<<endl;
                  B.transformare();
                  cout<<B<<endl;
                  ok1=1;
                }
            else
                {
                    cout<<"Nu ati introdus date, alegeti optiunea 1 mai intai"<<endl;
                }
        }

        if (option==3)
        {
            if(ok==1 && ok1==1)
                {

                    Multime C=A+B;
                    cout << C<<endl;
                }
            else
                {
                    cout<<"Alegeti mai intai optiunile 1 si 2 pentru a putea face operatii cu multimi"<<endl;
                }
        }

        if (option==4)
        {
           if(ok==1 && ok1==1)
                {

                    Multime C=A*B;
                    cout << C <<endl;
                }
            else
                {
                    cout<<"Alegeti mai intai optiunile 1 si 2 pentru a putea face operatii cu multimi"<<endl;
                }
        }

        if (option==5)
        {
            if(ok==1 && ok1==1)
                {

                    Multime C=A/B;
                    cout << C <<endl;
                }
            else
                {
                    cout<<"Alegeti mai intai optiunile 1 si 2 pentru a putea face operatii cu multimi"<<endl;
                }
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
        //system("pause"); ///Pauza - Press any key to continue...
        //system("cls");   ///Sterge continutul curent al consolei
    }
    while(option!=0);
}

int main()
{
    menu();
    return 0;
}
