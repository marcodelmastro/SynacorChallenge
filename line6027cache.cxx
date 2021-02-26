#include <iostream>

unsigned int line6027cache(unsigned int r0, unsigned int r1, unsigned int r7, int** cache)
{
  // return memoized result if available
  if (cache[r0][r1] != -1) {
    return cache[r0][r1];
  }
  // standard implementation, but caching result
  int p = -1;
  if (r0==0) {
    p = r1+1;
  } else if (r1==0) {
    p = line6027cache(r0-1,r7,r7,cache);
  } else {
    p = line6027cache(r0-1, line6027cache(r0,r1-1,r7,cache), r7,cache);
  }
  // memoizing result
  p = p % 32768;
  cache[r0][r1]=p;
  return p;
}

unsigned int line6027( unsigned int r0, unsigned int r1, unsigned int r7 )
{
  // inizialize cache
  int** cache = new int*[5]; // r0 starts at 4 and get decreased down to 0, not reason to cache more
  for (int i=0;i<5;i++) {
    cache[i] = new int[32768];
  }
  for (int i=0;i<5;i++) {
    for (int j=0;j<32768;j++) {
      cache[i][j] = -1; // if -1 still needs to be computed
    }
  }
  return line6027cache(r0,r1,r7,cache);
}

int main() {
  
  // inizialize cache
  unsigned int r0 = 4;
  unsigned int r1 = 1;
  unsigned int r7 = 1;
  
  std::cout << "line6017(" << r0 << ", " << r1 << ", " << r7 << ") = " << line6027(r0,r1,r7) << std::endl;
  return 0;
}
