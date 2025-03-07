package login;

class Guest extends User {
    public Access getAccess() {
	return Access.GUEST;
    }

    public boolean login(String username, String password) {
	return true;
    }
}
