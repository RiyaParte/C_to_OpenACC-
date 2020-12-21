#include<stdio.h>
#include<time.h>
#include<stdlib.h> 
#include<math.h>  
  
int main()
{
int n=5;
int a[n],b[n],c[n];  
int i ;     
for(i = 0;i<n;i++)
{
    a[i] =  2*i;
    b[i] =  3*i;
}  
for (i=0;i<n;i++)
{	
    c[i] = a[i] + b[i];
} 
for (i=0;i<n;i++)
{
 printf("c =%d\n",c[i]);
}
  return 0;
}
