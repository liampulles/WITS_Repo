#include "EasyBMP/EasyBMP.h"
using namespace std; 
int main( int argc, char* argv[] ) 
{ 
 BMP Background; 
 Background.ReadFromFile(argv[1]); 

 BMP Output; 
 int picWidth = Background.TellWidth(); 
 int picHeight = Background.TellHeight(); 

 Output.SetSize( Background.TellWidth() , Background.TellHeight() ); 

 Output.SetBitDepth(24); 

 for (int i = 1; i < picWidth-1; ++i)
 {
   for (int j = 1; j < picHeight-1; ++j) { 
    int col = (Background(i, j)->Blue + Background(i,j)->Green + Background(i,j)->Red)/3; 

     if (col > 127) 
     { 
       Output(i,j)->Red = 255 ; 
       Output(i,j)->Blue = Background(i,j)->Blue +10; 
       Output(i,j)->Green = Background(i,j)->Green +10; 
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
