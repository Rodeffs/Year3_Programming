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

    public String scheduleToString() {
	String output = "";

	for (int i = 0; i < schedule.size(); i++)
	    output += "Screening %d\n%s\n".formatted(i+1, schedule.get(i).toString());

	return output;
    }

    public String cinemasToString() {
	String output = "";

	for (int i = 0; i < cinemas.size(); i++)
	    output += "Cinema %d - %s\n".formatted(i+1, cinemas.get(i).getName());

	return output;
    }

    public String cinemaHallScheme(int cinemaIndex) {
	try {
	    return cinemas.get(cinemaIndex).toString();
	}
	catch (Exception e) {
	    return "Error, there is not such a cinema";
	}
    }

    public String hallScheme(int cinemaIndex, int hallIndex) {
	Cinema cinema = null;
	
	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return "Error, there is not such a cinema";
	}

	try {
	    return cinema.getHalls().get(hallIndex).toString();
	}
	catch (Exception e) {
	    return "Error, there is not such a hall in this cinema";
	}
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

    public ReturnCode makeReservationForClosest(String movieName, Calendar date, int ticketCount) {
	var closest = findClosestScreening(movieName, date, ticketCount);

	if (closest == null)
	    return ReturnCode.NO_CLOSEST_SCREENINGS;

	buyingTickets(closest.getHall(), ticketCount);
	return ReturnCode.OK;
    }

    public ReturnCode makeReservation(int screeningIndex, int ticketCount) {
	try {
	    var hall = schedule.get(screeningIndex).getHall();

	    if (ticketCount > hall.getFreeSeats())
		return ReturnCode.NOT_ENOUGH_FREE_SEATS;

	    buyingTickets(hall, ticketCount);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}

	return ReturnCode.OK;
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

    public ReturnCode addCinema(String cinemaName) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Cinema newCinema = new Cinema(cinemaName);
	cinemas.add(newCinema);
	return ReturnCode.OK;
    }

    public ReturnCode removeCinema(int cinemaIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    var cinema = cinemas.get(cinemaIndex);

	    var toBeRemoved = findScreenings(cinema);

	    for (var screening : toBeRemoved)
		schedule.remove(screening);

	    cinemas.remove(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}
	
	return ReturnCode.OK;
    }

    public ReturnCode newCinemaName(int cinemaIndex, String newName) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    cinemas.get(cinemaIndex).setName(newName);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode addHall(int cinemaIndex, int[] seatsPerRow) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;  // можно было заморочиться с enum Class, но для этой лабы достаточно просто int

	Hall hall = new Hall();

	for (var seatCount : seatsPerRow)
	    hall.addRow(seatCount);

	try {
	    cinemas.get(cinemaIndex).getHalls().add(hall);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode removeHall(int cinemaIndex, int hallIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;
	
	Cinema cinema = null;

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	try{
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
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode addRowToHall(int cinemaIndex, int hallIndex, int seatCount) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Cinema cinema = null;

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}
	
	try {
	    cinema.getHalls().get(hallIndex).addRow(seatCount);

	    var seatsToBeAdded = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeAdded)
		screening.getHall().addRow(seatCount);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode removeRowFromHall(int cinemaIndex, int hallIndex, int rowIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Cinema cinema = null;
	Hall hall = null;

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	try {
	    hall = cinema.getHalls().get(hallIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	try{
	    hall.getSeats().remove(rowIndex);

	    var seatsToBeDeleted = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeDeleted)
		screening.getHall().getSeats().remove(rowIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_ROW_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode resetSeatsData(int cinemaIndex, int hallIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Cinema cinema = null;

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	try {
	    cinema.getHalls().get(hallIndex).resetSeatsData();

	    var seatsToBeReset = findScreenings(cinema, hallIndex);

	    for (var screening : seatsToBeReset)
		screening.getHall().resetSeatsData();
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode addScreening(Calendar date, int cinemaIndex, String title, long duration, int hallIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Cinema cinema = null;

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}

	try {
	    cinema.getHalls().get(hallIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	Screening newScreening = new Screening(date, cinema, title, duration, hallIndex);
	var begin = date.getTimeInMillis();
	var end = begin + duration*60000;  // duration = x min = x*60*1000 ms

	var otherScreenings = findScreenings(cinemas.get(cinemaIndex), hallIndex);

	for (var other : otherScreenings) {
	    var otherBegin = other.getDate().getTimeInMillis();
	    var otherEnd = otherBegin + other.getDuration()*60000;

	    if (((otherBegin <= begin) && (begin <= otherEnd)) || /* начинается во время другого */
		((otherBegin <= end) && (end <= otherEnd)) ||  /* заканичвается во время другого */
		((begin <= otherBegin) && (otherBegin <= end)))  /* другой начинается во время него */
	    
		return ReturnCode.SCREENING_OVERLAP;  // тогда получается сеансы пересекаются во времени, а значит не добавляем новый сеанс
	}

	schedule.add(newScreening);
	return ReturnCode.OK;
    }

    public ReturnCode removeScreening(int screeningIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    schedule.remove(screeningIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}
	
	return ReturnCode.OK;
    }

    public ReturnCode setScreeningDate(int screeningIndex, Calendar date) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    schedule.get(screeningIndex).setDate(date);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode setScreeningCinemaHall(int screeningIndex, int cinemaIndex, int hallIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	Screening screening = null;
	Cinema cinema = null;

	try {
	    screening = schedule.get(screeningIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}

	try {
	    cinema = cinemas.get(cinemaIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_CINEMA_INDEX;
	}
	
	try {
	    Hall hall = cinema.getHalls().get(hallIndex);

	    screening.setCinema(cinema);
	    screening.setHall(hall);
	    screening.setHallNumber(hallIndex);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_HALL_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode setScreeningMovieTitle(int screeningIndex, String title) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    schedule.get(screeningIndex).setMovieName(title);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}
	
	return ReturnCode.OK;
    }

    public ReturnCode setScreeningDuration(int screeningIndex, long duration) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;
	
	try {
	    schedule.get(screeningIndex).setDuration(duration);
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}

	return ReturnCode.OK;
    }

    public ReturnCode screeningFreeAllSeats(int screeningIndex) {
	if (!admin)
	    return ReturnCode.NO_ACCESS;

	try {
	    schedule.get(screeningIndex).getHall().freeAllSeats();
	}
	catch (Exception e) {
	    return ReturnCode.INCORRECT_SCREENING_INDEX;
	}

	return ReturnCode.OK;
    }

    public static void errorHandling(ReturnCode commandOutput) {
	switch (commandOutput) {
	    case NO_ACCESS:
		System.out.println("Error, you do not have access to this command");
		break;

	    case INCORRECT_CINEMA_INDEX:
		System.out.println("Error, there is not such a cinema");
		break;

	    case INCORRECT_HALL_INDEX:
		System.out.println("Error, there is not such a hall in this cinema");
		break;

	    case INCORRECT_ROW_INDEX:
		System.out.println("Error, there is not such a row in this cinema hall");
		break;

	    case INCORRECT_SCREENING_INDEX:
		System.out.println("Error, there is not such a screening in the schedule");
		break;

	    case NOT_ENOUGH_FREE_SEATS:
		System.out.println("Error, there are not enough free seats in this hall");
		break;

	    case NO_CLOSEST_SCREENINGS:
		System.out.println("Error, no screening matches the input parameters");
		break;

	    case SCREENING_OVERLAP:
		System.out.println("Error, this time slot is already occupied");
		break;

	    case OK:
		break;
	}
    }
}
