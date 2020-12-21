#include<stdio.h> 
#include<stdlib.h> 
int main()
{
int n=5,x;
int a[n],b[n],c[n];  
int i ;     
i=0;
do{
    a[i] =  i*2;
    b[i] =  i*3;
i++;
}while(i<n);
i=0;
do{
    c[i] = a[i] + b[i];
 i++;
}while(i<n) ;  
i=0;
do{
 printf("c =%d\n",c[i]);
i++;
}while(i<n)  ;}
