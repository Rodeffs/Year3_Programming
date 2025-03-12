package login;
import java.util.ArrayList;
import java.util.Calendar;

import cinema.*;

abstract class Account {
    protected String username;
    protected String password;
    protected boolean logged = false;

    public Account(String username, String password) {
	this.username = username;
	this.password = password;
    }

    public boolean login(String username, String password) {
	logged = (this.username.equals(username) && this.password.equals(password));
	return logged;
    }

    public boolean isLoggedIn() {
	return logged;
    }

    public void logoff() {
	logged = false;
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

    public static Screening findClosestScreening(ArrayList<Screening> schedule, String movieName, Calendar date, int ticketCount) {
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

    public static ArrayList<Screening> findScreenings(ArrayList<Screening> schedule, Object... params) {  // вернуть все сеансы с заданными параметрами
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

    public static String scheduleToString(ArrayList<Screening> schedule) {
	String output = "";

	for (int i = 0; i < schedule.size(); i++)
	    output += (i+1) + ".\n" + schedule.get(i).toString() + "\n";

	return output;
    }
}
