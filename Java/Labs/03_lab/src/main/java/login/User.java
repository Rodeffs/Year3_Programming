package login;
import java.util.ArrayList;

import cinema.*;

abstract class User {
    abstract public boolean login(String username, String password);
    abstract public boolean makeReservation(Day day, Cinema cinema, String movieName, int beginTime, int endTime, int hallNumber);
    abstract 
    abstract public String closestScreening();
    abstract public ArrayList<Screening> getSchedule();
    abstract public void setSchedule(ArrayList<Screening> schedule);
}
