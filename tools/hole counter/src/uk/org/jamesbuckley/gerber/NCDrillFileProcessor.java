package uk.org.jamesbuckley.gerber;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class NCDrillFileProcessor {
	static final String file = "/users/courses/jeb90/mcb_v2.0.0_out/mcb2.txt";

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			NCDrillFileStats s = NCDrillFileStats.parseStream(new FileInputStream(file));
			
			System.out.printf("Num holes: %d\n", s.num_holes);
			System.out.printf("Min hole size: %f\n", s.smallest_hole);
			System.out.printf("Max hole size: %f\n", s.largest_hole);
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
