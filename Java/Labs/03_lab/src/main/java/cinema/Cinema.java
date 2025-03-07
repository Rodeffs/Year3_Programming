package cinema;
import java.util.ArrayList;

public class Cinema {
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
}
