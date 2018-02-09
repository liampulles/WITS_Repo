#include "EasyBMP/EasyBMP.h"
using namespace std; 
int main( int argc, char* argv[] ) 
{ 
  //read in input image from first input argument and store in Background
 BMP Background; 
 Background.ReadFromFile(argv[1]); 

 //declare output BMP to hold the new black and white image
 BMP Output; 
 //get width and height of input image
 int picWidth = Background.TellWidth(); 
 int picHeight = Background.TellHeight(); 
 //set the output image to those dimensions
 //since we're only manipulating pixel values 
 //so the dimensions will be wthe same
 Output.SetSize( Background.TellWidth() , Background.TellHeight() ); 
 //set outputs bit depth to 1 since we're converiting to B&W
 Output.SetBitDepth(1); 

 //Now loop through the width and height of the image
 //to access each pixel's Red, Green and Blue value
 //Then store the average in 'col', and if its bigger than 127
 //set that pixel to white (255) if not set it to black.
 for (int i = 1; i < picWidth-1; ++i)
 {
   for (int j = 1; j < picHeight-1; ++j) { 
    int col = (Background(i, j)->Blue + Background(i,j)->Green + Background(i,j)->Red)/3; 

     if (col > 127) 
     { 
       Output(i,j)->Red = 255; 
       Output(i,j)->Blue = 255; 
       Output(i,j)->Green = 255; 
     } 

     else { 
      Output(i,j)->Red = 0; 
      Output(i,j)->Blue = 0; 
      Output(i,j)->Green = 0; 
    }

  } 

} 

//Write the output image to the second input argument

Output.WriteToFile(argv[2]); 
return 0; 
} 
