package library;

public class Book {
    private String title;
    private String author;
    private int year;
    
    public Book(String title, String author, int year) {
	this.title = title;
	this.author = author;
	this.year = year;
    }

    public String getTitle() {
	return title;
    }

    public String getAuthor() {
	return author;
    }

    public int getYear() {
	return year;
    }

    public void setTitle(String title) {
	this.title = title;
    }

    public void setAuthor(String author) {
	this.author = author;
    }

    public void setYear(int year) {
	this.year = year;
    }

    @Override
    public String toString() {
	return "TITLE: %s, AUTHOR: %s, YEAR: %d".formatted(title, author, year);
    }

    @Override
    public boolean equals(Object obj) {
	if ((obj == null) || !(obj instanceof Book))
	    return false;

	Book otherBook = (Book)obj;

	if (title.equals(otherBook.getTitle()) &&
	    author.equals(otherBook.getAuthor()) &&
	    year == otherBook.getYear())
	    return true;

	return false;
    }

    @Override
    public int hashCode() {
	return "%s%s%d".formatted(title, author, year).hashCode();
    }
}
