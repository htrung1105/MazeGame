import json
import pprint

class UserDatabase:
    def __init__(self, filename = 'user_data.json'):
        self.filename = filename
        self.users = {}

    def leaderboard(self):
     easy_list = []
     for easy in self.users:
        if 'level' in self.users[easy] and self.users[easy]['level'] == 'easy':
            easy_list.append(self.users[easy])
     easy_list.sort(key=lambda x: x['time'])

     medium_list = []
     for medium in self.users:
        if 'level' in self.users[medium] and self.users[medium]['level'] == 'medium':
            medium_list.append(self.users[medium])
     medium_list.sort(key=lambda x: x['time'])

     hard_list = []
     for hard in self.users:
        if 'level' in self.users[hard] and self.users[hard]['level'] == 'hard':
            hard_list.append(self.users[hard])
     hard_list.sort(key=lambda x: x['time'])

     return (easy_list, medium_list, hard_list)

    # Load data from json database
    def load_users(self):
        try:
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            self.users = {}

    # Save data to json database
    def save_users(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=3)

    # Register a new user with username and password -> save to json database
    def register_user(self, username, password):
        if username in self.users:
            return False                    # Dang ki that bai
        self.users[username] = {'password': password}   ## Khoi tao cac thong so khac cua user
        self.save_users()
        return True                         # Dang ki thanh cong

    # Login user with username and password 
    # -> return tuple of (username, password) if success, False if fail
    def login_user(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == password:
                return (username, password)
            else:
                return False # wrong password
        else:
            return False # wrong username
        
    # Use this function to get data of user    
    def load_game(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == password:
                return self.users[username]
        return False
    
    def update_user(self, username, password, data):
        if username in self.users:
            if self.users[username]['password'] == password:
                self.users[username] = data   ## Khoi tao cac thong so khac cua user
                self.save_users()
                return True
            else: 
                return False
        else:
            return False

# UserDatabase.login_user(username, password) -> return False : username//password not exist//not true
#                         username&password True-> return: self.users[username]

###########DEMO##########################
db = UserDatabase('user_data.json')
db.load_users()

# Dang ki tai khoan
print(db.register_user('user1', 'pas1'))
print(db.register_user('user2', 'pas1'))
print(db.register_user('user3', 'pas1'))
print(db.register_user('user4', 'pas1'))
print(db.register_user('user5', 'pas1'))
print(db.register_user('user6', 'pas1'))
# Dang nhap
#print(db.login_user('user3', 'pas1'))

# update thong tin user
db.update_user('user1', 'pas1', {'user':'user1', 'password':'pas1', 'time':12308, 'level' : 'easy'})
db.update_user('user2', 'pas1', {'user':'user1', 'password':'pas1', 'time':456, 'level' : 'easy'})
db.update_user('user3', 'pas1', {'user':'user1', 'password':'pas1', 'time':789, 'level' : 'easy'})
db.update_user('user4', 'pas1', {'user':'user1', 'password':'pas1', 'time':1234, 'level' : 'medium'})
db.update_user('user5', 'pas1', {'user':'user1', 'password':'pas1', 'time':4567, 'level' : 'medium'})
db.update_user('user6', 'pas1', {'user':'user1', 'password':'pas1', 'time':7890, 'level' : 'hard'})

pprint.pprint(db.leaderboard())