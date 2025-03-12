package login;

import java.util.ArrayList;
import cinema.*;

public class Admin extends Account {
    private ArrayList<Screening> schedule = new ArrayList<Screening>();
    private ArrayList<Cinema> cinemas = new ArrayList<Cinema>();

    public Admin(String username, String password) {
	super(username, password);
    }
    
    public ArrayList<Cinema> getCinemaList() {
	return cinemas;
    }

    public ArrayList<Screening> getSchedule() {
	return schedule;
    }

    public void setCinemaList(ArrayList<Cinema> cinemas) {
	this.cinemas = cinemas;
    }

    public void setSchedule(ArrayList<Screening> schedule) {
	this.schedule = schedule;
    }

    public String cinemasToString() {
	String output = "";

	for (int i = 0; i < cinemas.size(); i++)
	    output += (i+1) + ". " + cinemas.get(i).getName() + "\n";

	return output;
    }
}
