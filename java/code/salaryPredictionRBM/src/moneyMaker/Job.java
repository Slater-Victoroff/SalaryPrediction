package moneyMaker;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import stemmer.EnglishStemmer;
import stemmer.PorterStemmer;
import stemmer.SnowballStemmer;

public class Job {

	private Double id;
	private String company;
	private String title;
	private String description;
	private String industry;
	private String location;
	private Double salary;
	private List<String> titleWords;
	private List<String> descriptionWords;
	
	public Job(String[] fileLine){
		this.id = Double.parseDouble(fileLine[0]);
		this.title = fileLine[1];
		this.description = fileLine[2];
		this.location = fileLine[4].toLowerCase().trim();
		this.company = fileLine[7].toLowerCase().trim();
		this.industry = fileLine[8].toLowerCase().trim();
		this.salary = Double.parseDouble(fileLine[10]);
		PorterStemmer stemmer = new PorterStemmer();
		this.titleWords = parseRawString(this.title, stemmer);
		this.descriptionWords = parseRawString(this.description, stemmer);
	}
	
	public List<String> parseRawString(String rawString, PorterStemmer stemmer){
		List<String> answer = new ArrayList<String>();
		String[] firstSplit = rawString.split("[\\p{P} \\t\\n\\r]");
		for (String s: firstSplit){
			stemmer.add(s.toCharArray(), s.length());
			stemmer.stem();
			answer.add(stemmer.toString());
		}
//		for (String s: firstSplit){
//			if ((s.contains(".com"))||(s.contains(".net"))||(s.contains(".edu")||(s.contains(".org")))){
//				continue;
//			}
//			else {rawSplit.addAll(Arrays.asList(s.split("[\\p{P}]")));}
//		}
//		for (String s: rawSplit){
//			stemmer.setCurrent(s.toLowerCase());
//			stemmer.stem();
//			String addition = stemmer.getCurrent();
//			answer.add(addition);
//		}
		return answer;
	}
	
	public List<String> getTitleWords(){
		return this.titleWords;
	}
	
	public List<String> getDescriptionWords(){
		return this.descriptionWords;
	}
	
	public String getCompany(){
		return this.company;
	}
	
	public String getLocation(){
		return this.location;
	}
	
	public String getIndustry(){
		return this.industry;
	}
}
