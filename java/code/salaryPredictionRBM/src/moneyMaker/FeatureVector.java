package moneyMaker;

import java.util.ArrayList;
import java.util.List;

public class FeatureVector {

	private static final String TITLE_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/titles.json";
	private static final String DESCRIPTION_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/descriptions.json";
	private static final String LOCATION_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/locations.json";
	private static final String INDUSTRY_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/industries.json";
	private static final String COMPANY_OUTPUT_FILE="/home/svictoroff/Documents/Kaggle/SalaryPrection/code/usefulData/companies.json";
	private enum FIELD_FILES{
		TITLE_OUTPUT_FILE, DESCRIPTION_OUTPUT_FILE, LOCATION_OUTPUT_FILE, INDUSTRY_OUTPUT_FILE,
		COMPANY_OUTPUT_FILE
	}
	
	private List<Boolean> title;
	private List<Boolean> description;
	private List<Boolean> location;
	private List<Boolean> company;
	private List<Boolean> industry;
	private enum FIELD{
		TITLE, DESCRIPTION, LOCATION, COMPANY, INDUSTRY
	}
	
	public FeatureVector(){
		title = new ArrayList<Boolean>();
		description = new ArrayList<Boolean>();
		location = new ArrayList<Boolean>();
		company = new ArrayList<Boolean>();
		industry = new ArrayList<Boolean>();
	}
	
	public void initializeField(Job job, FIELD field){
		
	}
	
	
	
}