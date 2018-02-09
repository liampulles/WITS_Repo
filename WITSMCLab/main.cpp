//Liam Pulles : 855442
// My perceptron training code!
// Works for any amount of layers and any amount of nodes in layers (where of
// course the first and last layer have the number of input and output nodes
// respectively.
// The program assumes datasets are stored in a "data" directory. The program also requires slight modification to the Dataset file (see file.cpp and the data
// directory) and requires a layerInfo.txt file in the "data" directory (see
// the percept_learn_multi function and layerInfo.txt) for describing the layer structure.

//I suggest starting at main() and following from there.

#include <iostream>
#include <string>
#include "file.cpp"
#include <vector>
#include <cmath>

//We use this to shuffle an "order vector"
void shuffleOrder(std::vector<int>& in){
  auto engine = std::default_random_engine{};
  std::shuffle(std::begin(in), std::end(in), engine);
}

//Not used
double errorVal(std::vector<double> T, std::vector<double> y){
  double total = 0;
  for (int i=0; i<T.size(); i++){
    total = total + std::abs(T[i]-y[i]);
  }
  return total;
}

//This makes our W 3D vector
void createW(std::vector< std::vector< std::vector<double>>>& outside, std::vector<int> layerInfo){
  //We shall assume layerInfo.txt does not count the (-1) node in each layer.
  
  //Dimension description of W: ----------
  //inside -> weights for input x vector.
  //outer -> We have k vec for first layer, n for second, etc. (layerinfo)
  //outside -> there are f layers in total. (layerinfo size)
  
  //"-1" because output layer has no weights. 
  for (int k=0; k<layerInfo.size()-1; k++){
    std::vector< std::vector<double>> outer;
    //+1 for the (-1) node, which we presume isn't counted in layerInfo.
    for (int i=0; i< layerInfo[k]+1; i++){
      std::vector<double>  inside;
      //populate the weights coming out of a SINGLE node.
      randomW(inside,layerInfo[k+1],i,k);
      outer.push_back(inside);
    }
    outside.push_back(outer);
  }
}

//The sigmoid function.
double sigmoid(double x, double b)
{
  return ( 1 / (1 + exp(-1*x*b)) );
}

//Does a dot product.
double DotProduct(std::vector<double> one, std::vector<double> two){
  //Must be same size!
  double out=0;
  for (int i=0; i<one.size(); i++){
    out = out + one[i]*two[i];
  }
  return out;
}

//Calculate the error for all the layers, in prep. for weight update
void ErrorCalc(std::vector< std::vector<double>> X, std::vector< std::vector< std::vector<double>>> W, std::vector<double> T,std::vector< std::vector<double>>& Err, double& topErr){
  //Make the Err vector "outer" shell to be number of layers.
  Err.resize( X.size() , std::vector<double>(0,0) );

  //Last layer firstly: (calculate sum: (tk-yk)^2 / topErr also)
  topErr = 0;
  for (int i=0; i<X[X.size()-1].size(); i++){
    Err[X.size()-1].push_back( X[X.size()-1][i] * (1 - X[X.size()-1][i]) * (T[i] - X[X.size()-1][i]) );
    topErr = topErr + (T[i]-X[X.size()-1][i])*(T[i]-X[X.size()-1][i]);
  }

  //Then for each layer further back (except first).
  for (int k=X.size()-2; k>=1; k--){
    //For each node in that layer
    for (int i=0; i<X[k].size(); i++){
      //Calculate error for this node.
      Err[k].push_back( X[k][i] * (1 - X[k][i]) * DotProduct(W[k][i],Err[k+1]) );
    }
  }
}

//get rid of all the [-1] nodes (needed for proper forward propogation)
void removeNegOnes(std::vector< std::vector<double>>& X){
  for (int i=0; i<X.size(); i++) X[i].pop_back();
  return;
}

//This forms a single "stage" in calcualting the final y vec. at the end.
// i.e. this calculates the output for a single layer.
void progress_forward(std::vector<double> oldX, std::vector< std::vector<double>> W, std::vector<double>& newX, double n){
  //for all nodes in the layer
  for (int j=0; j < newX.size(); j++){
    //for one output node
    //times by appropriate weights
    newX[j]=0;   
    for (int i=0; i< oldX.size(); i++){;
      newX[j] = newX[j] + oldX[i]*W[i][j];
    }
    //apply sigmoid. Note that I set the B paramater 1 - no user option.
    newX[j] = sigmoid(newX[j],1);
  }
  //Add -1 to end of newX. (to be fed as oldX into this function in the future)
  newX.push_back(-1);
  return;
}

//Not used currently
void swap(int *first, int *second)
{
   int temp = *first;
   *first = *second;
   *second = temp;
   return;
} 

//After we get the errors for all the nodes, update the weights.
void WeightUpdate(std::vector< std::vector< std::vector<double>>>& W, std::vector< std::vector<double>> Err, std::vector< std::vector<double>> X, double n){
  //Start from back
  for (int k=W.size()-1; k>=0; k--){
    //for each "out" (i.e. spider head) node
    for (int i=0; i<W[k].size(); i++){
      //for each "in" (i.e. spider feet) node
      for (int j=0; j<W[k][i].size(); j++){
	//I'm hoping this is multiplying the correct Err layer with the
	//correct Weight layer. I'm not getting any Seg faults for any
	//variation of layers, so it seems good...
	W[k][i][j] = W[k][i][j] + n*Err[k+1][i]*X[k][i];
      }
    }
  }
}

void percept_learn_multi(std::vector<int> layerInfo, std::vector< std::vector<double>> X, std::vector< std::vector<double>> T, std::vector< std::vector< std::vector<double>>>& multiW, double n, int rep, std::vector<int> Order){
  //layerInfo.txt stores info about layers. I'll submit an example (look in data).
  //Create a weight vector from layerInfo.txt
  createW(multiW, layerInfo);
  std::cout << "-----------WEIGHTS BEFORE-------------" << std::endl;
  printWeightVec(multiW);

  std::vector< std::vector<double>> totErr;
  double topErrTot = 0;
  for (int f=0; f<rep; f++){
    //ONE RUN THROUGH (i.e. go through the whole dataset once)
    //Shuffle Order
    shuffleOrder(Order);
    for (int i=0; i<X.size(); i++){
      //ONE DATA POINT (i.e. one row in the dataset)
      int j = Order[i];
      //Need an extra (-1) for input X. (progress_forward takes care
      // of doing this for further layers.)
      X[j].push_back(-1);

      //Basically I have two vectors which hold two concurrent layers of nodes.
      //progress_forward updates the second using the first, and then 
      //moves forward 1 layer. i.e. the second becomes the first.
      std::vector< std::vector<double>> nodes;
      nodes.resize( layerInfo.size(), std::vector<double>(0,0) );
      nodes[0] = X[j];
      //do for all layers except last
      for (int k=0; k<layerInfo.size()-1; k++){
	//do for one layer
	nodes[k+1].resize(layerInfo[k+1], 0);
	progress_forward(nodes[k],multiW[k],nodes[k+1],n);
      }

      //now X is our output vector. But we have to remove all the -1's we added.
      removeNegOnes(nodes);

      //First we calc. the errors in each layer.
      std::vector< std::vector<double>> Err;
      double topErr;
      ErrorCalc(nodes,multiW,T[i],Err,topErr);
      //This holds our sum(tk-yk)^2
      topErrTot = topErrTot + topErr;
      //Now we have to update all the weights in each layer.
      WeightUpdate(multiW,Err,nodes,n);
      totErr = Err;
    }
    //Print out sum (tk-yk)^2 * 1/2 (Error)
    topErrTot = topErrTot * 0.5;
    std::cout << "---------(E) ERROR THIS RUN--------------" << std::endl;
    std::cout << topErrTot << std::endl;
    removeNegOnes(X);
  }
  //Now print out our final errors for each node - just to see how much things
  //changed in the last iteration.
  std::cout << "------------FINAL ERROR VECTOR----------" << std::endl;
  printMultiVec(totErr);
}

int main(){
	std::vector< std::vector<double> > X;
	std::vector< std::vector< std::vector<double> > > multiW;
	std::vector< std::vector<double> > T;
	std::vector<int> Order;
	double n;

//Get learn rate.
	std::cout << "Enter learning rate: ";
	std::cin >> n; 

//Get layerInfo.txt
	std::vector<int> layerInfo;
	layers("data/layerInfo.txt",layerInfo);

//Get X, T. Initialize Order.
	std::string fileName;
       	std::cout << "Enter dataset name (in data): ";
	std::cin >> fileName;
	trainSet("data/" + fileName,X,T,Order);

//Get repititions
	int rep;
	std::cout << "Enter no of repititions: ";
	std::cin >> rep;
	
//Print X, W, T (for debugging)
	//std::cout << "X is: " << std::endl;
	//printMultiVec(X);
	//std::cout << "W is: " << std::endl;
	//printSingleVec(W);
	//std::cout << "T is: " << std::endl;
	//printMultiVec(T);

//Try percept learn.
	std::cout << "Learning..." << std::endl;	

	percept_learn_multi(layerInfo,X,T,multiW,n,rep, Order);
	//Our hopefully improved result W
	std::cout << "-----------WEIGHTS AFTER-------------" << std::endl;
	printWeightVec(multiW);

	return 0;
}
