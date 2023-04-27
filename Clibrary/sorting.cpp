#include <iostream>

extern "C"{
    void print();
}

void print(){std::cout<<"Hello World"<<std::endl;}
