package uk.org.jamesbuckley.gerber;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class NCDrillFileStats {
	public int num_holes;
	public double smallest_hole;
	public double largest_hole;
	
	private static final Pattern drill_pattern = Pattern.compile("^([XY]([0-9]{5,7}))([Y]([0-9]{5,7}))?D([0-9]*)\\*");
	
	public static NCDrillFileStats parseStream(InputStream s) throws IOException {
		NCDrillFileStats nc = new NCDrillFileStats();
		
		BufferedReader in = new BufferedReader(new InputStreamReader(s));
		
		nc.num_holes = 0;
		nc.largest_hole = 0;
		nc.smallest_hole = Double.MAX_VALUE;
		
		// Read lines from the stream and count the number of holes drilled
		while(true) {
			String line = in.readLine();
			
			// Check we haven't reached the end of the file
			if(line == null) {
				break;
			}
			
			Matcher m = drill_pattern.matcher(line);
			if(m.matches()) {
				nc.num_holes++;
			}
			
			
		}
		
		return nc;
	}
}
