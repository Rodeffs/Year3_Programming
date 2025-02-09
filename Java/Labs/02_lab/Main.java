import java.util.Map;
import java.util.HashMap;

public class Main {

    static String longest_unique_substring(String input_str) {
	
	// Хеш-таблица используется, чтобы увеличить скорость алгортима, т.е. чтобы не пробегаться каждый раз по строке проверяя, был ли уже этот символ

	Map<Character, Boolean> unique_chars = new HashMap<Character, Boolean>();

	String longest_substring = "";
	String cur_substring = "";

	for (int i=0; i < input_str.length(); i++) {
	    char cur_char = input_str.charAt(i);

	    if (unique_chars.containsKey(cur_char)) {
		if (cur_substring.length() > longest_substring.length()) 
		    longest_substring = cur_substring;

		cur_substring = "";
		unique_chars.clear();
	    }
	    else {
		unique_chars.put(cur_char, true);
		cur_substring += cur_char;
	    }
	}

	return longest_substring;
    }
    
    public static void main(String[] args) {
	
	String sample_str = "fkdlf3440-0flfkffkffffsklskallkellkpropowhelloabcdefghoeieow010";
	System.out.println("Исходная строка:\n" + sample_str);
	System.out.println("Наибольшая подстрока без повторяющихся символов:\n" + longest_unique_substring(sample_str));
    }
}
