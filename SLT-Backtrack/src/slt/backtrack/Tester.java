/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package slt.backtrack;

import java.io.IOException;

/**
 *
 * @author sl1m
 */
public class Tester {
    public static void runTests(int n, int leastEmpty, int mostEmpty) throws IOException {
        //test.print();
        SLTBacktrack solver = new SLTBacktrack();
        for (int i=leastEmpty; i<=mostEmpty; i++) {
            for (int j=0; j<n; j++) {
                solver.steps = 0;
                Board temp = Database.getBoard(i);
                long start = System.nanoTime();
                solver.backtrack(temp);
                long end = System.nanoTime();
                System.out.println(Integer.toString(i) + ' ' + Long.toString(end-start));
            }
        }
    }
}
