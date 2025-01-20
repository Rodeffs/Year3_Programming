import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
	System.out.println("Задания:\n1. Сиракузская последовательность\n2. Сумма ряда\n3. Ищем клад\n4. Логистический максимин\n5. Дважды чётное число");
	System.out.print("Введите номер задания (1-5): ");

	Scanner in = new Scanner(System.in);

	int lab = in.nextInt();

	switch(lab) {
	    case 1:
		System.out.print("Введите натуральное число: ");

		collatz_conjecture(in.nextInt());

		System.out.println("Потребовалось " + count + " шагов");
		break;

	    case 2:
		System.out.print("Введите количество чисел в знакочередующемся ряде: ");
		int size = in.nextInt();
		int[] numbers = new int[size];
    
		System.out.println("Введите " + size + " чисел:");

		for (int i = 0; i < size; i++) {
		    numbers[i] = in.nextInt();
		}

		System.out.println("Сумма ряда: " + row_sum(numbers));
		break;

	    case 3:
		System.out.print("Введите координату x клада: ");
		int x = in.nextInt();
		System.out.print("Введите координату y клада: ");
		int y = in.nextInt();

		System.out.println("Минимальное количество указаний: " + find_treasure(x, y));
		break;

	    case 4:
		System.out.print("Введите количество дорог: ");
		int road_count = in.nextInt();
		
		ArrayList<ArrayList<Integer>> roads = new ArrayList<ArrayList<Integer>>();

		for (int i = 1; i <= road_count; i++) {
		    ArrayList<Integer> road = new ArrayList<Integer>();

		    System.out.print("Введите количество туннелей для " + i + " дороги: ");
		    int tunnel_count = in.nextInt();
		    System.out.println("Введите высоту каждого туннеля:");

		    for (int j = 0; j < tunnel_count; j++) {
			road.add(in.nextInt());
		    }

		    roads.add(road);
		}

		int[] optimal = max_height(roads);
		
		String output = String.format("Оптимальные дорога и высота грузовика: %d %d", optimal[0], optimal[1]);
		System.out.println(output);
		break;

	    case 5:
		System.out.print("Введите положительное трёхзначное число: ");

		if (twice_even(in.nextInt())) {
		    System.out.println("Это дважды чётное число");
		}
		else {
		    System.out.println("Это не дважды чётное число");
		}
		break;

	    default:
		System.out.println("Ошибка: такого задания не было");
	}

	in.close();
    }
    
    // Задание 1

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

    // Задание 2

    static boolean minus = false;

    static int row_sum(int[] numbers) {
	int sum = 0;

	for (int number : numbers) {
	    if (minus) {
		sum -= number;
		minus = false;
	    }
	    else {
		sum += number;
		minus = true;
	    }
	}

	return sum;
    }

    // Задание 3

    static int find_treasure(int x_goal, int y_goal) {
	int shortest_path = 0, x = 0, y = 0;
	boolean goal_reached = false;
	Scanner in = new Scanner(System.in);
	
	System.out.println("Введите указания:");

	String direction = in.next();
	int steps = in.nextInt();

	// Я сначала подумал, что нужно построить путь, имея на вход лишь исходные данные, но оказалось всё гораздо проще
	// По сути мы тут же идём в указании, которое было введёно, таким образом получим кратчайший путь
	// Очевидно, что если выполнение предыдущих указаний уже привело нас к кладу, то дальше их не надо учитывать

	while (!direction.equals("стоп")) {
	    if ((x == x_goal) && (y == y_goal)) {
		goal_reached = true;
	    }
	    
	    // ЗАПОМНИТЬ: в Java оператор == проверяет, что это один и тот же объект, а не одно и то же значение (для этого нужен .equals())

	    if (direction.equals("север")) {
		y += steps;
	    }
	    else if (direction.equals("юг")) {
		y -= steps;
	    }
	    else if (direction.equals("запад")) {
		x -= steps;
	    }
	    else if (direction.equals("восток")) {
		x += steps;
	    }

	    if (!goal_reached) {
		shortest_path++;	
	    }

	    direction = in.next();

	    if (!direction.equals("стоп")) {
		steps = in.nextInt();
	    }
	}
	
	in.close();
	return shortest_path;
    }

    // Задание 4

    static int find_min(ArrayList<Integer> array) {
	int min = Integer.MAX_VALUE;

	for (int i : array) {
	    if (i < min) {
		min = i;
	    }
	}

	return min;
    }

    static int[] max_height(ArrayList<ArrayList<Integer>> roads) {
	int[] optimal_road = new int[2];
	int max = Integer.MIN_VALUE;

	for (int i = 0; i < roads.size(); i++) {
	    int lowest_tunnel = find_min(roads.get(i));

	    if (lowest_tunnel > max) {
		max = lowest_tunnel;
		optimal_road[0] = i+1;
		optimal_road[1] = max;
	    }
	}

	return optimal_road;
    }

    // Задание 5

    static boolean twice_even(int number) {
	int sum = 0, mult = 1;

	while (number >= 1) {
	    int digit = number % 10;
	    sum += digit;
	    mult *= digit;
	    number /= 10;
	}

	if ((sum % 2 == 0) && (mult % 2 == 0)) {
	    return true;
	}

	return false;
    }
}
