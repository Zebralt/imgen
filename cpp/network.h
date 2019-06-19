#ifndef network_h
#define network_h

#include <vector>

#define LOG(sstr) std::cout << sstr << std::endl


struct Information {

  short r = 0;
  short g = 0;
  short b = 0;

  Information() {

  }

  Information(int a, int t, int y) {
    r = a;
    g = t;
    b = y;
  }

};

class Cell {
public:
  Cell();
  Cell(int);
  int stack = 1;
  Information data;
  void addNeighbor(Cell*);
  std::vector<Cell*> neighbors;
  void process(const Information&);

};

class Network {
public:
  std::vector<Cell*> cells;
  int width;
  int height;

  Network(int width, int height, int quality = 0);

  Cell* getCell(int,int);

  void input(const Information&);
  void input(const Information&, int, int);

  void writePPM();
};

#endif // network_h
