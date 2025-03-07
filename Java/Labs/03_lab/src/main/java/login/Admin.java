package login;

class Admin extends User {
    String username = "admin";
    String password = "12345";

    public Access getAccess() {
	return Access.ADMIN;
    }

    public boolean login(String username, String password) {
	if (this.username.equals(username) && this.password.equals(password))
	    return true;

	return false;
    }
}
