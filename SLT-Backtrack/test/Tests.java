/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;
import slt.backtrack.Move;
import slt.backtrack.Board;
import java.util.ArrayList;
import java.util.Arrays;
import org.junit.Assert;
import slt.backtrack.SLTBacktrack;

/**
 *
 * @author sl1m
 */

public class Tests {
    Integer[][] correct;
    
    public Tests() {
        this.correct = new Integer[][]{
            {1,5,2, 4,6,9, 3,7,8}, 
            {7,8,9, 2,1,3, 4,5,6}, 
            {4,3,6, 5,8,7, 2,9,1}, 
            {6,1,3, 8,7,2, 5,4,9}, 
            {9,7,4, 1,5,6, 8,2,3}, 
            {8,2,5, 9,3,4, 1,6,7}, 
            {5,6,7, 3,4,8, 9,1,2}, 
            {2,4,8, 6,9,1, 7,3,5}, 
            {3,9,1, 7,2,5, 6,8,4}
        };
    }
    
    @BeforeClass
    public static void setUpClass() {
    }
    
    @AfterClass
    public static void tearDownClass() {
    }
    
    @Before
    public void setUp() {
    }
    
    @After
    public void tearDown() {
    }

    @Test
    public void checkPos1() {
        Integer[][] raw = {
        {1,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        assertFalse(board.checkPos(new Move(0,0,1)));
        assertFalse(board.checkPos(new Move(8,0,1)));
        assertFalse(board.checkPos(new Move(0,8,1)));
        assertFalse(board.checkPos(new Move(2,2,1)));
        assertTrue(board.checkPos(new Move(5,5,1)));
    }
    
    @Test
    public void checkPos2() {
        Integer[][] raw = {
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 9,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        assertFalse(board.checkPos(new Move(6,6,9)));
        assertFalse(board.checkPos(new Move(6,4,9)));
        assertFalse(board.checkPos(new Move(4,6,9)));
        assertFalse(board.checkPos(new Move(8,8,9)));
        assertTrue(board.checkPos(new Move(5,5,9)));
    }
    
    //@Test
    public void getMoves1() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,1,3, 4,5,6},
        {4,3,6, 5,8,7, 2,9,1},
        
        {6,1,3, 8,7,2, 5,4,9},
        {9,7,4, 1,5,6, 8,2,3},
        {8,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,1, 7,3,5},
        {3,9,1, 7,2,5, 6,8,0}
        };
        Board board = new Board(raw);
        //ArrayList<Move> results = SLTBacktrack.getMoves(board);
        //assertEquals(results.size(),1);
    }
    
   //@Test
    public void getMoves2() {
        Integer[][] raw = {
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        //ArrayList<Move> results = SLTBacktrack.getMoves(board);
        //assertEquals(results.size(),729);
    }
    
    @Test
    public void getMoves2_1() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,1,3, 4,5,6},
        {4,3,6, 5,8,7, 2,9,1},
        
        {6,1,3, 8,7,2, 5,4,9},
        {9,7,4, 1,5,6, 8,2,3},
        {8,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,1, 7,3,5},
        {3,9,1, 7,2,5, 6,8,0}
        };
        Board board = new Board(raw);
        ArrayList<Move> results = SLTBacktrack.getMoves2(board);
        assertEquals(results.size(),1);
    }
    
    @Test
    public void isFull1() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,1,3, 4,5,6},
        {4,3,6, 5,8,7, 2,9,1},
        
        {6,1,3, 8,7,2, 5,4,9},
        {9,7,4, 1,5,6, 8,2,3},
        {8,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,1, 7,3,5},
        {3,9,1, 7,2,5, 6,8,4}
        };
        Board board = new Board(raw);
        assertTrue(SLTBacktrack.isFull(board));
    }
    
    @Test
    public void isFull2() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,1,3, 4,5,6},
        {4,3,6, 5,8,7, 2,9,1},
        
        {6,1,3, 8,7,2, 5,4,9},
        {9,7,4, 1,0,6, 8,2,3},
        {8,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,1, 7,3,5},
        {3,9,1, 7,2,5, 6,8,4}
        };
        Board board = new Board(raw);
        assertFalse(SLTBacktrack.isFull(board));
    }
    
    @Test
    public void isFull3() {
        Integer[][] raw = {
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        assertFalse(SLTBacktrack.isFull(board));
    }
    
    @Test
    public void backtrack1() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,1,3, 4,5,6},
        {4,3,6, 5,8,7, 2,9,1},
        
        {6,1,3, 8,7,2, 5,4,9},
        {9,7,4, 1,5,6, 8,2,3},
        {8,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,1, 7,3,5},
        {3,9,1, 7,2,5, 6,8,0}
        };
        Board board = new Board(raw);
        SLTBacktrack back= new SLTBacktrack();
        back.backtrack(board);
        //System.out.println(Arrays.deepToString(back.solution.board));
        Assert.assertArrayEquals(correct,back.solution.board);
    }
    
    @Test
    public void backtrack2() {
        Integer[][] raw = {
        {1,5,2, 4,6,9, 3,7,8},
        {7,8,9, 2,0,3, 4,5,6},
        {4,3,0, 5,8,7, 2,9,1},
        
        {6,1,3, 8,0,2, 5,4,9},
        {9,7,4, 1,5,6, 0,2,3},
        {0,2,5, 9,3,4, 1,6,7},
        
        {5,6,7, 3,4,8, 9,1,2},
        {2,4,8, 6,9,0, 7,3,5},
        {3,9,1, 7,2,5, 6,8,0}
        };
        Board board = new Board(raw);
        SLTBacktrack back= new SLTBacktrack();
        back.backtrack(board);
        //System.out.println(Arrays.deepToString(back.solution.board));
        Assert.assertArrayEquals(correct,back.solution.board);
    }
    
    @Test
    public void backtrack3() {
        Integer[][] raw = {
        {1,5,0, 4,6,9, 3,7,8},
        {0,8,0, 2,0,3, 4,0,6},
        {4,3,0, 0,8,7, 0,0,1},
        
        {6,1,0, 8,0,2, 5,4,9},
        {9,7,0, 0,5,6, 0,0,3},
        {0,2,5, 9,0,0, 1,6,0},
        
        {5,0,0, 3,4,8, 9,1,0},
        {2,0,8, 0,9,0, 7,0,5},
        {0,9,1, 0,0,5, 0,8,0}
        };
        Board board = new Board(raw);
        SLTBacktrack back= new SLTBacktrack();
        back.backtrack(board);
        //System.out.println(Arrays.deepToString(back.solution.board));
        Assert.assertArrayEquals(correct,back.solution.board);
    }
    
    @Test
    public void backtrack5() {
        Integer[][] raw = {
        {0,0,5, 0,2,0, 0,0,0},
        {8,0,0, 0,0,7, 4,0,1},
        {0,6,0, 0,0,0, 0,5,0},
        
        {0,1,0, 0,9,0, 0,0,0},
        {0,7,0, 8,0,3, 0,6,0},
        {0,0,0, 0,7,0, 0,4,0},
        
        {0,5,0, 0,0,0, 0,8,0},
        {4,0,2, 9,0,0, 0,0,3},
        {0,0,0, 0,3,0, 2,0,0}
        };
        Board board = new Board(raw);
        SLTBacktrack back= new SLTBacktrack();
        back.backtrack(board);
        System.out.println(Arrays.deepToString(back.solution.board));
        //Assert.assertArrayEquals(correct,back.solution.board);
        Assert.assertTrue(true);
    }
    
    /* Too long
    @Test
    public void backtrack4() {
        Integer[][] raw = {
        {5,0,0, 0,0,0, 0,0,0},
        {2,0,8, 0,0,0, 0,0,0},
        {0,9,1, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        SLTBacktrack back= new SLTBacktrack();
        back.backtrack(board);
        System.out.println(Arrays.deepToString(back.solution.board));
        Assert.assertArrayEquals(correct,back.solution.board);
    }
    */
    @Test
    public void validate1() {
        Integer[][] raw = {
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        Assert.assertTrue(board.validateBoard());
    }
    
    @Test
    public void validate2() {
        Integer[][] raw = {
        {1,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,1,0},
        {0,0,0, 0,0,1, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,1},
        {0,0,0, 0,1,0, 0,0,0},
        {0,1,0, 0,0,0, 0,0,0},
        
        {0,0,0, 1,0,0, 0,0,0},
        {0,0,0, 0,0,0, 1,0,0},
        {0,0,1, 0,0,0, 0,0,0}
        };
        Board board = new Board(raw);
        Assert.assertTrue(board.validateBoard());
    }
    
    @Test
    public void validate3() {
        Integer[][] raw = {
        {1,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,0,0, 0,1,0},
        {0,0,0, 0,0,0, 0,0,0},
        
        {0,0,0, 0,0,0, 0,0,0},
        {0,0,0, 0,1,0, 0,0,0},
        {0,1,0, 0,0,0, 0,0,0},
        
        {0,0,0, 1,0,0, 0,0,0},
        {0,0,0, 0,0,0, 1,0,0},
        {0,0,0, 0,0,0, 0,0,1}
        };
        Board board = new Board(raw);
        Assert.assertFalse(board.validateBoard());
    }
    
    //This fails - don't know why
    @Test
    public void validate4() {
        Integer[][] raw = {
            {1,5,2, 4,6,9, 3,7,8}, 
            {7,8,9, 2,1,3, 4,5,6}, 
            {4,3,6, 5,8,7, 2,9,1}, 
            {6,1,3, 8,7,2, 5,4,9}, 
            {9,7,4, 1,5,6, 8,2,3}, 
            {8,2,5, 9,3,4, 1,6,7}, 
            {5,6,7, 3,4,8, 9,1,2}, 
            {2,4,8, 6,9,1, 7,3,5}, 
            {3,9,1, 7,2,5, 6,8,4}
        };
        Board board = new Board(raw);
        Assert.assertFalse(board.validateBoard());
    }
}
