#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 100

int randomNumber(int, int);
int* randomPermutation(int *, int);
void inversePermutation(int *, int *, int);

int main(){
  srand(time(NULL));

  int perm[SIZE];
  int invPerm[SIZE];
  int n = 15;

  randomPermutation(perm, n);
  inversePermutation(perm, invPerm, n);

  printf("\nInverse permutation:\n");
  for(int i = 0; i < n; i++){
    printf("[%d]", invPerm[i]);
  }

  return 0;
}

int* randomPermutation(int *perm, int n){
  for (int i = 0; i < n; i++)
  {
    perm[i] = i + 1;
    printf("[%d]", perm[i]);
  }

  printf("\n");

  for (int i = n - 1; i > 0; i--)
  {
    int num = randomNumber(0, i);

    int temp = perm[i];
    perm[i] = perm[num];
    perm[num] = temp;
  }

  printf("Permutation:\n");

  for (int i = 0; i < n; i++)
  {
    printf("[%d]", perm[i]);
  }

  return perm;
}

void inversePermutation(int *perm, int *invPerm, int n){
  for(int i = 0; i < n; i++){
    invPerm[perm[i] - 1] = i + 1;
  }

}

int randomNumber(int min, int max){
  return (rand() % (max - min + 1)) + min;
}