package login;

abstract class User {
    abstract public Access getAccess();
    abstract public boolean login(String username, String password);
}
