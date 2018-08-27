import sqlite3

class User:

    def __init__(self, username, password='Undefined', type='Undefined'):
        self.username = username
        self.password = password
        self.type = type

    def add_user(self):
        user = self.get_user_by_name(self.username)
        if user is None:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'INSERT INTO users VALUES (?, ?, ?)'
            cursor.execute(query, (self.username, self.password, self.type,))
            connection.commit()
            connection.close()
            return 'User successfully created!'
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'UPDATE users SET password=?, type=? WHERE name=?'
            cursor.execute(query, (self.password, self.type, self.username,))
            connection.commit()
            connection.close()
            return "User has been successfully updated!"

    def delete_user(self):
        user = self.get_user_by_name(self.username)
        if user is not None:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'DELETE FROM users WHERE name=?'
            cursor.execute(query, (self.username,))
            connection.commit()
            connection.close()
            return "User successfully deleted!"
        else:
            return "User has not been found!"

    @classmethod
    def get_user_by_name(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE name=?'
        data = cursor.execute(query, (username,))
        user_data = data.fetchone()
        if user_data is not None:
            return cls(username=user_data[0], password=user_data[1], type=user_data[2])
        else:
            return None

    def get_type_by_name(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT type FROM users WHERE name=?'
        result = cursor.execute(query, (name,))
        data = result.fetchone()
        return data[0]