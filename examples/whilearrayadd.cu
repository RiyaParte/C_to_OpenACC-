#include<stdio.h> 
#include<time.h>
#include<stdlib.h> 
__global__ void func1(int *c,int *a,int *b,int n,int startvalue)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
if( i < n && i >= startvalue )
{
a[i] = i * 2;
b[i] = i * 3;
i++;

}
}
__global__ void func2(int *c,int *a,int *b,int n,int startvalue)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
if( i < n && i >= startvalue )
{
c[i] = a[i] + b[i];
i++;

}
}
int main()
{
int *d_c;
int *d_a;
int *d_b;
int n=5,x;
int a[n],b[n],c[n];  
int i ;     
i=0;
int startvalue;
int blocks = 1024;
int threads= 1024;
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, &c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, &a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, &b, n*sizeof(int), cudaMemcpyHostToDevice); 
startvalue = i;
func1<<<blocks, threads>>>(d_c,d_a,d_b,n,startvalue);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
i=0;
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, &c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, &a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, &b, n*sizeof(int), cudaMemcpyHostToDevice); 
startvalue = i;
func2<<<blocks, threads>>>(d_c,d_a,d_b,n,startvalue);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
i=0;
while(i<n){
 printf("c =%d\n",c[i]);
i++;
}
}
