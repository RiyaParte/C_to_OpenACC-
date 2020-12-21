#include<stdio.h> 
#include<stdlib.h> 
int main()
{
int n=5,x;
int a[n],b[n],c[n];  
int i ;     
i=0;
while(i<n){
    a[i] =  i*2;
    b[i] =  i*3;
i++;
}
i=0;
while(i<n){
    c[i] = a[i] + b[i];
 i++;
} 
i=0;
while(i<n){
 printf("c =%d\n",c[i]);
i++;
}
}
