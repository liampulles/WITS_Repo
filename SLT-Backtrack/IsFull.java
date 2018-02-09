/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package aaaassign;

/**
 *
 * @author Sbu
 */
public class IsFull {
    int [][]board;
    int count = 0;
    boolean isFull(){
    for(int i =0;i<9;i++){
         for(int j=0;j<9;j++){
             if(board[i][j]!=0){
//                 count +=board[i][j];//should we check if the board is correct??
                 return true;
             }
             else{
                 return false;
             }
             
                 
             }   
             }
        
    


