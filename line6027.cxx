#include <iostream>

unsigned int line6027(unsigned int r0, unsigned int r1, unsigned int r7) {
  if (r0==0) {
    return ( r1+1 ) % 32768;
  }
  else if (r1==0) {
    return line6027(r0-1,r7,r7);
  } else {
    return line6027(r0-1, line6027(r0,r1-1,r7), r7);
  }
}
 
int main() {
  unsigned int r0 = 4;
  unsigned int r1 = 1;
  unsigned int r7 = 1;
  std::cout << "line6017(" << r0 << ", " << r1 << ", " << r7 << ") = " << line6027(r0,r1,r7) << std::endl;
  return 0;
}
