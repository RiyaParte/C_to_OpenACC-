#include<stdio.h> 
#include<time.h>
#include<stdlib.h>
__global__ void func1(int *c,int *a,int *b,int col,int n,int row,int k,int sum,int m)
{
int i = blockIdx.y*blockDim.y + threadIdx.y;
int j = blockIdx.x*blockDim.x + threadIdx.x;
if(i < m)
{
if(j < n)
{
  a[(i * n) + j] = i + j;
}

}
}
__global__ void func2(int *c,int *a,int *b,int col,int n,int row,int k,int sum)
{
int i = blockIdx.y*blockDim.y + threadIdx.y;
int j = blockIdx.x*blockDim.x + threadIdx.x;
if(i < n)
{
if(j < k)
{
  b[(i * k) + j] = i + j;
}

}
}
__global__ void func3(int *c,int *a,int *b,int n,int j,int i,int k,int sum,int m)
{
int col = blockIdx.y*blockDim.y + threadIdx.y;
int row = blockIdx.x*blockDim.x + threadIdx.x;
if(col < m)
{
if(row < k)
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
int main() {
  int m=2, n=2, k=2, i, j, col, row, sum=0;
int *d_c;
int *d_a;
int *d_b;
  int a[m][n], b[n][k], c[m][k];
int blocks = 1024;
int threads= 1024;
dim3 threads(blocks, threads);
dim3 blocks(blocks, threads);
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
func1<<<blocks, threads>>>(d_c,d_a,d_b,col,n,row,k,sum,m);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
func2<<<blocks, threads>>>(d_c,d_a,d_b,col,n,row,k,sum);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
cudaMalloc((void **)&d_c, m*k*sizeof(int));
cudaMemcpy(d_c, &c, m*k*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_a, m*n*sizeof(int));
cudaMemcpy(d_a, &a, m*n*sizeof(int), cudaMemcpyHostToDevice); 
cudaMalloc((void **)&d_b, n*k*sizeof(int));
cudaMemcpy(d_b, &b, n*k*sizeof(int), cudaMemcpyHostToDevice); 
func3<<<blocks, threads>>>(d_c,d_a,d_b,n,j,i,k,sum,m);
cudaDeviceSynchronize();
 cudaMemcpy(&c, d_c, m*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_c);
cudaMemcpy(&a, d_a, m*n*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_a);
cudaMemcpy(&b, d_b, n*k*sizeof(int), cudaMemcpyDeviceToHost); 
cudaFree(d_b);
  for (i = 0; i < m; ++i) {
    for (j = 0; j < k; ++j) {
      printf("%d ", c[i][j]);
    }
    printf("\n");
  } 

  return 0;
}
