package login;
import java.util.ArrayList;
import java.util.Calendar;

import cinema.*;

abstract class Account {
    protected String username;
    protected String password;

    public Account(String username, String password) {
	this.username = username;
	this.password = password;
    }

    public boolean login(String username, String password) {
	return (this.username.equals(username) && this.password.equals(password));
    }

    public String getUsername() {
	return username;
    }

    public String getPassword() {
	return password;
    }

    public void setUsername(String username) {
	this.username = username;
    }

    public void setPassword(String password) {
	this.password = password;
    }

    public Screening findClosestScreening(ArrayList<Screening> schedule, String movieName, Calendar date, int ticketCount) {
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

    public ArrayList<Screening> findScreenings(ArrayList<Screening> schedule, Object... params) {  // вернуть все сеансы с заданными параметрами
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

    public void makeReservationForSeat(Screening screening, int row, int seatNumber) {
	screening.getHall().occupySeat(row, seatNumber);
    }

    public static String scheduleToString(ArrayList<Screening> schedule) {
	String output = "";

	for (var screening : schedule)
	    output += screening.toString() + "\n";

	return output;
    }
}
