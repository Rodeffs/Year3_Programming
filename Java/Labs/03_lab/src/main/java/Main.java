import java.util.ArrayList;

import cinema.*;
import login.*;

public class Main {

    public static void main(String[] args) {

	// Некоторые исходные данные
	
	Cinema cinema1 = new Cinema("Родина");
	Cinema cinema2 = new Cinema("Каро");
	Cinema cinema3 = new Cinema("Кинопарк");

	var hall1_1 = cinema1.addHall();
	var hall1_2 = cinema1.addHall();

	var hall2_1 = cinema2.addHall();
	var hall2_2 = cinema2.addHall();
	var hall2_3 = cinema2.addHall();

	var hall3_1 = cinema3.addHall();

	hall1_1.addRow(6);
	hall1_1.addRow(8);
	hall1_1.addRow(10);
	hall1_1.addRow(12);

	hall1_2.addRow(5);
	hall1_2.addRow(5);
	hall1_2.addRow(8);
	hall1_2.addRow(8);

	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	hall2_1.addRow(10);
	
	hall2_2.addRow(5);
	hall2_2.addRow(6);
	hall2_2.addRow(7);
	hall2_2.addRow(8);
	hall2_2.addRow(9);

	hall2_3.addRow(20);
	hall2_3.addRow(18);
	hall2_3.addRow(15);
	hall2_3.addRow(10);

	hall3_1.addRow(25);

	ArrayList<Cinema> cinemas = new ArrayList<Cinema>();

	cinemas.add(cinema1);
	cinemas.add(cinema2);
	cinemas.add(cinema3);

	hall1_1.occupySeat(0, 0);
	
	ArrayList<Screening> schedule = new ArrayList<Screening>();

	schedule.add(new Screening(Day.SATURDAY, cinema1, "Balatro", 0, 120, 0));
	schedule.add(new Screening(Day.SATURDAY, cinema1, "Terraria", 125, 185, 0));
	schedule.add(new Screening(Day.SATURDAY, cinema1, "Minecraft", 100, 160, 1));


    }
}
