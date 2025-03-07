package cinema;
import java.util.ArrayList;
import java.util.HashMap;

public class Cinema {
    private String name;
    private ArrayList<Hall> halls = new ArrayList<Hall>();
    private HashMap<Day, ArrayList<Screening>> schedule = new HashMap<Day, ArrayList<Screening>>();

    public Cinema(String name) {
	this.name = name;

	for (Day day : Day.values()) {
	    ArrayList<Screening> newScreeniList = new ArrayList<Screening>();
	    schedule.put(day, newScreeniList);
	}
    }

    public String getName() {
	return name;
    }

    public ArrayList<Hall> getHalls() {
	return halls;
    }

    public HashMap<Day, ArrayList<Screening>> getSchedule() {
	return schedule;
    }
    
    public void setName(String name) {
	this.name = name;
    }

    public void setHalls(ArrayList<Hall> halls) {
	this.halls = halls;
    }

    public void setSchedule(HashMap<Day, ArrayList<Screening>> schedule) {
	this.schedule = schedule;
    }

    public Hall addHall() {
	Hall newHall = new Hall();
	halls.add(newHall);
	return newHall;
    }

    public void removeHall(int hallNumber) {
	halls.remove(hallNumber);
    }

    public Hall getHall(int hallNumber) {
	return halls.get(hallNumber);
    }

    public Screening addScreening(Day day, String movieName, int beginTime, int endTime, int hallNumber) {
	Screening newScreening = new Screening(movieName, beginTime, endTime, halls.get(hallNumber), hallNumber);
	var todayScreeneings = getScreenings(day);
	todayScreeneings.add(newScreening);
	return newScreening;
    }

    public ArrayList<Screening> getScreenings(Day day) {
	return schedule.get(day);
    }
    
    public void printSchedule() {
	for (var day : Day.values()) 
	    if (!schedule.get(day).isEmpty()) {
		System.out.println(day);

		for (var screening : schedule.get(day)) 
		    System.out.print(screening.toString());
	    }
    }
}
