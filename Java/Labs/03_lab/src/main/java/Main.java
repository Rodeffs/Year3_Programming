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

	int cinemaIndex = -1, hallIndex = -1, screeningIndex = -1;

	while (true) {
	    var input = in.next();

	    if (input.equals("h")) 
		System.out.println("Commands:\n'h'  - print this message\n'ps' - print the full screenings schedule\n'pc' - print the list of cinemas\n'ph' - print halls for cinema\n'pr' - print specified hall scheme\n'c'  - print the closest screening\n'r'  - make a reservation for the closest screening\n'rm' - make a manual reservation\n'q'  - quit the program\n\nAdmin commands:\n'ac' - add cinema\n'ec' - select cinema for editing\n'rc' - remove cinema\n'as' - add screening to schedule\n'es' - select screening for editing\n'rs' - remove screening from schedule\n\nEdit cinema commands:\n'nn' - new name for cinema\n'ah' - add hall\n'eh' - select hall for editing\n'rh' - remove hall\n\nEdit hall commands:\n'ar' - add row\n'rr' - remove row\n'rsd' - reset seat data\n\nEdit schedule commands:\n'st' - set time & date\n'sch' - set cinema and hall\n'sm' - set movie title\n'sd' - set duration\n'fas' - free all seats\n\nEdit commands are there so you won't have to select the same thing for multiple edits at the same time\nThe drawback is that you will have to first enter an edit command, before actually editing\nFor instance, to add hall to a cinema, first use 'es' to select a cinema and then 'ah' to actually add\n");

	    else if (input.equals("ps"))
		System.out.print(user.scheduleToString());
	    
	    else if (input.equals("pc")) 
		System.out.println(user.cinemasToString());

	    else if (input.equals("ph")) {
		System.out.print("Enter the cinema number to print halls for: ");
		System.out.println(user.cinemaHallScheme(in.nextInt()-1));
	    }

	    else if (input.equals("pr")) {
		System.out.print("Enter the cinema number: ");
		int cinemaIndexTemp = in.nextInt()-1;
		
		System.out.print("Enter the hall number from this cinema: ");
		System.out.println(user.hallScheme(cinemaIndexTemp, in.nextInt()-1));
	    }

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
		System.out.print("Movie title: ");
		var title = in.next();

		System.out.print("Amount of tickets: ");
		var tickets = in.nextInt();

		User.errorHandling(user.makeReservationForClosest(title, Calendar.getInstance(), tickets));
	    }

	    else if (input.equals("rm")) {
		System.out.println(user.scheduleToString());
		System.out.print("Enter the screening number to make a reservation for: ");
		var num = in.nextInt()-1;

		System.out.print("Amount of tickets: ");
		var tickets = in.nextInt();

		User.errorHandling((user.makeReservation(num, tickets)));
	    }

	    else if (input.equals("q"))
		break;

	    else if (input.equals("ac")) {
		System.out.print("Enter the name of the new cinema: ");
		User.errorHandling(user.addCinema(in.next()));
	    }

	    else if (input.equals("ec")) {
		System.out.println(admin.cinemasToString());

		System.out.print("Enter the cinema number to be edited: ");
		cinemaIndex = in.nextInt() - 1;
	    }

	    else if (input.equals("rc")) {
		System.out.print("WARNING, schedule will be altered as well! Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y")) {
		    System.out.println(admin.cinemasToString());
		    System.out.print("Enter the cinema number to remove (will be removed from schedule as well): ");
		    User.errorHandling(user.removeCinema(in.nextInt()-1));
		}
	    }
	    
	    else if (input.equals("as")) {
		System.out.print("Movie title: ");
		var title = in.next();
		System.out.print("Cinema: ");
		cinemaIndex = in.nextInt()-1;
		System.out.print("Hall number: ");
		hallIndex = in.nextInt()-1;
		System.out.print("Duration (in minutes): ");
		var duration = in.nextLong();
		System.out.print("Screening year: ");
		var year = in.nextInt();
		System.out.print("Screening month: ");
		var month = in.nextInt();
		System.out.print("Screening day: ");
		var day = in.nextInt();
		System.out.print("Screening hour: ");
		var hour = in.nextInt();
		System.out.print("Screening minute: ");
		var minute = in.nextInt();

		Calendar date = Calendar.getInstance();
		date.set(year, month, day, hour, minute, 0);

		User.errorHandling(user.addScreening(date, cinemaIndex, title, duration, hallIndex));
	    }

	    else if (input.equals("es")) {
		System.out.println(user.scheduleToString());

		System.out.print("Enter screening number to edit: ");
		screeningIndex = in.nextInt()-1;
	    }

	    else if (input.equals("rs")) {
		System.out.println(user.scheduleToString());
		System.out.print("Enter screening number to remove: ");
		User.errorHandling(user.removeScreening(in.nextInt()-1));
	    }

	    else if (input.equals("nn")) {
		System.out.print("Enter the new name for cinema (schedule will also be updated): ");
		User.errorHandling(user.newCinemaName(cinemaIndex, in.next()));
	    }

	    else if (input.equals("ah")) {
		System.out.print("Enter the amount of rows in the new hall: ");
		int rows = in.nextInt();
		int[] seatsPerRow = new int[rows];
		
		for (int i = 0; i < rows; i++) {
		    System.out.print("Enter the amount of seats in row %d: ".formatted(i+1));
		    seatsPerRow[i] = in.nextInt();
		}

		User.errorHandling(user.addHall(cinemaIndex, seatsPerRow));
	    }

	    else if (input.equals("eh")) {
		System.out.println(user.cinemaHallScheme(cinemaIndex));

		System.out.print("Enter the hall number to be edited: ");
		hallIndex = in.nextInt() - 1;
	    }

	    else if (input.equals("rh")) {
		System.out.print("WARNING! Schedule will be also affected. Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y")) {
		    System.out.print("Enter the hall number to be removed: ");
		    User.errorHandling(user.removeHall(cinemaIndex, in.nextInt()-1));
		}
	    }

	    else if (input.equals("ar")) {
		System.out.print("Enter the amount of seats in the new row: ");
		User.errorHandling(user.addRowToHall(cinemaIndex, hallIndex, in.nextInt()));
	    }

	    else if (input.equals("rr")) {
		System.out.print("WARNING, schedule will be altered as well! Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y")) {
		    System.out.println(user.hallScheme(cinemaIndex, hallIndex));
		    System.out.println("Enter the row number to remove: ");
		    User.errorHandling(user.removeRowFromHall(cinemaIndex, hallIndex, in.nextInt()-1));
		}
	    }

	    else if (input.equals("rsd")) {
		System.out.print("WARNING, scheduled seats will be reset! Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y"))
		    User.errorHandling(user.resetSeatsData(cinemaIndex, hallIndex));
	    }

	    else if (input.equals("st")) {
		System.out.print("Year: ");
		var year = in.nextInt();
		System.out.print("Month: ");
		var month = in.nextInt();
		System.out.print("Day: ");
		var day = in.nextInt();
		System.out.print("Hour: ");
		var hour = in.nextInt();
		System.out.print("Minute: ");
		var minute = in.nextInt();

		Calendar date = Calendar.getInstance();
		date.set(year, month, day, hour, minute, 0);
		User.errorHandling(user.setScreeningDate(screeningIndex, date));
	    }

	    else if (input.equals("sch")) {
		System.out.print("WARNING, scheduled seats will be reset! Proceed (y/N)? ");
		input = in.next();

		if (input.equals("y") || input.equals("Y")) {
		    System.out.print("Enter the cinema number: ");
		    int cinemaIndexTemp = in.nextInt()-1;

		    System.out.print("Enter the hall number from this cinema: ");
		    User.errorHandling(user.setScreeningCinemaHall(screeningIndex, cinemaIndexTemp, in.nextInt()-1));
		}
	    }

	    else if (input.equals("sm")) {
		System.out.print("Enter the new movie title: ");
		User.errorHandling(user.setScreeningMovieTitle(screeningIndex, in.next()));
	    }

	    else if (input.equals("sd")) {
		System.out.print("Enter the new screening duration: ");
		User.errorHandling(user.setScreeningDuration(screeningIndex, in.nextLong()));
	    }

	    else if (input.equals("fas"))
		User.errorHandling(user.screeningFreeAllSeats(screeningIndex));

	    else
		System.out.println("Error, unknown command. Enter 'h' to list the commands");
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
