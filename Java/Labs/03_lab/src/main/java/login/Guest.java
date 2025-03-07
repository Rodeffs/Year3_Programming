package login;

class Guest extends User {
    public boolean login(String username, String password) {
	return true;
    }
}
