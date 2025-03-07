package cinema;

class Seat {
    boolean occupied = false;

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
