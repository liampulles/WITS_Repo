/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package slt.backtrack;

//-----------------------FOR SIBU AND TSHEPISO-------------------------

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.LinkedList;


public class SLTBacktrack {
    //"Global" solution, filled in by backtrack when board is full.
    public Board solution;
    public int steps = 0;

    public boolean backtrack(Board board){
        ArrayList<Move> moves = getMoves2(board);
        steps++;
        //i.e. at leaf node of tree
        if (moves.isEmpty()) {
            if (isFull(board)) {
                //We have a solution! Save it...
                solution = board.clone();
                return true;
            }
            else {
                return false;
            }
        }
        
        //If we're not a leaf node then we need to call more backtracks.
        Iterator<Move> i=moves.iterator();
        while (i.hasNext()) {
            Move aMove = i.next();
            //Create a new board with a move filled in.
            Board temp = board.clone();
            temp.fillIn(aMove);          
            //Call backtrack on that filled in board.
            if (backtrack(temp)) return true;
        }
        //None of our children has a solution
        return false;
    }

    //Modified from Sibu
    public static boolean isFull(Board board){
        for(int i =0;i<9;i++){
            for(int j=0;j<9;j++){
                if(board.board[i][j]==0) {
                    return false;
                }
            }
        }
        return true;
    }
    
    //Liam says: Had to optimize a bit to avoid StackOverflow
    public static ArrayList<Move> getMoves2(Board board) {
        //Liam says: I set the potential capacity beforehand, so as to avoid the
        //arraylist resizing itself.
        ArrayList<Move> moves = new ArrayList<>(81);
        Move move;
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                //Go to next position in board if not 0
                if (board.board[i][j] != 0) continue;
                for(int num=1;num<=9;num++){
                    move = new Move(i,j,num);
                    if(board.checkPos(move)){
                        moves.add(move);
                    }
                }
            } 
        }
        //Laim says: This seems to make things go faster in general. Probably
        //reach an unfinishable board sooner.
        //Collections.shuffle(moves);
        //System.out.println(moves.size());
        return moves;
    }
    
    public static void main(String[] args) throws IOException {
        //Board test = Database.getBoard(5);
        //test.print();
        //SLTBacktrack solver = new SLTBacktrack();
        //if (solver.backtrack(test)) {
            //solver.solution.print();
            //System.out.println("Steps: " + Integer.toString(solver.steps));
        //} else {
            //System.out.println("No Solution");
        //}
        Tester.runTests(5, 18, 60);
    }
    
}
