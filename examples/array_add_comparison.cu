#include<stdio.h>
#include<time.h>
#include<time.h>
#include<stdlib.h> 
#include<math.h>  
  
__global__ void func1(int *c,int *a,int *b, int n)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
// printf("i = %d\n", i);
if(i < n)
{
a[i] = 2;
b[i] = 3;

}
}
__global__ void func2(int *c,int *a,int *b, int n)
{
int i = blockIdx.x*blockDim.x + threadIdx.x;
if(i < n)
{ 
c[i] = a[i] + b[i];

}
}
int main()
{
float timespentGPU,timespentGPU1,timespentGPU2;
float timespentCPU,timespentCPU1,timespentCPU2;


cudaEvent_t start, stop; 
cudaEventCreate(&start); //Creates an event object 
cudaEventCreate(&stop);

cudaEventRecord(start, 0);
int *d_c;
int *d_a;
int *d_b;
int n=2*1000000 ;
// int a[n],b[n],c[n];  
int *h_a=(int*) malloc(n* sizeof(int));
int *h_b=(int*) malloc(n * sizeof(int));
int *h_c=(int*) malloc(n * sizeof(int));  
int i ;     
int blocks = 1024;
int threads= 1024;
// printf("Here");
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, h_c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, h_a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, h_b, n*sizeof(int), cudaMemcpyHostToDevice); 

cudaEventRecord(start, 0);
func1<<<blocks, threads>>>(d_c,d_a,d_b,n);
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentGPU1, start, stop); 
cudaDeviceSynchronize();
 cudaMemcpy(h_c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(h_a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(h_b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMalloc((void **)&d_c, n*sizeof(int));
cudaMemcpy(d_c, h_c, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, n*sizeof(int));
cudaMemcpy(d_a, h_a, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*sizeof(int));
cudaMemcpy(d_b, h_b, n*sizeof(int), cudaMemcpyHostToDevice); 
cudaEventRecord(start, 0); 
func2<<<blocks, threads>>>(d_c,d_a,d_b, n);
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentGPU2, start, stop); 

cudaDeviceSynchronize();
 cudaMemcpy(h_c, d_c, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(h_a, d_a, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(h_b, d_b, n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
for (i=0;i<n;i++)
{
 printf("c =%d\n",h_c[i]);
}
timespentGPU = timespentGPU1+timespentGPU2;
printf("\n timespent on GPU=%f ms",timespentGPU);

 	   
cudaEventRecord(start, 0); 
for(i = 0;i<n;i++)
{
    h_a[i] =  2;
    h_b[i] =  3;
}  
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentCPU1, start, stop); 


cudaEventRecord(start, 0); 

for (i=0;i<n;i++)
{
    h_c[i] = h_a[i] + h_b[i];
} 
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentCPU2, start, stop); 


timespentCPU = timespentCPU1+timespentCPU2;
printf("\n timespent on CPU=%f ms",timespentCPU);


printf("\n Speedup = %f",timespentCPU/timespentGPU);
  return 0;
}
