
#include "network.h"
#include <ctime>
#include <cstdlib>
#include <cstdio>

int main(int argc, char** argv) {

  srand(time(NULL));

  Network n(200, 200,1);

  n.input(Information(20,80,70), 100,100);

  n.writePPM();

}
