#include <stdio.h>

int main(int argc, char *argv[]) {
    long long inst = 0; 
    long long R0 = 0;
    long long R1 = 0;
    long long R2 = 0;
    long long R3 = 0;
    long long R4 = 0;
    long long R5 = 0;

    while(1) {
      R5 = 0x1c8;
      R5 = R5 & 0x7b;
      // == 0x48
      if(R5 == 0x48) {
          R5 = 1;
          //addr 5 1 1
          break;
      } else {
          R5 = 0;
      }
    }
    // seti 0 3 5
    R5 = 0;
    inst += 5; // skipped seti 0 0 1
PC_6:
    R4 = R5 | 65536;
    R5 = 13284195;
    inst += 2;
PC_8:
    //bani 4 255 3
    R3 = R4 & 255;
    R5 = R3 + R5;
    R5 &= 16777215;
    R5 *= 65899;
    R5 &= 16777215;
    //gtir 256 4 3
    if (256 > R4) {
      R3 = 1;
      //set 27 1 1
      goto PC_28;
    } else {
      R3 = 0;
      // addr 3 1 1
    }
    //seti 0 5 3
    R3 = 0;
PC_18:
    R2 = R3 + 1;
    R2 *= 256;
    if(R2 > R4){
      R2 = 1;
      //goto PC_26;
      goto PC_26;
    } else {
      R2 = 0;
    }
    R3 += 1;
    goto PC_18;
PC_26:
    //setr 3 7 4
    R4 = R3;
    goto PC_8;
PC_28:
    printf("%lld\n", R5);
    if(R5 == R0) {
      R3 = 1;
      //printf("exiting");
      return 0;
    } 
    goto PC_6;
}
