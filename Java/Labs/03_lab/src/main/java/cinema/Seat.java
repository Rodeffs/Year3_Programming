package cinema;

public class Seat {
    private boolean occupied = false;

    public Seat() {}

    public Seat(boolean occupied) {
	this.occupied = occupied;
    }

    public Seat(Seat otherSeat) {
	this.occupied = otherSeat.isOccupied();
    }

    public boolean isOccupied() {
	return occupied;
    }

    public void occupy() {
	this.occupied = true;
    }

    public void deoccupy() {
	this.occupied = false;
    }

}
