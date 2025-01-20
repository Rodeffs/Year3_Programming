import java.util.Scanner;

public class Main {

    Scanner in = new Scanner(System.in);

    public static void main(String[] args) {
	System.out.println("Hello, World!");

	int a = 5;
	int b = 6;

	System.out.println("Task 1: " + sum(a, b));	
    }

    static int sum(int a, int b) {
	return a + b;
    }
}
