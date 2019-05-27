#include <stdio.h>
#include <unistd.h>

#define PROB 1
//PART 2: program is sum of factors of reg=10551343
//https://www.mathsisfun.com/numbers/factors-all-tool.html
//1, 11, 743, 1291, 8173, 14201, 959213, 10551343
int main(int argc, char *argv[]) {
     long long R0 = 0; 
     long long R1 = 0; 
     long long R2 = 0; 
     long long R4 = 0; 
     long long R5 = 0; 

     if(PROB == 1) {
        R0 = 0;
        R1 = 943; 
        R2 = 107;
        R4 = 1;
        R5 = 1;
     } else {
        R0 = 0;
        R1 = 1; 
        R2 = 10550400;
        R4 = 0;
        R5 = 1;
     }

loop:
     R4 = 1;
     while(1) {
        printf("[%llu, %llu, %llu, 0, %llu, %llu]\n", R0, R1, R2, R4, R5);
        R2 = R4 * R5;
        if(R2 == R1)
           R0 += R5;
        R4 += 1;
        if(R4 > R1) {
          R2 = 1;
          break;
        } else {
          R2 = 0;
        }
     }
     R5 += 1;
     if(R5 > R1) {
        printf("done, R0=%llu\n", R0);
     } else {
        goto loop;
     } 
     return 0;
}
