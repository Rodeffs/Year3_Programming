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

    public void removeCinema(Cinema cinema) {
	cinemas.remove(cinema);
	removeScreenings(cinema);
    }

    public void removeScreenings(Object... params) {
	var toBeRemoved = findScreenings(schedule, params);

	for (var screening : toBeRemoved)
	    schedule.remove(screening);

	toBeRemoved.clear();
    }
}
