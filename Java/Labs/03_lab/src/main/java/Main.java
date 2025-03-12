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
		    System.out.println("Commands:\n'h' or 'help' - print this message\n's' or 'schedule' - print the full screenings schedule\n'c' or 'closest' - reserve for the closest screening\n'r' or 'reserve' - make a reservation by manually selecting a screening\n'ac' - add cinema\n'ec' - edit cinema\n'rc' - remove cinema\n'pc' - print the list of cinemas\n'as' - add screening to schedule\n'es' - edit schedule\n'rs' - remove screening from schedule");

		else
		    System.out.println("Commands:\n'h' or 'help' - print this message\n's' or 'schedule' - print the full screenings schedule\n'c' or 'closest' - reserve for the closest screening\n'r' or 'reserve' - make a reservation by manually selecting a screening");
	    }

	    else if (input.equals("pc") && admin.isLoggedIn()) 
		System.out.println(admin.cinemasToString());

	    else if (input.equals("ac") && admin.isLoggedIn()) {
		System.out.print("Enter the name of the new cinema: ");
		var name = in.next();

		Cinema newCinema = new Cinema(name);
		cinemas.add(newCinema);
	    }

	    else if (input.equals("ec") && admin.isLoggedIn()) {
		System.out.println(admin.cinemasToString());

		System.out.print("Enter the cinema number to be edited");
		var num = in.nextInt();

		if ((num < 1) || (num > cinemas.size()))
		    System.out.println("Error, there isn't such a cinema");

		else {
		    var editcin = cinemas.get(num-1);

		    System.out.println("EDITING MODE - CINEMA\nEnter 'h' or 'help' to list commands");

		    while (true) {
			input = in.next();

			if (input.equals("h") || input.equals("help"))
			    System.out.println("Options:\n'nn' - new name for cinema\n'ah' - add hall\n'eh - edit hall\n'rh' - remove hall\n'ph' - print halls\n'h' or 'help' - print this message\n'q' or 'quit' - quit EDITING MODE - CINEMA");

			else if (input.equals("nn")) {
			    System.out.print("Enter the new name for cinema (schedule will also be updated): ");
			    editcin.setName(in.next());
			}

			else if (input.equals("ah")) {
			    System.out.print("Enter the amount of rows in the new hall: ");
			    var rows = in.nextInt();

			    Hall hall = new Hall();
			    int i = 1;

			    while (i <= rows) {
				System.out.print("Enter the amount of seats in row %d: ".formatted(i+1));

				var seatCount = in.nextInt();

				if (seatCount < 0)
				    System.out.println("Error, negative amount");
				else {
				    hall.addRow(seatCount);
				    i++;
				}
			    }

			    editcin.getHalls().add(hall);
			}

			else if (input.equals("rh")) {
			    System.out.print("WARNING! Schedule will be also affected. Proceed (y/N)? ");

			    input = in.next();

			    if (input.equals("y") || input.equals("Y")) {
				System.out.print("Enter the hall number to be removed: ");
				var hallnum = in.nextInt();

				if ((hallnum < 1) || (hallnum > editcin.getHalls().size()))
				    System.out.println("Error, there isn't such a hall");

				else {
				    editcin.getHalls().remove(hallnum-1);

				    var toBeChanged = User.findScreenings(schedule, editcin);

				    for (var screening : toBeChanged) {
					var oldnum = screening.getHallNumber();

					if (oldnum == (hallnum-1))
					    schedule.remove(screening);

					else if (oldnum > (hallnum-1))
					    screening.setHallNumber(oldnum-1);
				    }
				}
			    }
			}

			else if (input.equals("ph"))
			    System.out.println(editcin.toString());

			else if (input.equals("eh")) {
			    System.out.println(editcin.toString());

			    System.out.print("Enter the hall number to be edited: ");
			    var hallnum = in.nextInt();

			    if ((hallnum < 1) || (hallnum > editcin.getHalls().size()))
				System.out.println("Error, there isn't such a hall");

			    else {
				var edithall = editcin.getHalls().get(hallnum-1);

				System.out.println("EDITING MODE - HALL\nEnter 'h' or 'help' to list commands");

				while (true) {    
				    input = in.next();

				    if (input.equals("h") || input.equals("help"))
					System.out.println("Options:\n'ar' - add row\n'rr' - remove row\n'pr' - print hall scheme\n'rsd' - reset seat data\n'h' or 'help' - print this message\n'q' or 'quit' - quit EDITING MODE - HALL");

				    else if (input.equals("ar")) {
					System.out.print("Enter the amount of seats in the new row: ");

					var seatCount = in.nextInt();

					if (seatCount < 0)
					    System.out.println("Error, negative amount");

					else {
					    edithall.addRow(seatCount);

					    var seatsToBeAdded = User.findScreenings(schedule, editcin, hallnum-1);

					    for (var screening : seatsToBeAdded)
						screening.getHall().addRow(seatCount);
					}
				    }

				    else if (input.equals("rr")) {
					System.out.println("WARNING, scheduled seats will be reset! Proceed (y/N)? ");

					input = in.next();

					if (input.equals("y") || input.equals("Y")) {
					    System.out.println(edithall.toString());
					    System.out.println("Enter the row number to remove: ");
					    var rownum = in.nextInt();

					    try {
						edithall.getSeats().remove(rownum);

						var seatsToBeReset = User.findScreenings(schedule, editcin, hallnum-1);

						for (var screening : seatsToBeReset)
						    screening.setHall(edithall);
					    }
					    catch (Exception e) {
						System.out.println("Error, there isn't such a row");
					    }
					}
				    }

				    else if (input.equals("pr"))
					System.out.println(edithall.toString());

				    else if (input.equals("rsd")) {
					System.out.println("WARNING, scheduled seats will be reset! Proceed (y/N)? ");

					input = in.next();

					if (input.equals("y") || input.equals("Y")) {
					    edithall.resetSeatsData();

					    var seatsToBeReset = User.findScreenings(schedule, editcin, hallnum-1);

					    for (var screening : seatsToBeReset)
						screening.getHall().resetSeatsData();
					}
				    }

				    else if (input.equals("q") || input.equals("quit")) {
					System.out.println("QUITTING EDITING MODE - HALL");
					break;
				    }

				    else
					System.out.println("Error, unknown command. Enter 'h' to list the commands");
				}
			    }
			}

			else if (input.equals("as") && admin.isLoggedIn()) {

			}

			else if (input.equals("q") || input.equals("quit")) {
			    System.out.println("QUITTING EDITING MODE - CINEMA");
			    break;
			}

			else
			    System.out.println("Error, unknown command. Enter 'h' to list the commands");
		    }
		}
	    }

	    else if (input.equals("rc") && admin.isLoggedIn()) {
		System.out.println(admin.cinemasToString());

		System.out.print("Enter the cinema number to remove (will be removed from schedule as well): ");
		var num = in.nextInt();

		if ((num < 1) || (num > cinemas.size()))
		    System.out.println("Error, there isn't such a cinema");

		else {
		    var toBeRemoved = User.findScreenings(schedule, cinemas.get(num-1));

		    for (var screening : toBeRemoved)
			schedule.remove(screening);

		    cinemas.remove(num-1);
		}
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

		    if (!input.equals("n") && !input.equals("N"))
			buyingTickets(closest.getHall(), tickets);
		    System.out.println("Reservation made!");
		}

		else
		    System.out.println("Error, no matching screenings were found");
	    }

	    else if (input.equals("r") || input.equals("reserve")) {
		System.out.println(User.scheduleToString(schedule));

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
			if (!input.equals("n") && !input.equals("N"))
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
