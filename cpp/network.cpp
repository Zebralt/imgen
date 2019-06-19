#include "network.h"
#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <cstdio>

Information inf(50,50,50);
Information sup(250,250,200);
Information avg(125,50,175);

int pow(int i, int a) {
  int b = 1;
  for (;a>=0;a--) b *= i;
  return b;
}

int randint(int a, int b) {
  return rand()%(b-a)+a;
}

void randomOrderProcess(const std::vector<Cell*>& cells, const Information& info) {
  int count = 0;

  // one bit = one position

  // size = 5
  // visited : 0,3
  // 01001

  int all = 0;
  for (int i=0;i<cells.size();i++) {

    // picking an item
    do {
      all = randint(0,cells.size());
    } while (pow(2,all) & count);
    count += pow(2,all);

    Cell* cell = cells[all];
    if (cell) cell->process(info);

  }
}

Cell::Cell() {

}

Cell::Cell(int i) {
  stack = i;
}

void Cell::addNeighbor(Cell* c) {
  if (c) {
    neighbors.push_back(c);
  }
}

void Cell::process(const Information& b) {

  /// TREATMENT
  ///
//  data.r = b.b/(stack + 1);
//  data.g =  b.r/(stack + 1);
//  data.b = b.g/(stack + 1);

  data.r = b.r%250 + randint(1,10);
  data.g = b.g%250 + randint(3,7);
  data.b = b.b%250 + randint(2,6);

//  data.r = b.r%(sup.r - inf.r) + inf.r + randint(1,avg.r - inf.r);
//  data.g = b.g%(sup.g - inf.g) + inf.g + randint(1, avg.g - inf.g);
//  data.g = b.b%(sup.b - inf.b) + inf.b + randint(1, avg.b - inf.b);

  if (data.r > 255) data.r =  255; if (data.r < 0) data.r = 0;
  if (data.g > 255) data.g =  255; if (data.g < 0) data.g = 0;
  if (data.b > 255) data.b =  255; if (data.b < 0) data.b = 0;

//  data.r = b.r;
//  data.g = b.g;
//  data.b = b.b;

//  LOG("processing");

  if (stack > 0) {
    stack--;
//    for (auto c : neighbors) {
//      c->process(data);
//    }

    randomOrderProcess(neighbors, data);

  }

//  else
//    LOG("A cell died.");
}


/////////////////////////

Network::Network(int w, int h, int q) : width(w) , height(h) {
  for (int i=0;i<width * height;i++) {
    cells.push_back(new  Cell(q));
  }

  for (int i=0; i<width; i++) {

    for (int j = 0; j<height; j++) {

      if (Cell* c = getCell(j,i)) {

        for (int a = (i ? i - 1 : i); a <= ( i < width - 1 ? i + 1 : i); a++) {
          for (int b = (j ? j - 1 : j); b <= ( j < height - 1 ? j + 1 : j); b++) {
            if (a != i || b != j) {
              c->addNeighbor(getCell(a,b));
//              LOG(a << "," << b << " is a neighbor of " << i << "," << j);
            }
          }
        }

      }

    }

  }
}

Cell* Network::getCell(int x, int y) {

  if (x >= 0 && x < width && y >= 0 && y < height) {

    return cells[x + y * width];

  }

  return nullptr;
}

void Network::input(const Information& info) {
  if (cells.size()) {
    if (cells[0]) {
      cells[0]->process(info);
    }
  }
}

void Network::input(const Information& info, int x, int y) {
  Cell* c = getCell(y,x);
  if (c) {
    c->process(info);
  }
}

void Network::writePPM() {
  std::ostream& ppm = std::cout;

  ppm << "P3" << std::endl;
  ppm << width << " " << height << std::endl;
  ppm << "255" << std::endl;

  for (int i=0; i<width; i++) {
    for (int j=0; j<height; j++) {

      Cell* c = getCell(j,i);

      if (c) {

        ppm << std::setw(5) << c->data.r << std::setw(5) << c->data.g << std::setw(5) << c->data.b << std::endl;

      }
    }

//    ppm << std::endl;
  }

}
