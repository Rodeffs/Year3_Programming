import java.util.Scanner;

public class Main {

    static Scanner in = new Scanner(System.in);  // чтобы миллион раз не создавать новый сканнер

    public static void main(String[] args) {
	System.out.println("Задания:\n1. Сиракузская последовательность\n2. Сумма ряда\n3. Ищем клад\n4. Логистический максимин\n5. Дважды чётное число");
	System.out.print("Введите номер задания (1-5): ");

	switch(in.nextInt()) {
	    case 1:
		collatz_conjecture();
		break;

	    case 2:
		row_sum();
		break;

	    case 3:
		find_treasure();
		break;

	    case 4:
		find_optimal_path();
		break;

	    case 5:
		twice_even();
		break;

	    default:
		System.out.println("Ошибка: такого задания не было");
	}

	in.close();
    }
    
    // Задание 1

    static void collatz_conjecture() {
	System.out.print("Введите натуральное число: ");
	int n = in.nextInt();

	int count = 0;

	while (n != 1) {
	    if (n % 2 == 0)
		n /= 2;
	    else
		n = 3*n + 1;

	    count++;
	}

	System.out.println("Потребовалось " + count + " шагов");
    } 

    // Задание 2

    static void row_sum() {
	System.out.print("Введите количество чисел в знакочередующемся ряде: ");
	int size = in.nextInt();

	int sum = 0;
	boolean minus = false;

	System.out.println("Введите " + size + " чисел:");

	for (int i = 0; i < size; i++) {
	    int number = in.nextInt();

	    if (minus) {
		sum -= number;
		minus = false;
	    }
	    else {
		sum += number;
		minus = true;
	    }
	}

	System.out.println("Сумма ряда: " + sum);
    }

    // Задание 3

    static void find_treasure() {
	System.out.print("Введите координату x клада: ");
	int x_goal = in.nextInt();

	System.out.print("Введите координату y клада: ");
	int y_goal = in.nextInt();

	int shortest_path = 0, x = 0, y = 0;
	boolean goal_reached = false;
	
	System.out.println("Введите указания:");

	String direction = in.next();
	int steps = in.nextInt();

	// Я сначала подумал, что нужно построить путь, имея на вход лишь исходные данные, но оказалось всё гораздо проще
	// По сути мы тут же идём в указании, которое было введёно, таким образом получим кратчайший путь
	// Очевидно, что если выполнение предыдущих указаний уже привело нас к кладу, то дальше их не надо учитывать

	while (!direction.equals("стоп")) {
	    if ((x == x_goal) && (y == y_goal)) 
		goal_reached = true;
	    
	    // ЗАПОМНИТЬ: в Java оператор == проверяет, что это один и тот же объект, а не одно и то же значение (для этого нужен .equals())

	    if (direction.equals("север"))
		y += steps;
	    else if (direction.equals("юг")) 
		y -= steps;
	    else if (direction.equals("запад")) 
		x -= steps;
	    else if (direction.equals("восток")) 
		x += steps;

	    if (!goal_reached) 
		shortest_path++;	

	    direction = in.next();

	    if (!direction.equals("стоп")) 
		steps = in.nextInt();
	}
	
	System.out.println("Минимальное количество указаний: " + shortest_path);
    }

    // Задание 4
    
    static void find_optimal_path() {
	System.out.print("Введите количество дорог: ");
	int road_count = in.nextInt();

	int optimal_height = Integer.MIN_VALUE, optimal_road = 0;
	
	for (int i = 1; i <= road_count; i++) {
	    System.out.print("Введите количество туннелей для " + i + " дороги: ");
	    int tunnel_count = in.nextInt();

	    int min_tunnel = Integer.MAX_VALUE;

	    System.out.println("Введите высоту каждого туннеля:");

	    for (int j = 0; j < tunnel_count; j++) {
		int current_tunnel = in.nextInt();
		
		if (current_tunnel < min_tunnel)
		    min_tunnel = current_tunnel;
	    }

	    if (min_tunnel > optimal_height) {
		optimal_height = min_tunnel;
		optimal_road = i;
	    }
	}

	String output = String.format("Оптимальные дорога и высота грузовика: %d %d", optimal_road, optimal_height);
	System.out.println(output);
    }

    // Задание 5

    static void twice_even() {
	System.out.print("Введите положительное трёхзначное число: ");
	int number = in.nextInt();

	int sum = 0, mult = 1;

	while (number >= 1) {
	    int digit = number % 10;
	    sum += digit;
	    mult *= digit;
	    number /= 10;
	}

	if ((sum % 2 == 0) && (mult % 2 == 0))
	    System.out.println("Это дважды чётное число");
	else
	    System.out.println("Это не дважды чётное число");
    }
}
