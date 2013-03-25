package moneyMaker;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import stemmer.EnglishStemmer;
import stemmer.SnowballStemmer;

public class Job {

	private Double id;
	private String company;
	private String title;
	private String description;
	private String industry;
	private String location;
	private Double salary;
	private Set<String> titleWords;
	private Set<String> descriptionWords;
	
	public Job(String[] fileLine){
		this.id = Double.parseDouble(fileLine[0]);
		this.title = fileLine[1];
		this.description = fileLine[2];
		this.location = fileLine[4];
		this.company = fileLine[7];
		this.industry = fileLine[8];
		this.salary = Double.parseDouble(fileLine[10]);
		SnowballStemmer stemmer = (SnowballStemmer) new EnglishStemmer();
		this.titleWords = parseRawString(this.title, stemmer);
		this.descriptionWords = parseRawString(this.description, stemmer);
	}
	
	public Set<String> parseRawString(String rawString, SnowballStemmer stemmer){
		Set<String> answer = new HashSet<String>();
		String[] rawSplit = rawString.split("[\\p{P} \\t\\n\\r]");
		for (String s: rawSplit){
			stemmer.setCurrent(s.toLowerCase());
			stemmer.stem();
			if (stemmer.getCurrent().length() > 0){
				answer.add(stemmer.getCurrent());
			}
		}
		return answer;
		
	}
}
