import bcrypt
import re

class Security:
    @staticmethod
    def get_hashed_password(plain_text_password):
        # Hash and salt password
        # Salt is stored in the password
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        # Check hashed password.
        return bcrypt.checkpw(plain_text_password, hashed_password)

    @staticmethod
    def check_password_strength(password):
        error_msg = ""
        if len(password) < 10:
            error_msg += "Password must be at least 10 characters\n"
        if not re.search("[a-z]", password):
            error_msg += "Password must contain at least one lower-case character\n"
        if not re.search("[A-Z]", password):
            error_msg += "Password must contain at least one upper-case character\n"
        if not re.search("[0-9]", password):
            error_msg += "Password must contain at least one number\n"
        if not re.search("[!\"£$%^&*()@#~':;,.]", password):
            error_msg += "Password must contain at least one special character\n"

        return error_msg

    @staticmethod
    def check_email(email):
        # Check email is in correct format
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email) and email.count('@') == 1:
            return ""
        else:
            return "Email Address Not Valid"
