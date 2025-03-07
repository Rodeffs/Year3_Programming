package cinema;

public class Screening {
    Day day;
    Cinema cinema;
    String movieName;
    int beginTime;  // время = число в минутах от 00:00
    int endTime;
    int hallNumber;
    Hall hall;

    public Screening(Day day, Cinema cinema, String movieName, int beginTime, int endTime, int hallNumber) {
	this.day = day;
	this.cinema = cinema;
	this.movieName = movieName;
	this.beginTime = beginTime;
	this.endTime = endTime;
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHall(hallNumber));
    }

    public Day getDay() {
	return day;
    }

    public Cinema getCinema() {
	return cinema;
    }

    public String getMovieName() {
	return movieName;
    }

    public int getBeginTime() {
	return beginTime;
    }

    public int getEndTime() {
	return endTime;
    }

    public int getHallNumber() {
	return hallNumber;
    }

    public Hall getHall() {
	return hall;
    }

    public void setDay(Day day) {
	this.day = day;
    }

    public void setCinema(Cinema cinema, int hallNumber) {
	this.cinema = cinema;
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHall(hallNumber));
    }

    public void setMovieName(String movieName) {
	this.movieName = movieName;
    }

    public void setBeginTime(int beginTime) {
	this.beginTime = beginTime;
    }

    public void setEndTime(int endTime) {
	this.endTime = endTime;
    }

    public void setHallNumber(int hallNumber) {
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHall(hallNumber));
    }

    @Override
    public String toString() {
	String output = "";
	
	output += "День: " + getDay() + "\n";
	output += "Кинотеатр: " + getCinema().getName() + "\n";
	output += "Название фильма: " + getMovieName() + "\n";
	output += "Время начала: " + getBeginTime() + "\n";
	output += "Время конца: " + getEndTime() + "\n";
	output += "Номер зала: " + getHallNumber() + "\n";
	output += "План зала: " + hall.toString() + "\n";

	return output;
    }
}
