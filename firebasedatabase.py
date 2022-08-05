import firebase_admin
from firebase_admin import db, auth
import hashlib

import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', level=logging.INFO)


class FirebaseDatabase:
    def __init__(self, cred_path, db_link):
        """
        A class used to manage the database database.
        :param cred_path: The path to the database credential file.
        :param db_link: The link to the database database.
        """

        self.cred_obj = firebase_admin.credentials.Certificate(cred_path)
        self.default_app = firebase_admin.initialize_app(self.cred_obj, {
            'databaseURL': db_link
        })

        self.db = db.reference("/")
        logging.info('Database initialized')

    def get(self, path):
        """
        Get the value of a given path in the database.
        :param path: The path to the value in the database.
        :return: A dictionary of the json object.
        """

        ref = db.reference(path)
        data = ref.get()
        try:
            logging.info(f'Retrieve data from {path} ({len(data)} element(s)) - data : {data}')
        except TypeError:
            logging.info(f'No data from {path} when retrieving')
        return data

    def set(self, path, value):
        """
        Set the value of a given path in the database.
        :param path: The path to the value in the database.
        :param value: The value to set.
        """
        self.db = db.reference(path)
        self.db.set(value)
        self.db = db.reference("/")
        logging.info(f'Set {path} to value : {value}')

    def add(self, path, value):
        data = self.get(path)
        print(data)
        if type(data) == list:
            data.append(value)
            self.set(path, data)
            logging.info(f'Added value to existing {path} - value : {value}')
        elif type(data) == dict:
            self.set(path, {**data, **value})
            logging.info(f'Added value to new {path} - value : {value}')
        else:
            logging.info(f'Added value to {path} - value : {value}')
            self.set(path, [value])

    def create_user(self, username, mail, password):
        """
        Create a new user in the database.
        :param username: The username of the new user.
        :param mail: The mail of the new user.
        :param password: The password of the new user.
        :return: The id of the new user.
        """

        user = auth.create_user(
            email=mail,
            password=password,
            display_name=username)

        # sha256 encoding of the password
        password = hashlib.sha256(password.encode()).hexdigest()

        self.add(f"usersData/{user.uid}", {"username": username, "sha2Password": password})
        self.add(f"data/{user.uid}", {"categories": ""})

        logging.info(f'Sucessfully created new user: {user.uid}')
