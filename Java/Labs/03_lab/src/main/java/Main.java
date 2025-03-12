import java.util.ArrayList;
import java.util.Calendar;
import java.util.Scanner;

import cinema.*;
import login.*;

public class Main {
    static ArrayList<Cinema> cinemas = new ArrayList<Cinema>();
    static ArrayList<Screening> schedule = new ArrayList<Screening>();
    static Scanner in = new Scanner(System.in);

    public static void main(String[] args) {
	initialize();

	Admin admin = new Admin("admin", "12345");
	admin.setCinemaList(cinemas);
	admin.setSchedule(schedule);

	User user = new User("user", "54321");
	
	System.out.println("Please, enter account information");
	
	while (true) {
	    System.out.print("Login: ");
	    var login = in.nextLine();
	    
	    System.out.print("Password: ");
	    var password = in.nextLine();

	    if (login.equals("admin")) {
		if (admin.login(login, password)) {
		    System.out.println("Logged in as admin. Enter 'h' to list the commands");
		    break;
		}
		System.out.println("Incorrect password! Please, enter again");
	    }

	    else {
		System.out.println("Welcome! Enter 'h' to list the commands");
		break;
	    }
	}

	while (true) {
	    var input = in.next();

	    if (input.equals("h") || input.equals("help")) {
		if (admin.isLoggedIn())
		    System.out.println("Commands:\n'h' or 'help' - print this message\n's' or 'schedule' - print the full screenings schedule\n'c' or 'closest' - reserve for the closest screening\n'r' or 'reserve' - make a reservation by manually selecting a screening\n'ac' - add cinema\n'ec' - edit cinema\n'rc' - remove cinema\n'as' - add screening to schedule\n'es' - edit schedule\n'rs' - remove screening from schedule");

		else
		    System.out.println("Commands:\n'h' or 'help' - print this message\n's' or 'schedule' - print the full screenings schedule\n'c' or 'closest' - reserve for the closest screening\n'r' or 'reserve' - make a reservation by manually selecting a screening");
	    }

	    else if (input.equals("s") || input.equals("schedule"))
		System.out.println(User.scheduleToString(schedule));

	    else if (input.equals("c") || input.equals("closest")) {
		System.out.print("Movie title: ");
		var title = in.next();

		System.out.print("Amount of tickets: ");
		var tickets = in.nextInt();
		
		var closest = User.findClosestScreening(schedule, title, Calendar.getInstance(), tickets);

		if (closest != null) {
		    System.out.print(closest.toString());
		    System.out.print("Make a reservation for this screening? (Y/n): ");
		    input = in.next();

		    if (!input.equals("n") && !input.equals("no"))
			buyingTickets(closest.getHall(), tickets);
		    System.out.println("Reservation made!");
		}

		else
		    System.out.println("Error, no matching screenings were found");
	    }

	    else if (input.equals("r") || input.equals("reserve")) {
		System.out.print("Enter the screening number to make a reservation for: ");
		var num = in.nextInt();
		
		if ((num < 1) || (num > schedule.size()))
		    System.out.println("Error, this screening doesn't exist");

		else {
		    System.out.print("Amount of tickets: ");
		    var tickets = in.nextInt();

		    var hall = schedule.get(num-1).getHall();

		    if (tickets > hall.getFreeSeats())
			System.out.println("Error, there isn't enough free seats");

		    else {
			System.out.print(schedule.get(num-1).toString());
			System.out.print("Make a reservation for this screening? (Y/n): ");
			input = in.next();
			if (!input.equals("n") && !input.equals("no"))
			    buyingTickets(hall, tickets);
			System.out.println("Reservation made!");
		    }
		}
	    }

	    else if (input.equals("q") || input.equals("quit"))
		break;

	    else
		System.out.println("Error, unknown command. Enter 'h' to list the commands");
	}

    }

    public static void buyingTickets(Hall hall, int tickets) {
	int i = 1;

	while (i <= tickets) {
	    System.out.println(hall.toString());
	    System.out.println("Choose a seat for person %d:".formatted(i));

	    System.out.print("Row: ");
	    var row = in.nextInt() - 1;
	    System.out.print("Seat number: ");
	    var num = in.nextInt() - 1;

	    try {
		if (hall.isSeatOccupied(row, num))
		    System.out.println("This seat is already occupied!");

		else {
		    hall.occupySeat(row, num);
		    i++;
		}
	    }

	    catch (Exception e){
		System.out.println("This seat doesn't exist!");
	    }
	}
    }

    public static void initialize() {  // исходные данные для тестинга

	// Кинотеарты

	Cinema cinema1 = new Cinema("Rodina");
	cinemas.add(cinema1);

	Cinema cinema2 = new Cinema("Karo");
	cinemas.add(cinema2);

	Cinema cinema3 = new Cinema("Кinopark");
	cinemas.add(cinema3);

	// Залы в кинотеатрах

	Hall hall1_1 = new Hall();
	Hall hall1_2 = new Hall();

	hall1_1.addRow(6);
	hall1_1.addRow(8);
	hall1_1.addRow(10);
	hall1_1.addRow(12);

	hall1_2.addRow(5);
	hall1_2.addRow(5);
	hall1_2.addRow(8);
	hall1_2.addRow(8);

	cinema1.getHalls().add(hall1_1);
	cinema1.getHalls().add(hall1_2);

	Hall hall2_1 = new Hall();
	Hall hall2_2 = new Hall();
	Hall hall2_3 = new Hall();

	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	
	hall2_2.addRow(5);
	hall2_2.addRow(6);
	hall2_2.addRow(7);
	hall2_2.addRow(8);
	hall2_2.addRow(9);

	hall2_3.addRow(20);
	hall2_3.addRow(18);
	hall2_3.addRow(15);
	hall2_3.addRow(10);

	cinema2.getHalls().add(hall2_1);
	cinema2.getHalls().add(hall2_2);
	cinema2.getHalls().add(hall2_3);

	Hall hall3_1 = new Hall();

	hall3_1.addRow(25);

	cinema3.getHalls().add(hall3_1);

	// Сеансы
	
	Calendar s1_date = Calendar.getInstance();
	s1_date.add(Calendar.DATE, 10);
	Screening s1 = new Screening(s1_date, cinema1, "Balatro", 120, 0);
	schedule.add(s1);

	Calendar s2_date = Calendar.getInstance();
	s2_date.add(Calendar.DATE, 20);
	Screening s2 = new Screening(s2_date, cinema2, "Minecraft", 150, 1);
	schedule.add(s2);

	Calendar s3_date = Calendar.getInstance();
	s3_date.add(Calendar.DATE, 10);
	Screening s3 = new Screening(s3_date, cinema1, "Balatro", 120, 1);
	schedule.add(s3);

	Calendar s4_date = Calendar.getInstance();
	s4_date.add(Calendar.DATE, 19);
	Screening s4 = new Screening(s2_date, cinema3, "Minecraft", 150, 0);
	schedule.add(s4);

	Calendar s5_date = Calendar.getInstance();
	s5_date.add(Calendar.HOUR, 2);
	Screening s5 = new Screening(s5_date, cinema1, "Terraria", 100, 0);
	schedule.add(s5);
    }
}
