/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package slt.backtrack;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import static slt.backtrack.SLTBacktrack.isFull;

/**
 *
 * @author sl1m
 */
public class Optimized {
        
    
    public boolean backtrack2(Board board){
        LinkedList<LinkedList<Move>> moves = getMoves5(board);
 //       steps++;
        //if (steps%100000 == 0) System.out.println(steps);
        //i.e. at leaf node of tree
        if (moves.isEmpty()) {
            if (isFull(board)) {
                //We have a solution! Save it...
 //               solution = board.clone();
                return true;
            }
            else {
                return false;
            }
        }
        
        //If we're not a leaf node then we need to call more backtracks.
        Iterator<LinkedList<Move>> i=moves.iterator();
        while (i.hasNext()) {
            Iterator<Move> j = i.next().iterator();
            while(j.hasNext()) {
                Move aMove = j.next();
                //Create a new board with a move filled in.
                Board temp = board.clone();
                temp.fillIn(aMove);          
                //Call backtrack on that filled in board.
                if (backtrack2(temp)) return true;
            }
        }
        //None of our children has a solution
        return false;
    }
    
        //FOR TSHEPISO
    public static ArrayList<Move> getMoves(Board board) {
        ArrayList<Move> moves = new ArrayList<>();
        Move move;
        for(int num=1;num<=9;num++){
            
            for(int i=0;i<9;i++){
                
                for(int j=0;j<9;j++){
                    move = new Move(i,j,num);
                    if(board.checkPos(move)){
                        moves.add(move);
                    }
                }
                
            }
            
        }
        
        return moves;
    }
    
    public static LinkedList<LinkedList<Move>> getMoves3(Board board) {
        LinkedList<LinkedList<Move>> moves = new LinkedList<>();
        Move move;
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                //Go to next position in board if not 0
                if (board.board[i][j] != 0) continue;
                LinkedList<Move> pos = new LinkedList<>();
                for(int num=1;num<=9;num++){
                    move = new Move(i,j,num);
                    if(board.checkPos(move)){
                        pos.push(move);
                    }
                }
                if (pos.size() == 1) moves.addFirst(pos);
                else moves.addLast(pos);
            } 
        }
        return moves;
    }
    
    public static LinkedList<LinkedList<Move>> getMoves4(Board board) {
        LinkedList<LinkedList<Move>> moves = new LinkedList<>();
        Move move;
        int smallest = 9;
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                //Go to next position in board if not 0
                if (board.board[i][j] != 0) continue;
                LinkedList<Move> pos = new LinkedList<>();
                for(int num=1;num<=9;num++){
                    move = new Move(i,j,num);
                    if(board.checkPos(move)){
                        pos.push(move);
                    }
                }
                if (pos.size() <= smallest) { 
                    moves.addFirst(pos);
                    smallest = pos.size();
                }
                else moves.addLast(pos);
                //System.out.println(smallest);
            } 
        }
        if (smallest == 1) System.out.println();
        return moves;
    }
    
    public static LinkedList<LinkedList<Move>> getMoves5(Board board) {
        LinkedList<LinkedList<Move>> moves = new LinkedList<>();
        Move move;
        //boolean trouble = true;
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                //Go to next position in board if not 0
                if (board.board[i][j] != 0) continue;
                LinkedList<Move> pos = new LinkedList<>();
                for(int num=1;num<=9;num++){
                    move = new Move(i,j,num);
                    if(board.checkPos(move)){
                        pos.push(move);
                    }
                }
                moves.push(pos);
                //if (pos.size() == 1) trouble = false;
            } 
        }
        
        //if (trouble) System.out.println("Trouble");
        //else System.out.println("Nice");
        
        //lambda expression defines comparator
        Collections.sort(moves, (LinkedList<Move> a, LinkedList<Move> b) -> Integer.valueOf(a.size()).compareTo(b.size()));
        
        return moves;
    }
}
