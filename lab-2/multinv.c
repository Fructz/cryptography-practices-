#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#define MATRIX_CELLS 2
#define ASCII_FIRST 32
#define ASCII_SECOND 126
#define VALID_KEY (ASCII_SECOND - ASCII_FIRST + 1)

typedef struct Key
{
  int KMatrix[MATRIX_CELLS][MATRIX_CELLS];
  int detK;
  int invDetK;
} Key;

int gcd(int, int);
int multInv(int, int);
void encipherFile();
Key keyGeneration(int);
Key inverseMatrix(Key, int);

int main(){
  srand(time(NULL));

  for (int i = 0; i < 10; i++)
  {
    printf("Key: %d\n", i + 1);

    Key K = keyGeneration(VALID_KEY);
    Key Kinv = inverseMatrix(K, VALID_KEY);

    printf("\n");
  }

  /*printf("%d\n", multInv(26,7));
  printf("%d\n", multInv(35,12));
  printf("%d\n", multInv(40,7));
  printf("%d\n", multInv(55,8));
  printf("%d\n", multInv(95,17));*/
}

int multInv(int n, int a){
  if (n < 2) return -1;
  a = ((a % n) + n) % n;

  if (gcd(a, n) != 1) return -1;

  int a_0 = n, b_0 = a, t_0 = 0, t = 1, temp = 0;
  int q = a_0 / b_0, r = a_0 - q * b_0;

  while (r > 0){
    temp = (t_0 - q*t) % n;
    t_0 = t;
    t = temp;
    a_0 = b_0;
    b_0 = r;
    q = a_0 / b_0;
    r = a_0 - q * b_0;
  }

  if (b_0 != 1) return -1; else return (t % n + n) % n;
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

Key keyGeneration(int n){
  Key K;

  do
  {
    for (int i = 0; i < MATRIX_CELLS; i++){
      for (int j = 0; j < MATRIX_CELLS; j++)
      {
         K.KMatrix[i][j]= rand() % n;
      }
    }

    int prev_detK = K.KMatrix[0][0] * K.KMatrix[1][1] - K.KMatrix[0][1] * K.KMatrix[1][0];
    K.detK = (prev_detK % n + n) % n;

    K.invDetK = multInv(n, K.detK);
  } while (gcd(K.detK, n) != 1);

  printf("K = \n");
  printf("[%d][%d]\n", K.KMatrix[0][0], K.KMatrix[0][1]);
  printf("[%d][%d]\n", K.KMatrix[1][0], K.KMatrix[1][1]);

  return K;
}

Key inverseMatrix(Key K, int n){
  Key Kinv;

  int a = K.KMatrix[0][0];
  int b = K.KMatrix[0][1];
  int c = K.KMatrix[1][0];
  int d = K.KMatrix[1][1];

  int detInv = K.invDetK;

  Kinv.KMatrix[0][0] = (detInv * d) % n;
  Kinv.KMatrix[0][1] = (detInv * (-b)) % n;
  Kinv.KMatrix[1][0] = (detInv * (-c)) % n;
  Kinv.KMatrix[1][1] = (detInv * a) % n;

  for(int i = 0; i < MATRIX_CELLS; i++){
    for(int j = 0; j < MATRIX_CELLS; j++){
      Kinv.KMatrix[i][j] = (Kinv.KMatrix[i][j] % n + n) % n;
    }
  }

  printf("K^-1 = \n");
  printf("[%d][%d]\n", Kinv.KMatrix[0][0], Kinv.KMatrix[0][1]);
  printf("[%d][%d]\n", Kinv.KMatrix[1][0], Kinv.KMatrix[1][1]);
  return Kinv;
}

void encipherFile(Key K){
  char plaintext[20] = "HELL";

  if (strlen(plaintext) % 2 != 0)
  {
    strcat(plaintext, "X");
  }

  for (int i = 0; plaintext[i] != '\0'; i+=2)
  {
    int p0 = plaintext[i] - ASCII_FIRST;
    int p1 = plaintext[i + 1] - ASCII_FIRST;

    int c0 = (p0 * K.KMatrix[0][0] + p1 * K.KMatrix[0][1]) % VALID_KEY;
    int c1 = (p0 * K.KMatrix[1][0] + p1 * K.KMatrix[1][1]) % VALID_KEY;

    char encrypted0 = c0 + ASCII_FIRST;
    char encrypted1 = c1 + ASCII_FIRST;

    printf("%d %d\n", c0, c1);
    printf("%c%c\n", encrypted0, encrypted1);
  }
}