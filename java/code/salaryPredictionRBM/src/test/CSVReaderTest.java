package test;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import com.google.gson.Gson;

import moneyMaker.Job;

import csvReader.CSVReader;

public class CSVReaderTest {

	private static final String FULL_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1.csv";
	private static final String SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_sample.csv";
	private static final String SMALL_SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_small_sample.csv";
	private static final String TINY_SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_tiny_sample.csv";
	private static final String TEST_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1.csv";
	
	public static void main(String[] args) throws IOException{
		CSVReader reader = new CSVReader(new FileReader(SAMPLE_DATA));
		String[] nextLine;
		while ((nextLine = reader.readNext()) != null){
			Job job = new Job(nextLine);
			Gson gson = new Gson();
			String json = gson.toJson(job);
			System.out.println(json);
		}
	}
}
