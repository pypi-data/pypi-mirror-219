import datetime
import random
import string


class Create_User:
    def __init__(self, first_name: str = "Ttpvt", last_name: str = "User"):
        """
        Module to create a new student
        :param first_name: First name of the student, default Ttpvt
        :param last_name: Last name of the student, default User
        """
        self.created_timestamp = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ",
                                                                                                        "").replace(".",
                                                                                                                    "")
        self.first_name = first_name
        self.last_name = last_name + self.created_timestamp[0:-6]

    def get_first_name(self) -> str:
        """
        return the first name of the student.
        :return: The first name of the student as a string.
        """
        return self.first_name

    def get_last_name(self) -> str:
        """
        return the last name of the student.
        :return: The last name of the student as a string.
        """
        return self.last_name

    def create_email(self, domain_provider: str = "yopmail", top_domain: str = "com") -> str:
        """
        Function to create a new email based on user details and current timestamp.
        :param domain_provider: The email domain provider for the email address. Default is set to 'yopmail'.
        :param top_domain: The top-level domain for the email address. Default is set to 'com'.
        :return: The newly created email address  as a string
        """
        self.email = (self.first_name + "_" + self.last_name + "@" + domain_provider + "." + top_domain).lower()
        return self.email

    def get_email(self) -> str:
        """
        return the email address associated with the student.
        :return: The email address as a string if it exists, otherwise returns "".
        """
        try:
            return self.email
        except AttributeError:
            return ""

    def create_random_password(self) -> str:
        """
        Generates a random password and ensures it meets certain criteria.
        :return: The generated password as a string, meeting length and composition requirements.
                 Returns None if no valid password can be generated.
        """
        pwd_length = random.randint(8, 16)
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        self.password = ''.join(random.choice(characters) for _ in range(pwd_length))
        # Ensure at least one number and one capital letter
        while not any(char.isdigit() for char in self.password) or not any(char.isupper() for char in self.password):
            self.password = ''.join(random.choice(characters) for _ in range(pwd_length))
        return self.password

    def set_custom_password(self, password: str) -> str:
        """
        Function to set a new custom password
        :param password:  given by the user
        :return: The newly created password address as a string
        """
        self.password = password
        return password

    def get_password(self) -> str:
        """
        return the password associated with the student.
        :return: The password as a string if it exists, otherwise returns "".
        """
        try:
            return self.password
        except AttributeError:
            return ""

    def create_random_mobile_number(self, dial_code: str, number_length: int) -> list:
        """
        Function to create a new random mobile number
        :param dial_code: dial code of the mobile number, starting with +, else + is appended
        :param number_length: length of the mobile number as integer,
        :return: return a list consist of dial code and random generated mobile number
        """
        if dial_code[0] != "+":
            dial_code = "+" + dial_code

        if number_length > 4:
            number = self.created_timestamp[0:4] + self.created_timestamp[-(number_length-3):-1]
        else:
            number = sorted(self.created_timestamp[-(number_length+1):-1], reverse=True)
        self.mobile_number = [dial_code, number]

        return self.mobile_number

    def set_mobile_number(self, dial_code:str, number: int) -> list:
        """
        :param dial_code: dial code of the mobile number, starting with +, else + is appended
        :param number: custom mobile number
        :return: return a list consist of dial code and custom mobile number
        """
        if dial_code[0] != "+":
            dial_code = "+" + dial_code
        self.mobile_number = [dial_code, str(number)]

        return self.mobile_number

    def get_mobile_number(self) -> list:
        """
        :return: the mobile number of the student
        """
        try:
            return self.mobile_number
        except AttributeError:
            return []

    def get_self_attributes(self):
        """
        Returns a dictionary of all instance attributes and their values for the current object.
        :return: A dictionary containing the instance attributes and their values.
        """
        return self.__dict__