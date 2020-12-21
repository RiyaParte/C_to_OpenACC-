#include<stdio.h>
#include<time.h>
#include<time.h>
#include<stdlib.h> 
#include<math.h>  
  
__global__ void func1(int *c,int *a,int *b,int n)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
if(i < n)
{
a[i] = 2 * i;
b[i] = 3 * i;

}
}
__global__ void func2(int *c,int *a,int *b,int n)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
if(i < n)
{
c[i] = a[i] + b[i];

}
}
int main()
{
int *d_c;
int *d_a;
int *d_b;
int n=5;
int a[n],b[n],c[n];  
int i ;     
int blocks = 2048;
int threads= 2048;
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, &c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, &a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, &b, n*sizeof(int), cudaMemcpyHostToDevice); 
func1<<<blocks, threads>>>(d_c,d_a,d_b,n);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, &c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, &a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, &b, n*sizeof(int), cudaMemcpyHostToDevice); 
func2<<<blocks, threads>>>(d_c,d_a,d_b,n);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
for (i=0;i<n;i++)
{
 printf("c =%d\n",c[i]);
}
  return 0;
}
