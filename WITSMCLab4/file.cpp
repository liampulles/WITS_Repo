//=========================PLEASE READ:===========================
//Name: Liam Pulles
//Student no: 855442
//
// This file contains methods for printing vectors and reading from
// files.
//
// Please note that this code requires a slightly modified dataset.txt,
// namely that the top of the file must contain an integer specifying
// the number of elements in a row.
//
//    e.g.
//--> 3
//    2.07 -1.3 0.34
//    ...
//
//================================================================

#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <cstdlib>
#include <time.h>
#include <algorithm>
#include <random>

static void dataSet(std::string fileName, std::vector< std::vector<double>>& X){
  	std::ifstream file;
	int width;
	
	file.open(fileName);
	while(file.is_open()){
	  //I modify the e.g. Data.txt to have a single number at the top, which
	  //contains the number of elements in each row.
		file >> width;
		while(!file.eof()){
		  //Create row.
		  std::vector<double> Xrow;
		  for (int i=0; i<width; i++){
			  double in;
			  file >> in;
			  Xrow.push_back(in);
	          }
	          X.push_back(Xrow);
		}
		break;
	}
	file.close();
	return;
}

//Print out a 2D vector to screen.
static void printMultiVec(std::vector< std::vector<double> > items){
  for (int i=0; i<items.size(); i++){
    std::cout << "[ ";
    for (int k=0; k<items[i].size(); k++){
      std::cout << items[i][k] << " ";
    }
    std::cout << " ]" << std::endl;
  }
  return;
};

//Print out a 1D vector.
static void printSingleVec(std::vector<double> items){
  std::cout << "[ ";
    for (int k=0; k<items.size(); k++){
      std::cout << items[k] << ' ';
    }
    std::cout << "]" << std::endl;
  return;
};
