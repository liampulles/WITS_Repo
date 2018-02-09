/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package slt.backtrack;

//----------------------------FOR LIAM


public class Board {

    @Override
    public Board clone() {
        Integer[][] result = new Integer[board.length][];
        for (int r = 0; r < board.length; r++) {
            result[r] = board[r].clone();
        }
        //System.out.println("Hey");
        return new Board(result);
    }
    
    //"Root" node of tree, i.e. partial sudoku game goes in here
    public Board(Integer[][] board) {
        this.board = board;
    }
    
    //Always 9x9
    //first array is x coord, second is y coord, i.e. row then column
    public Integer[][] board;
    
    
    //Returns true if pos is available, false if it is invalid for a move.
    public boolean checkPos(Move move) {
        if (board[move.x][move.y]!=0) return false;
        //Check row and column
        int blockx = move.x/3;
        int blocky = move.y/3;
        for (int i=0; i<9; i++) {
            if (board[i][move.y] == move.num) return false;
            if (board[move.x][i] == move.num) return false;
            //For a block - think about it
            if (board[(blockx*3)+(i%3)][(blocky*3)+(i/3)] == move.num) return false;
        }
        return true;
    }
    
    public void fillIn(Move move) {
        //Liam says: This is so straightforward that I'm not going
        //           to write tests for it. :P
        board[move.x][move.y] = move.num;
    }
    
    //For validateBoard - debugging
    public boolean checkPos2(Move move) {
        //Check row
        for (int i=0; i<9; i++) {
            if (i==move.x) continue;
            if (board[i][move.y] == move.num) return false;
        }
        //Check column
        for (int i=0; i<9; i++) {
            if (i==move.y) continue;
            if (board[move.x][i] == move.num) return false;
        }
        //Check block
        int blockx = move.x/3;
        int blocky = move.y/3;
        for (int i=blockx*3; i<(blockx*3) + 3; i++) {
            for (int j=blocky*3; j<(blocky*3) + 3; j++) {
               if ((i==move.x)&&(j==move.y)) continue;
                if (board[i][j] == move.num) return false;
            }
        }
        return true;
    }
    
    //For debugging
    public boolean validateBoard() {
        for (int i=0; i<9; i++) {
            for (int j=0; j<9; j++) {
                if (board[i][j] != 0) {
                    if (!checkPos2(new Move(i,j,board[i][j]))) return false;
                }
            }
        }
        return true;
    }
    
    public void print() {
        System.out.println("===========");
        for (int i=0; i<9; i++) {
            for (int j=0; j<9; j++) {
                System.out.print(board[i][j]);
                if ((j+1)%3 == 0) System.out.print(' ');
            }
            System.out.print('\n');
            if ((i<8)&&((i+1)%3 == 0)) System.out.print('\n');
        }
        System.out.println("===========");
    }
}
