package library;
import java.util.HashSet;
import java.util.Set;
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

public class Library {
    private List<Book> books = new ArrayList<Book>();
    private Set<String> authors = new HashSet<String>();
    private Map<String, Integer> stats = new HashMap<String, Integer>();

    public Library() {}

    public void addBook(Book book) {
	if (books.contains(book))  // по идее в библиотеке может быть несколько одинаковых книг, но условие задания предполагает иначе
	    return;

	books.add(book);

	String author = book.getAuthor();
	authors.add(author);
	
	if (stats.get(author) == null)
	    stats.put(author, 1);

	else
	    stats.put(author, stats.get(author) + 1);
    }

    public void removeBook(Book book) {
	if (!books.contains(book))
	    return;

	books.remove(book);
	String author = book.getAuthor();
	
	if (findBooksByAuthor(author).isEmpty())
	    authors.remove(author);
	
	if (stats.get(author) <= 1)
	    stats.remove(author);

	else
	    stats.put(author, stats.get(author) - 1);
    }

    public List<Book> findBooksByAuthor(String author) {
	List<Book> authorBooks = new ArrayList<Book>();

	for (var book : books)
	    if (book.getAuthor().equals(author))
		authorBooks.add(book);

	return authorBooks;
    }

    public List<Book> findBooksByYear(int year) {
	List<Book> yearBooks = new ArrayList<Book>();

	for (var book : books)
	    if (book.getYear() == year)
		yearBooks.add(book);

	return yearBooks;
    }

    public void printAllBooks() {
	for (var book : books)
	    System.out.println(book);
    }

    public void printUniqueAuthors() {
	for (var author : authors)
	    System.out.println(author);
    }

    public void printAuthorStatistics() {
	for (Map.Entry<String, Integer> authorStat : stats.entrySet())
	    System.out.println("AUTHOR: " + authorStat.getKey() + ", BOOK COUNT: " + authorStat.getValue());
    }
}
