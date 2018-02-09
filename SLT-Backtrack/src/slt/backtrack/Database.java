/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package slt.backtrack;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 *
 * @author sl1m
 */
public class Database {
    public static Board getBoard(int spaces) throws IOException {
        spaces = Integer.min(81,Integer.max(0,spaces));
        //System.out.println(System.getProperty("user.dir"));
        String line = randomLine("Sudoku/123456789.txt");
        Integer[][] board = new Integer[9][9];
        List<Integer> shuffle = new ArrayList<>();
        for (int i=0; i<9; i++){
            for (int j=0; j<9; j++) {
                board[i][j] = line.charAt((i*9)+j) - '0';
                shuffle.add((i*9)+j);
            }
        }
        Collections.shuffle(shuffle);
        for (int i=0; i<spaces; i++) {
            int item = shuffle.get(i);
            board[item/9][item%9] = 0;
        }
        return new Board(board);
    }
    
    public static String randomLine(String sfile) throws FileNotFoundException, IOException
    {
        File file = new File(sfile);
        RandomAccessFile f = new RandomAccessFile(file, "r");
        double random = Math.random();
        long loc = (long) (random * f.length());
        f.seek(loc);
        //Skip a line
        f.readLine();
        return f.readLine();
    }
}
