class AdminAuth:
    def __init__(self):
        self.admin_password = "admin123" # Hardcarded admin password for simplicity
        self.is_logged_in = False
    def login(self, password):
        if password == self.admin_password: # Check if the provided password matches the admin password
            self.is_logged_in = True
            return True
        else:
            return False
    def get_login_status(self):
        return self.is_logged_in # Return the login status of the admin user
    
    def logout(self):
        self.is_logged_in = False ## Logout the admin user
