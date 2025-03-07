package cinema;
import java.util.ArrayList;

class Cinema {
    private String name;
    private ArrayList<Hall> halls = new ArrayList<Hall>();

    public Cinema(String name) {
	this.name = name;
    }

    public String getName() {
	return name;
    }

    public ArrayList<Hall> getHalls() {
	return halls;
    }

    public void setName(String name) {
	this.name = name;
    }

    public void setHalls(ArrayList<Hall> halls) {
	this.halls = halls;
    }

    public void addHall(int hallNumber) {
	Hall newHall = new Hall(hallNumber);
	halls.add(newHall);
    }

    public Hall getHall(int hallNumber) {
	for (Hall hall : halls) 
	    if (hall.getNumber() == hallNumber)
		return hall;
	
	return null;
    }
}
