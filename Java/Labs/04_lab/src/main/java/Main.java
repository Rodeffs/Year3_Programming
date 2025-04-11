import library.*;

public class Main {
    
    public static void main(String[] args) {
	Library libraryTest = new Library();
	
	Book book1 = new Book("War and Peace", "Leo Tolstoy", 1869);
	Book book2 = new Book("Anna Karenina", "Leo Tolstoy", 1878);
	Book book3 = new Book("Ruslan and Ludmila", "Alexander Pushkin", 1820);
	Book book4 = new Book("Eugene Onegin", "Alexander Pushkin", 1833);
	Book book5 = new Book("The Captain's Daughter", "Alexander Pushkin", 1836);
	Book book6 = new Book("The Master and Margarita", "Mikhail Bulgakov", 1967);
	
	libraryTest.addBook(book1);
	libraryTest.addBook(book2);
	libraryTest.addBook(book3);
	libraryTest.addBook(book4);
	libraryTest.addBook(book5);
	libraryTest.addBook(book6);

	System.out.println("Список книг:");
	libraryTest.printAllBooks();
	
	System.out.println("\nСтатистика книг авторов:");
	libraryTest.printAuthorStatistics();

	System.out.println("\nСписок авторов:");
	libraryTest.printUniqueAuthors();

	libraryTest.removeBook(book3);

	System.out.println("\nСписок книг после удаления одной книги:");
	libraryTest.printAllBooks();

	System.out.println("\nСтатистика книг авторов после удаления одной книги:");
	libraryTest.printAuthorStatistics();

	libraryTest.removeBook(book4);
	libraryTest.removeBook(book5);

	System.out.println("\nСписок книг после удаления всех книг одного автора:");
	libraryTest.printAllBooks();

	System.out.println("\nСписок авторов после удаления всех книг одного автора:");
	libraryTest.printUniqueAuthors();

	System.out.println("\nСтатистика книг авторов после удаления всех книг одного автора:");
	libraryTest.printAuthorStatistics();
    }
}
