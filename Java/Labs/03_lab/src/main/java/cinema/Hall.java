package cinema;
import java.util.ArrayList;

public class Hall {
    private int maxSeatsInRow = 0; // костыль для красивого вывода
    private ArrayList<ArrayList<Seat>> seats = new ArrayList<ArrayList<Seat>>();
    
    public Hall() {}

    public Hall(ArrayList<ArrayList<Seat>> seats) {
	this.setSeats(seats);
    }

    public Hall(Hall otherHall) {  // конструктор копирования
	this.setSeats(otherHall.getSeats());
    }

    public ArrayList<ArrayList<Seat>> getSeats() {
	return seats;
    }

    public void setSeats(ArrayList<ArrayList<Seat>> seats) {
	this.resetSeatsData();

	for (var row : seats) {
	    ArrayList<Seat> newRow = new ArrayList<>();

	    int seatCount = row.size();

	    if (seatCount > maxSeatsInRow)
		maxSeatsInRow = seatCount;

	    for (var seat : row) {
		Seat newSeat = new Seat(seat);
		newRow.add(newSeat);
	    }

	    this.seats.add(newRow);
	}
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
	
	for (int i = 0; i < seats.size(); i++) {
	    var row = seats.get(i);  // var is like auto from C

	    int nonexistantSeats = maxSeatsInRow - row.size();

	    for (int j = 0; j < nonexistantSeats/2; j++)
		output += "  ";

	    for (var seat : row) 
		output += seat.isOccupied() ? "■ " : "□ ";

	    for (int j = 0; j < nonexistantSeats - nonexistantSeats/2; j++)
		output += "  ";

	    output += "\n";
	}

	return output;
    }
}
