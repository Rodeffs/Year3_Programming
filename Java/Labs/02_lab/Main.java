import java.util.Map;
import java.util.Arrays;
import java.util.HashMap;

public class Main {

    static String longest_unique_substring(String input_str) {
	
	// Хеш-таблица используется, чтобы увеличить скорость алгортима, т.е. чтобы не пробегаться каждый раз по строке проверяя, был ли уже этот символ

	Map<Character, Boolean> unique_chars = new HashMap<Character, Boolean>();

	String longest_substring = "";
	String cur_substring = "";

	for (int i = 0; i < input_str.length(); i++) {
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

    static int[] concatenate_sorted_arrays(int[] arr1, int[] arr2) {
	int len1 = arr1.length, len2 = arr2.length;
	int output_len = len1 + len2;
	int[] output_arr = new int[output_len];
	
	int i = 0, j = 0;

	while (i+j < output_len-1) {

	    if ( (i < len1) && (j < len2) ) {
		int cur1 = arr1[i], cur2 = arr2[j];

		if (cur1 < cur2) {
		    output_arr[i+j] = cur1;
		    i++;
		}

		else {
		    output_arr[i+j] = cur2;
		    j++;
		}
	    }

	    else if (i >= len1) {
		for (int k = j; k < len2; k++) 
		    output_arr[i+k] = arr2[k];
		break;
	    }

	    else {
		for (int k = i; k < len1; k++) 
		    output_arr[j+k] = arr1[k];
		break;
	    }
	}

	return output_arr;
    }
    
    public static void main(String[] args) {
	
	System.out.println("Задание 1:\n");

	String sample_str = "fkdlf3440-0flfkffkffffsklskallkellkpropowhelloabcdefghoeieow010";

	System.out.println("Исходная строка:\n" + sample_str);
	System.out.println("Наибольшая подстрока без повторяющихся символов:\n" + longest_unique_substring(sample_str));

	System.out.println("\nЗадание 2:\n");

	int[] arr1 = { 0, 1, 2, 3, 4, 5 };
	int[] arr2 = { 6, 7, 8, 9, 10, 11 };

	System.out.println("Отсортированный массив 1:\n" + Arrays.toString(arr1));	
	System.out.println("Отсортированный массив 2:\n" + Arrays.toString(arr2));

	int[] concatenated_arr = concatenate_sorted_arrays(arr1, arr2);
	System.out.println("Объединённый отсортированный массив:\n" + Arrays.toString(concatenated_arr));

	System.out.println("\nЗадание 3:\n");
    }
}
