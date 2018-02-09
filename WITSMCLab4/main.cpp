//=========================PLEASE READ:===========================
//Name: Liam Pulles
//Student no: 855442
//
// This file contains the main algorithms for k-Means.
//
// This code uses the min-max normalization method, and it runs both
// the normal k-Means Online and the normalized one for comparison.
//
// The k-Means algorithm is able to stop running if the max change
// in a cluster is sufficiently small, however in practice it almost
// always runs tha max number of iterations (ITERATION_MAX).
// Both the k-Means Online algorithms run for a fixed number of
// iterations (ITERATION_MAX) due to the decreasing learning rate
// based on the iteration number ( 1/1+count ).
//================================================================

#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <cmath>
#include <vector>
#include <string.h>
#include <cstdlib>
#include <time.h>
#include <algorithm>
#include <random>
#include "file.cpp"

#define ITERATION_MAX 1000

//Euclidean
double distance(std::vector<double> x, std::vector<double> y){
  double dist = 0;;
  for (int i=0; i<x.size(); i++){
    dist += (x[i]-y[i])*(x[i]-y[i]);
  }
  return std::sqrt(dist);
}

double squareDistance(std::vector<double> x, std::vector<double> y){
  double dist = 0;;
  for (int i=0; i<x.size(); i++){
    dist += (x[i]-y[i])*(x[i]-y[i]);
  }
  return dist;
}

double sumOfSquares(std::vector< std::vector<double>> clusters, std::vector< std::vector<double>> X, std::vector< std::vector<int>> assignment) {
  double tot;
  for (int i=0; i<clusters.size(); i++) {
    for (int j=0; j<assignment[i].size(); j++){
      tot = tot + squareDistance(clusters[i],X[assignment[i][j]]);
    }
  }
  return tot;
}

//returns the largest change in a cluster.
double error(std::vector< std::vector<double>> prevClusters, std::vector< std::vector<double>> clusters){
  double totdist = distance(prevClusters[0],clusters[0]);
  for (int i=1; i<clusters.size(); i++){
    if (distance(prevClusters[i],clusters[i]) > totdist){
      totdist = distance(prevClusters[i],clusters[i]);
    }
  }
  return totdist;
}

int findClosestCluster(std::vector<double> x, std::vector< std::vector<double>> clusters){
  int choice = 0;
  double closest = distance(x, clusters[0]);
  for (int i=1; i<clusters.size(); i++){
    if (distance(x,clusters[i]) < closest){
      choice = i;
    }
  }
  return choice;
}

void makeClustersNorm(int k, std::vector< std::vector< double>>& X, std::vector< std::vector< double >>& clusters){
  //Get clusters to right dimensions
  int dimensions = X[0].size();
  clusters.resize(k, std::vector<double> (dimensions,0));

  srand (time(NULL));
  for (int i=0; i<k; i++){
    for (int j=0; j<dimensions; j++){
      //Between 0 and 1
      clusters[i][j] = ((double) rand() / RAND_MAX);
    }
  }
}

void makeClusters(int k, std::vector< std::vector< double>>& X, std::vector< std::vector< double >>& clusters){
  int dimensions = X[0].size();
  clusters.resize(k, std::vector<double> (dimensions,0));
  
  //Find max and min over whole data set in each dimension of X.
  std::vector<double> min;
  min.resize(dimensions, 0);
  std::vector<double> max;
  max.resize(dimensions, 0);

  for (int i=0; i<dimensions; i++){
    min[i] = X[0][i];
    max[i] = X[0][i];
    for (int j=1; j<X.size(); j++){
      if (X[j][i] < min[i]){
	min[i] = X[j][i];
      }
      if (X[j][i] > max[i]){
	max[i] = X[j][i];
      }      
    }
  }

  //Assign random values over max-min range.
  srand (time(NULL));
  for (int i=0; i<k; i++){
    for (int j=0; j<dimensions; j++){
      clusters[i][j] = min[j] + (rand() % (int)(max[j] - min[j] + 1));
    }
  }
}

void moveToMean(std::vector<double>& point, std::vector<int> xPoints, std::vector< std::vector<double>> X){
  //Leave if cluster empty
  if (xPoints.size() == 0) return;
  std::vector<double> mean;
  mean.resize(point.size(), 0);
  //Traverse through the X points which are assigned to the cluster
  for (int i=0; i<xPoints.size(); i++){
    for (int j=0; j<mean.size(); j++){
      mean[j] += X[i][j];
    }
  }
  
  //Change point.
  for (int i=0; i<mean.size(); i++){
      point[i] = mean[i] / xPoints.size();
  }
  return;
}

void kMeansLoop(std::vector< std::vector<double>>& clusters, std::vector< std::vector<double>>& X) {
  //Which datapoints are assigned to each cluster? That's this vector.
  std::vector< std::vector<int>> assignment;
  std::cout << "==================================" << std::endl;
  std::cout << "Running k-means algorithm...";

  //To hold the previous clusters in an iteration
  std::vector< std::vector<double>> prevClusters;
  
  //Algorithm loop.
  int count = 0;
  do {
    //"Empty" assignment.
    assignment.resize(0);
    assignment.resize(clusters.size());
    prevClusters = clusters;
    for (int i=0; i<X.size(); i++){
      int closest = findClosestCluster(X[i],clusters);
      assignment[closest].push_back(i);
    }
    for (int j=0; j<clusters.size(); j++){
      moveToMean(clusters[j],assignment[j],X);
    }
    count++;
  } while ((count < ITERATION_MAX)&&(error(prevClusters,clusters) > 0.001));
  std::cout << "DONE" << std::endl;

  //return the cluster centres:
  if (count == ITERATION_MAX){
    std::cout << "Max iterations reached (" << count << ')' << std::endl;
  } else {
    std::cout << "Number of iterations: " << count << std::endl;
  }

  //Get unnormalized for sum of squares
  std::cout << "Sum of squares error: " << sumOfSquares(clusters,X,assignment) << std::endl;
  
  std::cout << "k-Means Cluster centres:" << std::endl;
  printMultiVec(clusters);
  std::cout << "==================================" << std::endl;
}

void updateCluster(std::vector<double>& cluster, std::vector<double>& x, double n){
  for (int i=0; i<cluster.size(); i++){
    cluster[i] = cluster[i] + n*(x[i] - cluster[i]);
  }
}

void kMeansOnlineLoop(std::vector< std::vector<double>>& clusters, std::vector< std::vector<double>>& X) {
  //Which datapoints are assigned to each cluster? That's this vector.
  std::vector< std::vector<int>> assignment;
  std::cout << "==================================" << std::endl;
  std::cout << "Running k-means Online algorithm...";

  //To hold the previous clusters in an iteration
  std::vector< std::vector<double>> prevClusters;

  //Ordering vector
  std::vector<int> Order;
  Order.resize( X.size() );

  //Shuffling engine
  auto engine = std::default_random_engine{};
  
  //Algorithm loop.
  int count = 0;
  do {
    //Learning rate
    double n = 1/(count+1);
    prevClusters = clusters;
    //Shuffle Ordering
    std::shuffle(std::begin(Order), std::end(Order), engine);
    for (int i=0; i<X.size(); i++){
      int j = Order[i];
      int closest = findClosestCluster(X[j],clusters);
      updateCluster(clusters[closest],X[j],n);
    }
    count++;
  } while ((count < ITERATION_MAX));
  std::cout << "DONE" << std::endl;

  //Get assignment.
  assignment.resize(clusters.size());
  for (int i=0; i<X.size(); i++){
    int closest = findClosestCluster(X[i],clusters);
    assignment[closest].push_back(i);
  }

  //return the cluster centres:
  std::cout << "Fixed number of iterations (" << count << ')' << std::endl;

  std::cout << "Sum of squares error: " << sumOfSquares(clusters,X,assignment) << std::endl;
  
  std::cout << "k-Means Online Cluster centres:" << std::endl;
  printMultiVec(clusters);
  std::cout << "==================================" << std::endl;
}

double dotProduct(std::vector<double> x, std::vector<double> y){
  double total = 0;
  for (int i=0; i< x.size(); i++){
    total += x[i]*y[i];
  }
  return total;
}

int findClosestClusterNormed(std::vector<double> x, std::vector< std::vector<double>> clusters){
  //Do dot products of x and clusters and find largest
  int choice = 0;
  double closest = dotProduct(x,clusters[0]);
  for (int i=1; i<clusters.size(); i++){
    double run = dotProduct(x,clusters[i]);
    if (run > closest){
      closest = run;
      choice = i;
    }
  }
  return choice;
}

void findMinMax(std::vector< std::vector<double>>& X, std::vector<double>& min, std::vector<double>& max){
  //Find max and min in each dimension
  min = X[0];
  max = X[0];
  for (int i=0; i<X.size(); i++){
    for (int j=0; j<X[i].size(); j++){
      if (X[i][j] > max[j]) max[j] = X[i][j];
      if (X[i][j] < min[j]) min[j] = X[i][j];
    }
  }
}

void normalizeX(std::vector< std::vector<double>>& X, std::vector<double>& min, std::vector<double>& max){
  //Normalize X (min-max)
  for (int i=0; i<X.size(); i++){
    for (int j=0; j<X[i].size(); j++){
      X[i][j] = (X[i][j] - min[j])/(max[j]-min[j]);
    }
  }
}

void unNormalizeX(std::vector< std::vector<double>>& X, std::vector<double>& min, std::vector<double>& max){
  //UnNormalize X (min-max)
  for (int i=0; i<X.size(); i++){
    for (int j=0; j<X[i].size(); j++){
      X[i][j] = min[j] + X[i][j]*(max[j] - min[j]);
    }
  }
}

void kMeansOnlineNormedLoop(std::vector< std::vector<double>>& clusters, std::vector< std::vector<double>>& X) {
  //Which datapoints are assigned to each cluster? That's this vector.
  std::vector< std::vector<int>> assignment;
  assignment.resize(clusters.size());
  std::cout << "==================================" << std::endl;
  std::cout << "Running k-means Online Normalized algorithm...";

  //To hold the previous clusters in an iteration
  std::vector< std::vector<double>> prevClusters;

  //Ordering vector
  std::vector<int> Order;
  Order.resize( X.size() );

  //Shuffling engine
  auto engine = std::default_random_engine{};
  
  //Algorithm loop.
  int count = 0;
  do {
    //Learning rate
    double n = 1/(count+1);
    prevClusters = clusters;
    //Shuffle Ordering
    std::shuffle(std::begin(Order), std::end(Order), engine);
    for (int i=0; i<X.size(); i++){
      int j = Order[i];
      int closest = findClosestClusterNormed(X[j],clusters);
      updateCluster(clusters[closest],X[j],n);
    }
    count++;
  } while ((count < ITERATION_MAX));
  std::cout << "DONE" << std::endl;

  //return the cluster centres:
  std::cout << "Fixed number of iterations (" << count << ')' << std::endl;

  //Get assignment.
  assignment.resize(clusters.size());
  for (int i=0; i<X.size(); i++){
    int closest = findClosestCluster(X[i],clusters);
    assignment[closest].push_back(i);
  }

  std::cout << "Sum of squares error: " << sumOfSquares(clusters,X,assignment) << std::endl;
  
  std::cout << "k-Means Online Normalized Cluster centres:" << std::endl;
  printMultiVec(clusters);
  std::cout << "==================================" << std::endl;
}

int main(void){
  //Get number of clusters
  int k;
  std::cout << "Specify the number of clusters (k):";
  std::cin >> k;

  //Get dataset
  std::vector< std::vector< double >> X;
  std::string dataSetName;
  std::cout << "Specify the name of the dataset file:";
  std::cin >> dataSetName;
  std::cout << "Getting dataset...";
  dataSet(dataSetName, X);
  std::cout << "DONE" << std::endl;
  std::cout << "Normalizing dataSet...";
  std::vector<double> min;
  std::vector<double> max;
  findMinMax(X,min,max);
  normalizeX(X,min,max);
  std::cout << "DONE" << std::endl;

  std::cout << "Initializing clusters...";
  //Generate cluster set
  std::vector< std::vector<double>> clusters;
  makeClustersNorm(k, X, clusters);
  std::cout << "DONE" << std::endl;

  std::cout<< "Initial Clusters:" << std::endl;
  printMultiVec(clusters);

  //Do k-Means
  std::vector< std::vector<double>> clusters1 = clusters;
  kMeansLoop(clusters1, X);

  //Do k-Means Online
  std::vector< std::vector<double>> clusters2 = clusters;
  kMeansOnlineLoop(clusters2, X);

  //Do k-Means Online Normalized
  kMeansOnlineNormedLoop(clusters,X);
}
