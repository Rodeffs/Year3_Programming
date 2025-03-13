package cinema;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Scanner;

public class User {
    private String username = "";
    private String password = "";
    private ArrayList<Screening> schedule = new ArrayList<Screening>();
    private ArrayList<Cinema> cinemas = new ArrayList<Cinema>();
    private boolean logged = false;
    private boolean admin = false;

    public User() {}
 
    public User(String username, String password) {
	this.username = username;
	this.password = password;
    }

    public User(String username, String password, boolean isAdmin) {
	this.username = username;
	this.password = password;
	this.admin = isAdmin;
    }
  
    public boolean login(String username, String password) {
	logged = (this.username.equals(username) && this.password.equals(password));
	return logged;
    }

    public String getUsername() {
	return username;
    }

    public String getPassword() {
	return password;
    }

    public ArrayList<Cinema> getCinemaList() {
	return cinemas;
    }

    public ArrayList<Screening> getSchedule() {
	return schedule;
    }

    public boolean isLoggedIn() {
	return logged;
    }

    public boolean isAdmin() {
	return admin;
    }

    public void setCinemaList(ArrayList<Cinema> cinemas) {
	this.cinemas = cinemas;
    }

    public void setSchedule(ArrayList<Screening> schedule) {
	this.schedule = schedule;
    }

    public void setUsername(String username) {
	this.username = username;
    }

    public void setPassword(String password) {
	this.password = password;
    }

    public void logoff() {
	logged = false;
    }

    public void giveAdminRights(boolean isAdmin) {
	this.admin = isAdmin;
    }

    public int addCinema(String cinemaName) {
	if (!admin)
	    return -1;

	Cinema newCinema = new Cinema(cinemaName);
	cinemas.add(newCinema);
	return 0;
    }

    public int newCinemaName(int cinemaIndex, String newName) {
	if (!admin)
	    return -1;

	try {
	    cinemas.get(cinemaIndex).setName(newName);
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int removeCinema(int cinemaIndex) {
	if (!admin)
	    return -1;

	try {
	    var cinema = cinemas.get(cinemaIndex);

	    var toBeRemoved = findScreenings(cinema);

	    for (var screening : toBeRemoved)
		schedule.remove(screening);

	    cinemas.remove(cinemaIndex);
	}
	catch (Exception e) {
	    return -2;
	}
	
	return 0;
    }

    public int addHall(int cinemaIndex, int[] seatsPerRow) {
	if (!admin)
	    return -1;  // можно было заморочиться с enum Class, но для этой лабы достаточно просто int

	Hall hall = new Hall();

	for (var seatCount : seatsPerRow)
	    hall.addRow(seatCount);
	
	try {
	    cinemas.get(cinemaIndex).getHalls().add(hall);
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int removeHall(int cinemaIndex, int hallIndex) {
	if (!admin)
	    return -1;
	
	try {
	    var cinema = cinemas.get(cinemaIndex);
	    cinema.getHalls().remove(hallIndex);

	    var toBeChanged = findScreenings(cinema);

	    for (var screening : toBeChanged) {
		var oldIndex = screening.getHallNumber() - 1;

		if (oldIndex == (hallIndex))
		    schedule.remove(screening);

		else if (oldIndex > (hallIndex))
		    screening.setHallNumber(oldIndex);
	    }
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int addRowToHall(int cinemaIndex, int hallIndex, int seatCount) {
	if (!admin)
	    return -1;

	try {
	    var cinema = cinemas.get(cinemaIndex);
	    cinema.getHalls().get(hallIndex).addRow(seatCount);

	    var seatsToBeAdded = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeAdded)
		screening.getHall().addRow(seatCount);
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int removeRowFromHall(int cinemaIndex, int hallIndex, int rowIndex) {
	if (!admin)
	    return -1;

	try {
	    var cinema = cinemas.get(cinemaIndex);
	    cinema.getHalls().get(hallIndex).getSeats().remove(rowIndex);

	    var seatsToBeDeleted = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeDeleted)
		screening.getHall().getSeats().remove(rowIndex);
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int resetSeatsData(int cinemaIndex, int hallIndex) {
	if (!admin)
	    return -1;

	try {
	    var cinema = cinemas.get(cinemaIndex);
	    cinema.getHalls().get(hallIndex).resetSeatsData();

	    var seatsToBeReset = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeReset)
		screening.getHall().resetSeatsData();
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public String cinemaHallScheme(int cinemaIndex) {
	try {
	    return cinemas.get(cinemaIndex).toString();
	}
	catch (Exception e) {
	    return "Error, there isn't such a cinema";
	}
    }

    public String hallScheme(int cinemaIndex, int hallIndex) {
	try {
	    return cinemas.get(cinemaIndex).getHalls().get(hallIndex).toString();
	}
	catch (Exception e) {
	    return "Error, there isn't such a cinema or a hall";
	}
    }

    public String scheduleToString() {
	String output = "";

	for (int i = 0; i < schedule.size(); i++)
	    output += (i+1) + ".\n" + schedule.get(i).toString() + "\n";

	return output;
    }

    public String cinemasToString() {
	String output = "";

	for (int i = 0; i < cinemas.size(); i++)
	    output += (i+1) + ". " + cinemas.get(i).getName() + "\n";

	return output;
    }

    public Screening findClosestScreening(String movieName, Calendar date, int ticketCount) {
	Screening closest = null;
	long maximumWait = Long.MAX_VALUE;

	for (var screening : schedule) 
	    if (screening.getMovieName().equals(movieName) && screening.getDate().after(date) && (ticketCount <= screening.getHall().getFreeSeats())) {
		var beginTime = screening.getDate().getTimeInMillis();
		var curTime = date.getTimeInMillis();

		if (beginTime - curTime < maximumWait) {
		    maximumWait = beginTime - curTime;
		    closest = screening;
		}
	    }

	return closest;
    }

    public ArrayList<Screening> findScreenings(Object... params) {  // вернуть все сеансы с заданными параметрами
	ArrayList<Screening> query = new ArrayList<Screening>();

	Calendar date = null;
	Cinema cinema = null;
	String movieName = null;
	int hallNumber = -1;

	for (var param : params) {
	    if (param instanceof Calendar)
		date = (Calendar)param;
	    else if (param instanceof Cinema)
		cinema = (Cinema)param;
	    else if (param instanceof String)
		movieName = (String)param;
	    else if (param instanceof Integer)
		hallNumber = (Integer)param;
	}

	for (var screening : schedule) {
	    boolean toAdd = false;

	    if (date != null)
		toAdd = screening.getDate().equals(date);

	    if (cinema != null)
		toAdd = screening.getCinema().equals(cinema);

	    if (movieName != null)
		toAdd = screening.getMovieName().equals(movieName);

	    if (hallNumber > -1)
		toAdd = (screening.getHallNumber() == hallNumber);

	    if (toAdd)
		query.add(screening);
	}

	return query;
    }

    public int makeReservation(int screeningIndex, int ticketCount) {
	try {
	    var hall = schedule.get(screeningIndex).getHall();

	    if (ticketCount > hall.getFreeSeats())
		return -2;

	    buyingTickets(hall, ticketCount);
	}
	catch (Exception e) {
	    return -2;
	}

	return 0;
    }

    public int makeReservationForClosest(String movieName, Calendar date, int ticketCount) {
	var closest = findClosestScreening(movieName, date, ticketCount);

	if (closest == null)
	    return -2;

	buyingTickets(closest.getHall(), ticketCount);
	return 0;
    }

    private void buyingTickets(Hall hall, int ticketCount) {  // работать с выводом в консоль не лучшая идея вне Main, но пойдёт для этой лабы
	int i = 1;

	Scanner in = new Scanner(System.in);

	while (i <= ticketCount) {
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

}
