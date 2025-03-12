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

    @Override
    public String toString() {
	String output = "";

	for (int i = 0; i < halls.size(); i++)
	    output += "Hall " + (i+1) + "\n" + halls.get(i).toString() + "\n";

	return output;
    }
}
