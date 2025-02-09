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

	while (i+j < output_len) {

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
		output_arr[i+j] = arr2[j];
		j++;
	    }

	    else {
		output_arr[i+j] = arr1[i];
		i++;
	    }
	}

	return output_arr;
    }
    
    static int max_subarray_sum(int[] arr) {
	int max_sum = Integer.MIN_VALUE;
	int cur_sum = 0;

	for (int i = 0; i < arr.length; i++) {
	    cur_sum += arr[i];

	    if (cur_sum > max_sum)
		max_sum = cur_sum;

	    if (cur_sum < 0)
		cur_sum = 0;
	}

	return max_sum;
    }

    static int[][] rotate_array_90_clockwise(int[][] arr) {
	int max_row = arr[0].length, max_column = arr.length;
	int[][] rotated_array = new int[max_row][max_column];

	for (int i = 0; i < max_row; i++) 
	    for (int j = 0; j < max_column; j++) 
		rotated_array[i][j] = arr[max_column-j-1][i];
	    
	return rotated_array;
    }

    static int[] target_pair_sum(int[] arr, int target) {
	for (int i = 0; i < arr.length-1; i++) 
	    for (int j = i+1; j < arr.length; j++) 
		if (arr[i] + arr[j] == target) {
		    int[] pair = { arr[i], arr[j] };
		    return pair;
		}

	return null;	
    }

    static int[][] rotate_array_90_counter_clockwise(int[][] arr) {
	int max_row = arr[0].length, max_column = arr.length;
	int[][] rotated_array = new int[max_row][max_column];

	for (int i = 0; i < max_row; i++) 
	    for (int j = 0; j < max_column; j++) 
		rotated_array[i][j] = arr[j][max_row-i-1];
	    
	return rotated_array;
    }

    static void print_2d_arr(int[][] arr) {
	for (int i = 0; i < arr.length; i++)
	    System.out.println(Arrays.toString(arr[i]));
    }

    public static void main(String[] args) {
	System.out.println("Задание 1:\n");

	String sample_str = "fkdlf3440-0flfkffkffffsklskallkellkpropowhelloabcdefghoeieow010";

	System.out.println("Исходная строка:\n" + sample_str);
	System.out.println("Наибольшая подстрока без повторяющихся символов:\n" + longest_unique_substring(sample_str));

	System.out.println("\nЗадание 2:\n");

	int[] arr1 = { 0, 2, 4, 6, 8, 10 };
	int[] arr2 = { 1, 3, 5, 7, 9, 11 };

	System.out.println("Отсортированный массив 1:\n" + Arrays.toString(arr1));	
	System.out.println("Отсортированный массив 2:\n" + Arrays.toString(arr2));

	int[] concatenated_arr = concatenate_sorted_arrays(arr1, arr2);
	System.out.println("Объединённый отсортированный массив:\n" + Arrays.toString(concatenated_arr));

	System.out.println("\nЗадание 3:\n");

	int[] arr3 = { 10, 10, -1, 10 };
	
	System.out.println("Исходный массив:\n" + Arrays.toString(arr3));
	System.out.println("Максимальная сумма подмассива:\n" + max_subarray_sum(arr3));
	
	System.out.println("\nЗадание 4:\n");

	int[][] arr2d = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 }, { 10, 11, 12 } };
	
	System.out.println("Исходный массив:");
	print_2d_arr(arr2d);

	int[][] rotated_90_clockwise = rotate_array_90_clockwise(arr2d);
	System.out.println("Массив, повёрнутый на 90 градусов по часовой стрелке:");
	print_2d_arr(rotated_90_clockwise);

	System.out.println("\nЗадание 5:\n");

	int[] arr4 = { 1, 2, 3, 4 };
	int target = 6;
	
	System.out.println("Исходный массив:\n" + Arrays.toString(arr4));
	System.out.println("Искомая сумма:\n" + target);

	int[] pair = target_pair_sum(arr4, target);

	if (pair != null)
	    System.out.println("Искомая пара элементов:\n" + Arrays.toString(pair));
	else
	    System.out.println("Искомой пары в массиве нет");

	System.out.println("\nЗадание 8:\n");

	System.out.println("Исходный массив:");
	print_2d_arr(arr2d);

	int[][] rotated_90_counter_clockwise = rotate_array_90_counter_clockwise(arr2d);
	System.out.println("Массив, повёрнутый на 90 градусов против часовой стрелки:");
	print_2d_arr(rotated_90_counter_clockwise);
    }
}
