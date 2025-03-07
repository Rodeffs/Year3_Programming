package cinema;
import java.util.ArrayList;
import cinema.Seat;

class Hall {
    int number;
    ArrayList<ArrayList<Seat>> seats = new ArrayList<ArrayList<Seat>>();

    public Hall(int number) {
	this.number = number;
    }

    public Hall(int number, ArrayList<ArrayList<Seat>> seats) {
	this.number = number;
	this.seats = seats;
    }

    public int getNumber() {
	return number;
    }

    public ArrayList<ArrayList<Seat>> getSeats() {
	return seats;
    }

    public void setNumber(int number) {
	this.number = number;
    }

    public void setSeats(ArrayList<ArrayList<Seat>> seats) {
	this.seats = seats;
    }

    public void addRow(int seatCount) {
	ArrayList<Seat> newRow = new ArrayList<>();

	for (int i = 1; i <= seatCount; i++) {
	    Seat newSeat = new Seat();
	    newRow.add(newSeat);
	}

	seats.add(newRow);
    }

    public void freeAllSeats() {
	for (int i = 0; i < seats.size(); i++) 
	    for (Seat seat : seats.get(i)) 
		seat.deoccupy();	
    }

    public void resetSeatsData() {
	seats.clear();
    }
}
