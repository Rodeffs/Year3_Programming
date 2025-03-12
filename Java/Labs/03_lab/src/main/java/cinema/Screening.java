package cinema;
import java.util.Calendar;

public class Screening {
    private Calendar date;
    private Cinema cinema;
    private String movieName;
    private int duration;
    private int hallNumber;
    private Hall hall;

    public Screening(Calendar date, Cinema cinema, String movieName, int duration, int hallNumber) {
	this.date = date;
	this.cinema = cinema;
	this.movieName = movieName;
	this.duration = duration;
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHalls().get(hallNumber));  // чтобы не портить исходный план здания
    }

    public Calendar getDate() {
	return date;
    }

    public Cinema getCinema() {
	return cinema;
    }

    public String getMovieName() {
	return movieName;
    }

    public int getDuration() {
	return duration;
    }

    public int getHallNumber() {
	return hallNumber;
    }

    public Hall getHall() {
	return hall;
    }

    public void setDate(Calendar date) {
	this.date = date;
    }

    public void setCinema(Cinema cinema, int hallNumber) {
	this.cinema = cinema;
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHalls().get(hallNumber));
    }

    public void setMovieName(String movieName) {
	this.movieName = movieName;
    }

    public void setDuration(int duration) {
	this.duration = duration;
    }

    public void setHallNumber(int hallNumber) {
	this.hallNumber = hallNumber;
	this.hall = new Hall(cinema.getHalls().get(hallNumber));
    }

    @Override
    public String toString() {
	String output = "";
	
	output += "Дата: " + getDate().getTime() + "\n";
	output += "Кинотеатр: " + getCinema().getName() + "\n";
	output += "Название фильма: " + getMovieName() + "\n";
	output += "Длительность (мин): " + getDuration() + "\n";
	output += "Номер зала: " + (1+getHallNumber()) + "\n";
	output += "Кол-во свободных мест: " + hall.getFreeSeats() + "\n";
	output += "План зала: " + "\n" + hall.toString() + "\n";

	return output;
    }
}
