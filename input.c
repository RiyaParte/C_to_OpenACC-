#include<stdio.h> 
#include<stdlib.h>
int main() {
  int m=2, n=2, k=2, i, j, col, row, sum=0;
  int a[m][n], b[n][k], c[m][k];
  for (i = 0; i < m; ++i) {
    for (j = 0; j < n; ++j) {
      a[i * n + j] = i + j;
    }
  } 
  for (i = 0; i < n; ++i) {
    for (j = 0; j < k; ++j) {
      b[i * k + j] = i + j;
    }
  } 
   
  for (col = 0; col < m; ++col) {
      for (row = 0; row < k; ++row) { 
          sum = 0; 
        for (i = 0; i < n; i++)
        {
          sum += a[row * n + i] * b[i * k + col];
        }
        c[row * k + col] = sum;
      }
  } 
   
  for (i = 0; i < m; ++i) {
    for (j = 0; j < k; ++j) {
      printf("%d ", c[i][j]);
    }
    printf("\n");
  } 

  return 0;
}
