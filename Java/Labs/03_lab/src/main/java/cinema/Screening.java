package cinema;
import java.util.Calendar;

public class Screening {
    private Calendar date;
    private Cinema cinema;
    private String movieName;
    private long duration;
    private int hallNumber;
    private Hall hall;

    public Screening(Calendar date, Cinema cinema, String movieName, long duration, int hallNumber) {
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

    public long getDuration() {
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

    public void setCinema(Cinema cinema) {
	this.cinema = cinema;
    }

    public void setMovieName(String movieName) {
	this.movieName = movieName;
    }

    public void setDuration(long duration) {
	this.duration = duration;
    }

    public void setHallNumber(int hallNumber) {
	this.hallNumber = hallNumber;
    }

    public void setHall(Hall hall) {
	this.hall = new Hall(hall);
    }

    @Override
    public String toString() {
	return "Date: %s\nCinema: %s\nTitle: %s\nDuration (min): %d\nHall number: %d\nFree seats: %d\nHall scheme:\n%s".formatted(date.getTime(), cinema.getName(), movieName, duration, 1 + hallNumber, hall.getFreeSeats(), hall.toString());
    }
}
