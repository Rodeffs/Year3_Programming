import java.util.Scanner;

public class Main {


    public static void main(String[] args) {
	
	System.out.println("Введите номер задания (1-5):");
	System.out.println("1. Сиракузская последовательность\n2. Сумма ряда\n3. Ищем клад\n4. Логистический максимин\n5. Дважды чётное число");

	Scanner in = new Scanner(System.in);

	int lab = in.nextInt();

	switch(lab) {
	    case 1:
		System.out.println("Введите натуральное число:");
		int n = in.nextInt();
		collatz_conjecture(n);
		System.out.println("Потребовалось " + count + " шагов");
		break;

	    case 2:
		break;

	    case 3:
		break;

	    case 4:
		break;

	    case 5:
		break;

	    default:
		System.out.println("Ошибка: такого задания не было");
	}

	in.close();
    }

    static int count = 0;

    static void collatz_conjecture(int n) {
	if (n == 1) {
	    return;
	}
	else if (n % 2 == 0) {
	    n /= 2;
	}
	else {
	    n = 3*n + 1;
	}

	count++;
	collatz_conjecture(n);
    }


}
