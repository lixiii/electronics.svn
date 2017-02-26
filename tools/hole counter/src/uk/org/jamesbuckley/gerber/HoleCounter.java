package uk.org.jamesbuckley.gerber;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Iterator;

import com.beust.jcommander.JCommander;

public class HoleCounter {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		CommandLineArgs a = new CommandLineArgs();
		new JCommander(a, args);
		
		System.out.println("hole counts");
		for(String file : a.files) {
			NCDrillFileStats stats;
			try {
				stats = NCDrillFileStats.parseStream(new FileInputStream(file));
				System.out.printf("%s: %d\n", file, stats.num_holes);
			} catch (FileNotFoundException e) {
				System.out.printf("%s: file not found\n", file);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				System.out.printf("%s: error reading file\n", file);
			}
		}

	}

}
