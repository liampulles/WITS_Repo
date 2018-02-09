//By Liam Pulles : 855442
//This code basically is for initialisation of vectors, printing vectors, and reading vectors from file. Vectors of dimensions 1D, 2D and 3D (for weights).

#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <cstdlib>
#include <time.h>
#include <algorithm>
#include <random>

//Map some random values for a vector. Use i and k to augment the random seed.
static void randomW(std::vector<double>& W, int size, int i,int k){
  srand((time(NULL)+1)*2*(i+1.2)*(k+7.3)*(k+1));
  for (int i=0; i<size; i++){
    W.push_back( ((double) rand() / (RAND_MAX/2)) - 1);
  }
};

//Make an X and T vector from the e.g Data.txt. Initialize our Order vector (for shuffling)
static void trainSet(std::string fileName, std::vector< std::vector<double> >& X,std::vector< std::vector<double>>& T, std::vector<int>& Order){
  	std::ifstream file;
	int width;
	int count = 0;
	
	file.open(fileName);
	while(file.is_open()){
	  //I modify the e.g. Data.txt to have a single number at the top, which
	  //contains the number of elements in each row.
		file >> width;
		while(!file.eof()){
		  //Create row.
		  std::vector<double> Xrow;
		  for (int i=0; i<width-1; i++){
			  double in;
			  file >> in;
			  Xrow.push_back(in);
	          }
	          X.push_back(Xrow);
		  //Make T -> assumes T is only one node
	          double tin;
		  file >> tin;
		  std::vector<double> Tone;
		  Tone.push_back(tin);
		  T.push_back(Tone);
		  count++;
		}
		break;
	}
	file.close();

	//SHUFFFFFFLLEE!
	Order.resize( count );
	std::iota (std::begin(Order), std::end(Order), 0);

	return;
}

//Convert a file array into a 2d vector. Again I modify the file to include
//a value at the top with the number of elements in each row.
static void multiVec(std::string fileName, std::vector< std::vector<double> >& items){
	std::ifstream file;
	int height;
	int width;

	file.open(fileName);
	while(file.is_open()){
		file >> width;
		file >> height;
		items.resize( width , std::vector<double>( height , 0 ) );
		for (int k=0; k<width; k++){
			for (int i=0; i<height; i++){
				file >> items[k][i];
				
			}
		}
		break;
	}
	file.close();
	return;
};

//Specifically for reading the layers. Only change from singleVec is that this
//is for an int 2d vector.
static void layers(std::string fileName, std::vector<int>& items){
	std::ifstream file;
	int width;

	file.open(fileName);
	while(file.is_open()){
		file >> width;
		items.resize( width, 0 );
		for (int k=0; k<width; k++){
			file >> items[k];
		}
		break;
	}
	file.close();
	return;
}

//Read a file which has a 1D vector. Again, file must be augmented with a value at top.
static void singleVec(std::string fileName, std::vector<double>& items){
	std::ifstream file;
	int width;

	file.open(fileName);
	while(file.is_open()){
		file >> width;
		items.resize( width, 0 );
		for (int k=0; k<width; k++){
			file >> items[k];
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

//Print out the 3D weight vector.
static void printWeightVec(std::vector< std::vector< std::vector<double> > > items){
  for (int i=0; i<items.size(); i++){
    std::cout << "Layer " << i << ":" << std::endl;
    printMultiVec(items[i]);
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
