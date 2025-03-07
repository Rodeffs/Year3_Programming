package cinema;

public class Screening {
    String movieName;
    int beginTime;
    int endTime;
    Hall hall;
    int hallNumber;

    public Screening(String movieName, int beginTime, int endTime, Hall hall, int hallNumber) {
	this.movieName = movieName;
	this.beginTime = beginTime;
	this.endTime = endTime;
	this.hall = new Hall(hall);
	this.hallNumber = hallNumber;
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

    public Hall getHall() {
	return hall;
    }

    public int getHallNumber() {
	return hallNumber;
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

    public void setHall(Hall hall) {
	this.hall = new Hall(hall);
    }
    
    @Override
    public String toString() {
	String output = "";

	output += "Название: " + getMovieName() + "\n";
	output += "Время начала: " + getBeginTime() + "\n";
	output += "Время конца: " + getEndTime() + "\n";
	output += "Номер зала: " + getHallNumber() + "\n";

	return output;
    }
}
