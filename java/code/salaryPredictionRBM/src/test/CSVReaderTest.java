package test;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import com.google.gson.Gson;

import moneyMaker.Job;

import csvReader.CSVReader;

public class CSVReaderTest {

	private static final String FULL_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1.csv";
	private static final String SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_sample.csv";
	private static final String SMALL_SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_small_sample.csv";
	private static final String TINY_SAMPLE_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Train_rev1_tiny_sample.csv";
	private static final String TEST_DATA="/home/svictoroff/Documents/Kaggle/SalaryPrection/data/Valid_rev1.csv";
	
	private static final String JOB_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/.json";
	private static final String TITLE_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/titles.json";
	private static final String DESCRIPTION_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/descriptions.json";
	private static final String LOCATION_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/locations.json";
	private static final String INDUSTRY_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/industries.json";
	private static final String COMPANY_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/companies.json";
	
	public static void dumpSetAsList(Set<String> data, String filePath) throws IOException{
		BufferedWriter writer = new BufferedWriter(new FileWriter(new File(filePath)));
		Gson gson = new Gson();
		List<String> dataList = new ArrayList<String>(data);
		String json = gson.toJson(dataList);
		writer.write(json);
		writer.close();
	}
	public static void main(String[] args) throws IOException{
		CSVReader reader = new CSVReader(new FileReader(FULL_DATA));
		String[] nextLine;
		File file = new File(JOB_OUTPUT_FILE);
		BufferedWriter jobWriter = new BufferedWriter(new FileWriter(file));
		int counter = 0;
		Set<String> allTitleWords = new HashSet<String>();
		Set<String> allDescriptionWords = new HashSet<String>();
		Set<String> allLocations = new HashSet<String>();
		Set<String> allIndustries = new HashSet<String>();
		Set<String> allCompanies = new HashSet<String>();
		while ((nextLine = reader.readNext()) != null){
			Job job = new Job(nextLine);
			allTitleWords.addAll(job.getTitleWords());
			allDescriptionWords.addAll(job.getDescriptionWords());
			allLocations.add(job.getLocation());
			allIndustries.add(job.getIndustry());
			allCompanies.add(job.getCompany());
			Gson gson = new Gson();
			String json = gson.toJson(job);
			jobWriter.write(json + "\n");
			counter++;
			if (counter%1000 == 0){
				System.out.println(counter);
			}
		}
		jobWriter.close();
		System.out.println(allTitleWords.size());
		System.out.println(allDescriptionWords.size());
		System.out.println(allLocations.size());
		System.out.println(allIndustries.size());
		System.out.println(allCompanies.size());
		dumpSetAsList(allTitleWords, TITLE_OUTPUT_FILE);
		dumpSetAsList(allDescriptionWords, DESCRIPTION_OUTPUT_FILE);
		dumpSetAsList(allLocations, LOCATION_OUTPUT_FILE);
		dumpSetAsList(allIndustries, INDUSTRY_OUTPUT_FILE);
		dumpSetAsList(allCompanies, COMPANY_OUTPUT_FILE);
	}
}