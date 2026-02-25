#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>
#define ASCII_FIRST 32
#define ASCII_SECOND 126
#define VALID_KEY (ASCII_SECOND - ASCII_FIRST + 1)

typedef struct Key{
  int a;
  int b;
}Key;

int gcd(int, int);
int* generateZnStar(int, int *, int *);
int getb_zn(int, int);
void joining_data();
void def_handler(int);
void encryptFile(const char *, const char *, Key);
void decipheringFile(const char *, const char *);
Key keyGeneration();

int main(){
  signal(SIGINT, def_handler);  // Activar Ctrl + C
  srand(time(NULL));

  /*int n = 26, count = 0;
  int *list = (int*)malloc((n - 1)*sizeof(int));

  if (list == NULL) {
      printf("Memory allocation failed\n");
      return 1;
  }

  list = generateZnStar(n, list, &count);

  printf("Z_%d* = ", n);
  for (int i = 0; i < count; i++)
  {
    printf("%d ", list[i]);
  }
  printf("\n");

  free(list);*/

  // Probar inverso modular
  //joining_data();

  //printf("%d", VALID_KEY);
  Key myKey = keyGeneration();

  printf("[%d, %d]", myKey.a, myKey.b);
  encryptFile("test.txt", "ciphertext.txt", myKey);
  //decipheringFile("ciphertext.txt", "decoded.txt");
  return 0;
}

Key keyGeneration(){
  int i = 0;
  Key K;

  K.a = -1;

  while (getb_zn(K.a, VALID_KEY) == -1)
  {
    K.a = rand() % VALID_KEY;
  }
  K.b = rand() % VALID_KEY;

  return K;
}

int getb_zn(int a, int n) {
    if (gcd(a, n) != 1) {
        //printf("\n[!] No inverse exists\n");
        return -1;
    }

    int size = 0;
    int *zn_star = (int*)malloc((n - 1)*sizeof(int));

    if (zn_star == NULL) {
        printf("Memory allocation failed\n");
        return -1;
    }

    generateZnStar(n, zn_star, &size);

    for (int i = 0; i < size; i++) {
        if ((a * zn_star[i]) % n == 1) {
            int result = zn_star[i];
            free(zn_star);
            return result;
        }
    }

    free(zn_star);
    return -1;
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

int char_to_code(char code) {
    if (code == '\n') return -1;

    int con = (int)code;

    if (con < ASCII_FIRST || con > ASCII_SECOND) {
        printf("[!] Error\n");
        return -1;
    }

    return con;
}

char code_to_char(int code) {
    if (code == -1) return '\n';
    return (char)code;
}

void encryptFile(const char *inputFile, const char *outputFile, Key key) {
    FILE *in = fopen(inputFile, "r");
    if (in == NULL) {
        printf("Error opening input file\n");
        return;
    }

    FILE *out = fopen(outputFile, "w");
    if (out == NULL) {
        printf("Error opening output file\n");
        fclose(in);
        return;
    }

    int c;
    while ((c = fgetc(in)) != EOF) {
        if (c == '\n') {
            fputc('\n', out);
        } else {
            int num = c - ASCII_FIRST;
            int encrypted = (key.a * num + key.b) % VALID_KEY;
            fputc(encrypted + ASCII_FIRST, out);
        }
    }

    fclose(in);
    fclose(out);

    printf("\n[+] Encryption completed -> %s\n", outputFile);
}

void decipheringFile(const char *inputFile, const char *outputFile){
    Key mykey;
    printf("Enter your key:\n");
    printf("a: "); scanf("%d", &mykey.a);
    printf("b: "); scanf("%d", &mykey.b);

    FILE *in = fopen(inputFile, "r");
    if (in == NULL) {
        printf("Error opening input file\n");
        return;
    }

    FILE *out = fopen(outputFile, "w");
    if (out == NULL) {
        printf("Error opening output file\n");
        fclose(in);
        return;
    }

    int c;
    int a_inv = getb_zn(mykey.a, VALID_KEY);
    while ((c = fgetc(in)) != EOF) {
        if (c == '\n') {
            fputc('\n', out);
        } else {
            int num = c - ASCII_FIRST;
            int decoded = a_inv * (num - mykey.b);
            decoded = ((decoded % VALID_KEY) + VALID_KEY) % VALID_KEY;
            fputc(decoded + ASCII_FIRST, out);
        }
    }

    fclose(in);
    fclose(out);

    printf("[+] Decryption completed -> %s\n", outputFile);
}

void joining_data() {
    int a, n;
    printf("\n[+] Please, insert 2 numbers:\n");

    printf("a: "); scanf("%d", &a);
    printf("n: "); scanf("%d", &n);

    int element = getb_zn(a, n);
    if (element != -1) printf("Inverse: %d\n", element);
}

void def_handler(int sig) {
    printf("\n\n[!] Leaving...\n");
    exit(1);
}