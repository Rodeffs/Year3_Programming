package cinema;
import java.util.ArrayList;

class Hall {
    private int number;
    private int maxSeatsInRow = 0; // костыль для красивого вывода
    private ArrayList<ArrayList<Seat>> seats = new ArrayList<ArrayList<Seat>>();

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

	if (seatCount > maxSeatsInRow)
	    maxSeatsInRow = seatCount;

	for (int i = 0; i < seatCount; i++) {
	    Seat newSeat = new Seat();
	    newRow.add(newSeat);
	}

	seats.add(newRow);
    }

    public boolean isSeatOccupied(int row, int number) {
	return seats.get(row).get(number).isOccupied();
    }

    public void occupySeat(int row, int number) {
	seats.get(row).get(number).occupy();
    }

    public void deoccupySeat(int row, int number) {
	seats.get(row).get(number).deoccupy();
    }

    public void freeAllSeats() {
	for (int i = 0; i < seats.size(); i++) 
	    for (Seat seat : seats.get(i)) 
		seat.deoccupy();	
    }

    public void resetSeatsData() {
	seats.clear();
	maxSeatsInRow = 0;
    }
    
    @Override
    public String toString() {
	String output = "";
	
	// Место занято - ■
	// Место свободно - □

	return output;
    }
}
