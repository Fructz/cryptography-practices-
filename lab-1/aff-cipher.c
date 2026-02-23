#include <stdio.h>
#include <stdlib.h>
#define TAM 26

int gcd(int, int);
int* generateZnStar(int, int *, int *);

int main(){
  int n = 26, count = 0;
  int *list = (int*)malloc((n - 1)*sizeof(int));

  list = generateZnStar(n, list, &count);
  for (int i = 0; i < count; i++)
  {
    printf("%d ", list[i]);
  }

  free(list);
  return 0;
}

int* generateZnStar(int n, int *list, int *count){
  int result = 0; *count = 0;

  for (int i = 1; i < n; i++){
    result = gcd(i, n);
    if (result == 1){
      list[*count] = i;
      (*count)++;
    }
  }

  return list;
}

int gcd(int a, int b) {
    a = abs(a);
    b = abs(b);

    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }

    return a;
}