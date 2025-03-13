import java.util.ArrayList;
import java.util.Calendar;
import java.util.Scanner;

import cinema.*;

public class Main {
    static ArrayList<Cinema> cinemas = new ArrayList<Cinema>();
    static ArrayList<Screening> schedule = new ArrayList<Screening>();

    public static void main(String[] args) {
	Scanner in = new Scanner(System.in);

	initialize();

	User admin = new User("admin", "12345", true);
	User user = new User();

	System.out.println("Please, enter account information");
	
	while (true) {
	    System.out.print("Login: ");
	    var login = in.nextLine();
	    
	    System.out.print("Password: ");
	    var password = in.nextLine();

	    if (login.equals("admin")) {
		if (admin.login(login, password)) {
		    user = admin;
		    System.out.println("Logged in as admin. Enter 'h' to list the commands");
		    break;
		}
		System.out.println("Incorrect password! Please, enter again");
	    }

	    else {
		user.setUsername(login);
		user.setPassword(password);
		user.login(login, password);
		System.out.println("Welcome! Enter 'h' to list the commands");
		break;
	    }
	}

	user.setCinemaList(cinemas);
	user.setSchedule(schedule);

	while (true) {
	    var input = in.next();

	    if (input.equals("h")) 
		System.out.println("Commands:\n'h' - print this message\n's' - print the full screenings schedule\n'pc' - print the list of cinemas\n'c' - print the closest screening\n'r' - make a reservation\n'q' - quit the program\n\nAdmin commands:\n'ac' - add cinema\n'ec' - edit cinema\n'rc' - remove cinema\n'as' - add screening to schedule\n'es' - edit schedule\n'rs' - remove screening from schedule");

	    else if (input.equals("pc")) 
		System.out.println(user.cinemasToString());

	    else if (input.equals("ac") && user.isAdmin()) {
		System.out.print("Enter the name of the new cinema: ");

		if (user.addCinema(in.next()) < 0)
		    System.out.println("Error, there isn't such a cinema");
	    }

	    else if (input.equals("ec") && user.isAdmin()) {
		System.out.println(admin.cinemasToString());

		System.out.print("Enter the cinema number to be edited");
		var cinemaIndex = in.nextInt() - 1;

		System.out.println("EDITING MODE - CINEMA\nEnter 'h' to list commands");

		while (true) {
		    input = in.next();

		    if (input.equals("h"))
			System.out.println("Options:\n'nn' - new name for cinema\n'ah' - add hall\n'eh - edit hall\n'rh' - remove hall\n'ph' - print halls\n'h' - print this message\n'q' - quit EDITING MODE - CINEMA");

		    else if (input.equals("nn")) {
			System.out.print("Enter the new name for cinema (schedule will also be updated): ");

			if (user.newCinemaName(cinemaIndex, in.next()) < 0) 
			    System.out.println("Error, there isn't such a cinema");
		    }

		    else if (input.equals("ah")) {
			System.out.print("Enter the amount of rows in the new hall: ");
			int rows = in.nextInt();
			int[] seatsPerRow = new int[rows];
			
			for (int i = 0; i < rows; i++) {
			    System.out.print("Enter the amount of seats in row %d: ".formatted(i+1));
			    seatsPerRow[i] = in.nextInt();
			}

			if (user.addHall(cinemaIndex, seatsPerRow) < 0) 
			    System.out.println("Error, there isn't such a cinema");
		    }

		    else if (input.equals("rh")) {
			System.out.print("WARNING! Schedule will be also affected. Proceed (y/N)? ");
			input = in.next();

			if (input.equals("y") || input.equals("Y")) {
			    System.out.print("Enter the hall number to be removed: ");
			    if (user.removeHall(cinemaIndex, in.nextInt()-1) < 0)
				System.out.println("Error, there isn't such a cinema or hall");
			}
		    }

		    else if (input.equals("ph"))
			System.out.println(user.cinemaHallScheme(cinemaIndex));

		    else if (input.equals("eh")) {
			System.out.println(user.cinemaHallScheme(cinemaIndex));

			System.out.print("Enter the hall number to be edited: ");
			var hallIndex = in.nextInt() - 1;

			System.out.println("EDITING MODE - HALL\nEnter 'h' to list commands");

			while (true) {    
			    input = in.next();

			    if (input.equals("h"))
				System.out.println("Options:\n'ar' - add row\n'rr' - remove row\n'pr' - print hall scheme\n'rsd' - reset seat data\n'h' or 'help' - print this message\n'q' or 'quit' - quit EDITING MODE - HALL");

			    else if (input.equals("ar")) {
				System.out.print("Enter the amount of seats in the new row: ");

				if (user.addRowToHall(cinemaIndex, hallIndex, in.nextInt()) < 0)
				    System.out.println("Error, there isn't such a cinema or hall");
			    }

			    else if (input.equals("rr")) {
				System.out.println("WARNING, schedule will be altered as well! Proceed (y/N)? ");
				input = in.next();

				if (input.equals("y") || input.equals("Y")) {
				    System.out.println(user.hallScheme(cinemaIndex, hallIndex));
				    System.out.println("Enter the row number to remove: ");
				    if (user.removeRowFromHall(cinemaIndex, hallIndex, in.nextInt()-1) < 0)
					System.out.println("Error, there isn't such a cinema, hall or row");
				}
			    }

			    else if (input.equals("pr"))
				System.out.println(user.hallScheme(cinemaIndex, hallIndex));

			    else if (input.equals("rsd")) {
				System.out.println("WARNING, scheduled seats will be reset! Proceed (y/N)? ");
				input = in.next();

				if (input.equals("y") || input.equals("Y"))
				    if (user.resetSeatsData(cinemaIndex, hallIndex) < 0)
					System.out.println("Error, there isn't such a cinema or hall");
			    }

			    else if (input.equals("q")) {
				System.out.println("QUITTING EDITING MODE - HALL");
				break;
			    }

			    else
				System.out.println("Error, unknown command. Enter 'h' to list the commands");
			}
		    }

			else if (input.equals("as") && user.isAdmin()) {

			}

			else if (input.equals("q")) {
			    System.out.println("QUITTING EDITING MODE - CINEMA");
			    break;
			}

			else
			    System.out.println("Error, unknown command. Enter 'h' to list the commands");
		    }
	    }

	    else if (input.equals("rc") && user.isAdmin()) {
		System.out.println("WARNING, schedule will be altered as well! Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y")) {
		    System.out.println(admin.cinemasToString());
		    System.out.print("Enter the cinema number to remove (will be removed from schedule as well): ");
		    if (user.removeCinema(in.nextInt()-1) < 0)
			System.out.println("Error, there isn't such a cinema");
		}
	    }

	    else if (input.equals("s"))
		System.out.println(user.scheduleToString());

	    else if (input.equals("c")) {
		System.out.print("Movie title: ");
		var title = in.next();

		System.out.print("Amount of tickets: ");
		var tickets = in.nextInt();
		
		var closest = user.findClosestScreening(title, Calendar.getInstance(), tickets);

		if (closest != null) 
		    System.out.print(closest.toString());

		else
		    System.out.println("Error, no matching screenings were found");
	    }

	    else if (input.equals("r")) {
		System.out.println("Choose (1, 2, 3):\n1. Make a reservation for the closest screening\n2. Make a manual reservation\n3. Return");
		input = in.next();

		if (input.equals("1")) {
		    System.out.print("Movie title: ");
		    var title = in.next();

		    System.out.print("Amount of tickets: ");
		    var tickets = in.nextInt();

		    if (user.makeReservationForClosest(title, Calendar.getInstance(), tickets) < 0)
			System.out.println("Error, no matching screenings were found");
		    else
			System.out.println("Reservation made");
		    }

		else if (input.equals("2")) {
		    System.out.println(user.scheduleToString());
		    System.out.print("Enter the screening number to make a reservation for: ");
		    var num = in.nextInt()-1;

		    System.out.print("Amount of tickets: ");
		    var tickets = in.nextInt();

		    if (user.makeReservation(num, tickets) < 0)
			System.out.println("Error, this screening doesn't exist or doesn't have enough free seats");
		    else
			System.out.println("Reservation made");
		}
	    }

	    else if (input.equals("q"))
		break;

	    else
		System.out.println("Error, unknown command or you don't have access. Enter 'h' to list the commands");
	}

	in.close();
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
