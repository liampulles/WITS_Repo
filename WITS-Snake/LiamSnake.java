
import java.awt.Point;
import java.util.*;

public class ExampleSnake {

    static final int UP = 0;
    static final int DOWN = 1;
    static final int LEFT = 2;
    static final int RIGHT = 3;
    static final int numApples = 2;
    int numSnakes = 4;
    int width, height;
    int [][] dirVec = new int[3][3];
    
    public ExampleSnake() {
        Scanner in = new Scanner(System.in);
        getParameters(in); // get the game parameters
        
        //set direction mapping, RxR -> R (1,1 is center):
        dirVec[1][0] = UP;
        dirVec[1][2] = DOWN;
        dirVec[0][1] = LEFT;
        dirVec[2][1] = RIGHT;
        
        while (true) { // This stuff must be done on every move
        	int[][] colBoard = new int [width][height];
            Point[] apples = getApples(in); // Gets the coordinates of the apples
            int mySnake = getSnakeNumber(in); // get the number of your snake
            //System.out.println("log "+mySnake);
            String[] snakes = getSnakes(in); // get snake lines
            ArrayList<Point> enemies = new ArrayList<Point>();
            boolean[] power = new boolean[1];
            power[0] = false;
            int[] myLength= new int[1];
            myLength[0] = 0;
            Point head = constructBoard(colBoard,snakes,mySnake,enemies,power,myLength);
            //printBoard(colBoard);
            int move;
            try {
            	move = calculateMove(apples, snakes, head, colBoard, enemies, power, myLength); //Figures out which move to make
            } catch (Exception e) {
            	move = UP;
            }
            System.out.print(move+"\n");// prints out the move, which communicates the move to the game
            colBoard=null; //Garbage collector, take care of it.
        }
    }

    public void printBoard(int[][] colBoard){
    	for (int i = 0; i < height; i++){
    		for (int k = 0; k < width; k++){
    			System.out.print(colBoard[k][i]);
    			System.out.print(' ');
    		}
    		System.out.print('\n');
    	}
    }
    
    public Point getPoint(String in){
    	String[] coord = in.split(",");
    	return new Point(Integer.parseInt(coord[0]),Integer.parseInt(coord[1]));
    }
    
    public void fillLine (Point fir, Point sec, int[][] colBoard, int snakeNum){
    	for (int i = Integer.min(fir.x,sec.x); i <= Integer.max(fir.x,sec.x); i++){
    		for (int k = Integer.min(fir.y,sec.y); k<= Integer.max(fir.y,sec.y) ; k++){
    			colBoard[i][k] = snakeNum+1;//for snake 0 ... won't be visible
    		}
    	}
    }
    
    public void tryFillHead(int snakeNum, Point head, int[][] colBoard){
    	Point temp = new Point(0,0);
    	int count=0;
    	if (colBoard[head.x+1][head.y]==snakeNum+1){
    		temp.x = temp.x + 1;
    		count++;
    	}
    	if (colBoard[head.x-1][head.y]==snakeNum+1){
    		temp.x = temp.x - 1;
    		count++;
    	}
    	if (colBoard[head.x][head.y+1]==snakeNum+1){
    		temp.y = temp.y + 1;
    		count++;
    	}
    	if (colBoard[head.x][head.y-1]==snakeNum+1){
    		temp.y = temp.y - 1;
    		count++;
    	}
    	if (count==1) colBoard[head.x+temp.x][head.y+temp.y]=9;
    	return;
    }
    
    public Point constructBoard(int[][] board,String[] snakes, int mySnake, ArrayList<Point> enemies, boolean[] power, int[] myLength){
    	Point head = new Point(0,0);
    	power[0] = snakes[mySnake].split(" ")[0].equals("power");
    	for (int i = 0; i < snakes.length; i++){
    		String[] snakeStr = snakes[i].split(" ");
    		boolean temp = false;
    		temp = (power[0])&&(i!=mySnake); //we shouldn't do next bit if this.
    		if ((!temp)&&(!snakeStr[0].equals("dead"))) {
    			Point prev = getPoint(snakeStr[3]);
    			for (int k = 4; k < snakeStr.length; k++){
    				if (i==mySnake) myLength[0]++;
    				Point next = getPoint(snakeStr[k]);
    				fillLine(prev, next, board, i);
    				prev = next;
    			}
    		}
    		if (i==mySnake){
    			head = getPoint(snakeStr[3]);
    		} else {
    			if (!snakeStr[0].equals("dead")){
    				enemies.add(getPoint(snakeStr[3]));
    				//tryFillHead(i,getPoint(snakeStr[3]),board);
    			}
    		}
    	}
    	//board[head.x][head.y]=9;
    	return head;
    }
    
    public Point greedyGo(Point dir, Point alt, Point head, int[][] colBoard){
    	//Preferred direction?
    	if (colBoard[head.x+dir.x][head.y+dir.y] == 0) return dir;
    	//Alternate direction?
    	if (colBoard[head.x+alt.x][head.y+alt.y] == 0) return alt;
    	//Opposite of Alternate direction?
    	if (colBoard[head.x-alt.x][head.y-alt.y] == 0) return new Point(alt.x*-1,alt.y*-1);
    	//Opposite of Preferred direction?!? Only option left...
    	return new Point(dir.x*-1,dir.y*-1);
    }

    public Point findEmptyBlockNear(int[][] colBoard, Point Target){
    	if (colBoard[Target.x][Target.y] == 0) return Target;
    	//Test a "cross" of increasing radius
    	for (int rad=1; rad<50; rad++){
    		if ((Target.x-rad>0)&&(colBoard[Target.x-rad][Target.y]==0)) return new Point(Target.x-rad,Target.y);
    		if ((Target.x+rad<50)&&(colBoard[Target.x+rad][Target.y]==0)) return new Point(Target.x+rad,Target.y);
    		if ((Target.y-rad>0)&&(colBoard[Target.x][Target.y-rad]==0)) return new Point(Target.x,Target.y-rad);
    		if ((Target.y+rad<50)&&(colBoard[Target.x][Target.y+rad]==0)) return new Point(Target.x,Target.y+rad);
    	}
    	return Target;
    }
    
    public Point findStrategicCentre(ArrayList<Point> enemies){
		//find closest enemy to middle
    	int Dist=Math.abs(enemies.get(0).x-25)+Math.abs(enemies.get(0).y-25);
    	Point closest_mid = new Point(enemies.get(0).x,enemies.get(0).y);
    	for (int i=1; i<enemies.size(); i++){
    		if (Math.abs(enemies.get(i).x-25)+Math.abs(enemies.get(i).y-25)<=Dist){
    			closest_mid.x=enemies.get(i).x;
    			closest_mid.y=enemies.get(i).y;
    		}
    	}
    	
    	//find square "radius"
    	int rad = 0;
    	if (Math.abs(closest_mid.y-25)>=Math.abs(closest_mid.x-25)){
    		rad = Math.abs(closest_mid.y-25);
    	} else {
    		rad = Math.abs(closest_mid.x-25);
    	}
    	
    	//find mean point
    	Point mean = findMean(enemies);
    	
    	//find m in equation y+25=m(x+25)
    	float m = (mean.y-25)/(mean.x-25);
    	
    	//find square_point
    	Point square_point = new Point();
    	if (Math.abs(m)>1){ //intersects vertical
    		if (mean.y-25<0){ //bottom side
    			square_point.y = 25-rad;
    		} else { //top side
    			square_point.y = 25+rad;   			
    		}
			square_point.x = Math.round((square_point.y/m) + (25/m) - 25); 
    	} else { //intersects horizontal
    		if (mean.x-25<0){ //left side
    			square_point.x = 25-rad;
    		} else { //right side
    			square_point.x = 25+rad;
    		}
    		square_point.y = Math.round((m*square_point.x)+(25*m)-25);
    	}
    	
    	//get pre_target (closest to middle)
    	Point pre_target = new Point();
    	if ( ((mean.x*mean.x)+(mean.y*mean.y)) <= ((square_point.x*square_point.x)+(square_point.y*square_point.y)) ){ //mean closest
    		pre_target = mean;
    	} else { //square_point closest
    		pre_target = square_point;
    	}
    	
    	//get point one closer to centre
    	Point fin = pre_target.getLocation();
    	if (Math.abs(m)>1){ //manipulate x
    		if (m>0){ //put to left.
    			fin.x = fin.x - 1;
    		} else { //put to right
    			fin.x = fin.x + 1;
    		}
    	} else { //manipulate y;
    		if (m>0){ //put to bottom;
    			fin.y = fin.y - 1;
    		} else { //put to top;
    			fin.y = fin.y + 1;
    		}
    	}
    	
    	return fin;
    }
    
    public Point findMean(ArrayList<Point> enemies){
    	Point tot = new Point(0,0);
    	for (int i=0; i<enemies.size(); i++){
    		tot.x = tot.x + enemies.get(i).x;
    		tot.y = tot.y + enemies.get(i).y;
    	}
    	tot.x = (int)Math.round(tot.x/enemies.size());
    	tot.y = (int)Math.round(tot.y/enemies.size());
    	return tot;
    }
    
    public Point findMeanPolar(ArrayList<Point> enemies, Integer enem_count){
    	Point mean = findMean(enemies);
    	if (mean.x>25){
    		mean.x = 25 - (mean.x-25);
    	} else {
    		mean.x = 25 + (25-mean.x);
    	}
    	
    	if (mean.y>25){
    		mean.y = 25 - (mean.y-25);
    	} else {
    		mean.y = 25 + (25-mean.y);
    	}
    	return mean;
    }
    
    public Point greedyGoStraight(Point dirr,Point head,int[][] colBoard){
    	Point dir = new Point((int)Math.signum(dirr.x),0);
    	Point alt = new Point(0,(int)Math.signum(dirr.y));
    	return greedyGo(dir,alt,head,colBoard);
    }
    
    public Point findSector(Point Target){
    	//make sectors
    	Point temp = new Point();
    	Point closest = new Point(25,25);
    	float dist = 99999999;
    	for (int i=0; i<3; i++){
    		for (int k=0; k<3; k++){
    			temp.x = (int)Math.round(8.333333+(16.666666*k));
    			temp.y = (int)Math.round(8.333333+(16.666666*i));
    			int distx = temp.x - Target.x;
    			int disty = temp.y - Target.y;
    			if ( ((distx*distx)+(disty*disty)) < dist){
    				dist = ((distx*distx)+(disty*disty));
    				closest = temp.getLocation();
    			}
    		}
    	}
    	return closest;
    }
    
    public boolean recursiveFill(Point head,int[][] fillBoard,int iterations){
    	//return true if at least one doesn't hit a dead end before iterations = 0.
    	if (fillBoard[head.x][head.y]!=0) return false;
    	fillBoard[head.x][head.y] = 9;
    	if (iterations==0) return true;
    	if ((head.x+1<=49)&&(recursiveFill(new Point(head.x+1,head.y),fillBoard,iterations-1))) return true;
    	if ((head.x-1>=0)&&(recursiveFill(new Point(head.x-1,head.y),fillBoard,iterations-1))) return true;
    	if ((head.y+1<=49)&&(recursiveFill(new Point(head.x,head.y+1),fillBoard,iterations-1))) return true;
    	if ((head.y-1>=0)&&(recursiveFill(new Point(head.x,head.y-1),fillBoard,iterations-1))) return true;
    	return false;
    }
    
    public int numChoices(Point head,int[][] colBoard){
    	int checks=0;
    	if (colBoard[head.x+1][head.y]==0) checks++;
    	if (colBoard[head.x-1][head.y]==0) checks++;
    	if (colBoard[head.x][head.y+1]==0) checks++;
    	if (colBoard[head.x][head.y-1]==0) checks++;
    	return checks;
    }
    
    public Point smartGo(Point fir,Point sec,Point head,int[][] colBoard){
    	int iterations=20; //what depth? speed..
    	Point main = greedyGo(fir,sec,head,colBoard); //main choice
    	int[][] fillBoard = colBoard.clone();
    	fillBoard[head.x][head.y]=9;
    	if (!recursiveFill(new Point(head.x+main.x,head.y+main.y),fillBoard,iterations)){ //cut off if go here
    		colBoard[head.x+main.x][head.y+main.y]=9;
    		if (numChoices(head,colBoard)==0){ //if there is no other choice, then go with it.
    			colBoard[head.x+main.x][head.y+main.y]=0;
    			return main;
    		}
    		return smartGo(fir,sec,head,colBoard); //if there is a choice, keep that path "blocked" and choose another route.
    	}
    	return main; //good to go!
    }
    
    public int calculateMove(Point[] apples, String[] snakes, Point head, int[][] colBoard, ArrayList<Point> enemies, boolean[] power, int[] myLength) {
        //for (String s:snakes){
        //    System.out.println("log "+s);
        //}
        //Current strategy: smartly move to apple if close, else smartly move to sector.
        Point Target = apples[1].getLocation();
        if (apples[0].x!=-1) Target = apples[0].getLocation();
        Point diff = new Point(Target.x - head.x,Target.y-head.y);
        for (int i = 0; i < enemies.size(); i++){
        	Point enem_diff = new Point(Target.x - enemies.get(i).x,Target.y - enemies.get(i).y);
        	if ( (!power[0]) && ( (Math.abs(enem_diff.x)+Math.abs(enem_diff.y)) <= (Math.abs(diff.x)+Math.abs(diff.y)) ) ){
        		if (myLength[0]>=30){
        			break;
        		} else {
        			//go to middle.
        			Point mean = findMean(enemies);
        			Target = new Point((int)Math.round((mean.x+25)/2),(int)Math.round((mean.y+25)/2)); //findEmptyBlockNear(colBoard, new Point(25,25)); //centre
        			//Target = new Point(25,25);
        			Target = findSector(Target);
        			//Target = findEmptyBlockNear(colBoard,Target);
        		}
        		diff = new Point(Target.x - head.x,Target.y-head.y);
        		break;
        	}
        }
        
        Point ret = new Point();
        //if (Math.abs(diff.x)+Math.abs(diff.y)<7){
        //	ret = greedyGoStraight(diff,head,colBoard);
       // } else {
        	Point fir;
        	Point sec;
        	if (diff.x <= 0) fir = new Point(-1,0); else fir = new Point(1,0);
        	if (diff.y <= 0) sec = new Point(0,-1); else sec = new Point(0,1);
        	if (diff.x*diff.x <= diff.y*diff.y){
        		Point temp = fir.getLocation();
        		fir = sec.getLocation();
        		sec = temp.getLocation();
        	}
        	//ret = greedyGo(fir,sec,head,colBoard);
        	ret = smartGo(fir,sec,head,colBoard);
       // }
        return dirVec[1+ret.x][1+ret.y];
    }

//===================================================================
//----------------------Standard stuff-------------------------------    
//===================================================================
    
    public int getSnakeNumber(Scanner in) {
        String snakeNumber = in.nextLine();
        return Integer.parseInt(snakeNumber);
    }

    public String[] getSnakes(Scanner in) {
        String[] snake = new String[numSnakes];
        for (int i = 0; i < numSnakes; i++) {
            snake[i] = in.nextLine();
        }
        return snake;
    }

    public Point[] getApples(Scanner in) {
        Point[] apples = new Point[numApples];
        for (int i = 0; i < numApples; i++) {
            String appleString = in.nextLine();
            String[] appleComponents = appleString.split(" ");
            int appleX = Integer.parseInt(appleComponents[0]);
            int appleY = Integer.parseInt(appleComponents[1]);
            apples[i] = new Point(appleX, appleY);
        }
        return apples;
    }

    public void getParameters(Scanner in) {
        String firstLine = in.nextLine();
        String[] firstComponents = firstLine.split(" ");
        numSnakes = Integer.parseInt(firstComponents[0]);
        width = Integer.parseInt(firstComponents[1]);
        height = Integer.parseInt(firstComponents[1]);
    }

    public static void main(String[] args) {
        new ExampleSnake();
    }
}

