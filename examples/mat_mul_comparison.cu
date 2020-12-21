 
#include<stdio.h> 
#include<time.h>
#include<stdlib.h>
#define THREADS_PER_BLOCK 1024

__global__ void func1(int *b,int *c,int *a,int sum,int k,int col,int row,int n,int m)
{
int i = blockIdx.y*blockDim.y + threadIdx.y;
int j = blockIdx.x*blockDim.x + threadIdx.x;
// printf("i = %d j = %d \n",i,j );
if(i >= 0 && i < m)
{
	if(j >= 0 && j < n) 
		{ 
		  a[(i * n) + j] = i + j;
		} 
	}
}	
__global__ void func2(int *b,int *c,int *a,int sum,int k,int col,int row,int n)
{
int i = blockIdx.y*blockDim.y + threadIdx.y;
int j = blockIdx.x*blockDim.x + threadIdx.x;
	if(i >= 0 && i < n)
	{
		if(j >= 0 && j < k)

		{ 
		  b[(i * k) + j] = i + j; 
		}
	}
}	
__global__ void func3(int *b,int *c,int *a,int i,int sum,int k,int j,int n,int m)
{
int row = blockIdx.y*blockDim.y + threadIdx.y;
int col = blockIdx.x*blockDim.x + threadIdx.x;
if(col >= 0 && col < m)
{
if(row >= 0 && row < k)
{
{
  sum = 0;
  for (i = 0; i < n; i++)
  {
    sum += a[(row * n) + i] * b[(i * k) + col];
  }

  c[(row * k) + col] = sum;
}
}
}
}
int main() {
  int m=800 , n=800 , k=800, i, j, col, row, sum=0;
  int a[m][n], b[n][k], c[m][k];
int *d_b;
int *d_c;
int *d_a; 
int width = n; 
int sqrtThreads = sqrt(THREADS_PER_BLOCK);
int nBlocks = width/sqrtThreads;
if (width % sqrtThreads != 0) { // Add an extra block if necessary
  nBlocks++;
}
dim3 grid(nBlocks, nBlocks, 1);
dim3 block(sqrtThreads, sqrtThreads, 1); // Max number of threads per block

float timespentGPU,timespentGPU1,timespentGPU2,timespentGPU3;
float timespentCPU,timespentCPU1,timespentCPU2,timespentCPU3;

cudaEvent_t start, stop; 
cudaEventCreate(&start); //Creates an event object 
cudaEventCreate(&stop);  
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice);
cudaEventRecord(start, 0); 
func1<<<grid, block>>>(d_b,d_c,d_a,sum,k,col,row,n,m);
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentGPU1, start, stop); 
cudaDeviceSynchronize();
 cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice); 
 
cudaEventRecord(start, 0); 
func2<<<grid, block>>>(d_b,d_c,d_a,sum,k,col,row,n);
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentGPU2, start, stop); 
cudaDeviceSynchronize();
cudaDeviceSynchronize();
 cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice); 
cudaEventRecord(start, 0); 
func3<<<grid, block>>>(d_b,d_c,d_a,i,sum,k,j,n,m);
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop); 
cudaEventElapsedTime(&timespentGPU3, start, stop); 
cudaDeviceSynchronize();
 cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
  for (i = 0; i < m; ++i) {
    for (j = 0; j < k; ++j) {
      printf("%d ", c[i][j]);
    }
    printf("\n");
  }  


timespentGPU = timespentGPU1+timespentGPU2+timespentGPU3; 
printf("\n timespent on GPU=%f",timespentGPU);
 


int *h_a=&a[0][0],*h_b=&b[0][0],*h_c=&c[0][0];

cudaEventRecord(start, 0); 
  for (i = 0; i < m; ++i) {
    for (j = 0; j < n; ++j) {
      h_a[i * n + j] = i + j;
    }
  }   
cudaEventRecord(stop, 0);
  cudaEventSynchronize(stop);
cudaEventElapsedTime(&timespentCPU1, start, stop); 


cudaEventRecord(start, 0); 
  for (i = 0; i < n; ++i) {
    for (j = 0; j < k; ++j) {
      h_b[i * k + j] = i + j;
    }
  } 
cudaEventRecord(stop, 0);
  cudaEventSynchronize(stop);
cudaEventElapsedTime(&timespentCPU2, start, stop);
   
cudaEventRecord(start, 0);    
  for (col = 0; col < m; ++col) {
      for (row = 0; row < k; ++row) { 
          sum = 0; 
        for (i = 0; i < n; i++)
        {
          sum += h_a[row * n + i] * h_b[i * k + col];
        }
        h_c[row * k + col] = sum;
      }
  } 
cudaEventRecord(stop, 0);
  cudaEventSynchronize(stop);
cudaEventElapsedTime(&timespentCPU3, start, stop);
timespentCPU = timespentCPU1+timespentCPU2+timespentCPU3;
printf("\n timespent on CPU=%f",timespentCPU);
 

printf("\n Speedup = %f",timespentCPU/timespentGPU) ;
  return 0;
}