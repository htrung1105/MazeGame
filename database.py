import json
import pprint

class UserDatabase:
    """
        def register_user(username, password) :: 
            Register a new user with username and password
            Return True if success, False if fail

        def login_user(username, password) ::
            Login user with username and password
            Return tuple of (username, password) if success, False if fail

        def load_user(username, password) ::
            Load data from a user (all game, password, username)
            Return False if fail, return user data if success

        def load_game(username, password, game_name) ::
            Load a game from a user
            Return False if fail, return game data if success

        def save_game(username, password, game_name, data) ::
            Save a game to a user
            Return False if fail, return True if success

        def pack_data() ::
            Pack a game data into a dictionary, included keys:
                - 'map', 'level', 'size', 'start', 'end', 'time', 'status', 'username'


        def leaderboard() ::
            return False if no user, return a tuple of 3 list:
                - Easy list, Medium list, Hard list in order of increasing time
    """    
    def __init__(self, filename = 'user_data.json'):
        self.filename = filename
        self.users = {}
        self.load_data()

    # Load data from json database
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, initialize an empty dictionary
            self.users = {}

    # Save data to json database
    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=3)

    # Register a new user with username and password -> save to json database
    def register_user(self, username, password):
        if username in self.users:
            return False                    # Dang ki that bai
        self.users[username] = {'password': password}   ## Khoi tao cac thong so khac cua user
        self.save_data()
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

    # Use this function to load data from a user (all game, password, username)    
    def load_users(self, username, password):
        if username in self.users:
            if self.users[username]['password'] == password:
                return self.users[username]
        return False
        
    # Use this function to load a game from a user    
    def load_game(self, username, password, game_name):
        if username in self.users:
            if self.users[username]['password'] == password:
                return self.users[username][game_name]
        return False
    
    # Use this function to save a game to a user 
    def save_game(self, username, password, game_name, data):
        if username in self.users:
            if self.users[username]['password'] == password:
                self.users[username][game_name] = data
                self.save_data()
                return True
        return False

    def leaderboard(self):
        if len(self.users) == 0:
            return False
        easy_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'easy':
                        easy_list.append(self.users[user][game_name])
        easy_list.sort(key=lambda x: x['time'])

        medium_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'medium':
                        medium_list.append(self.users[user][game_name])
        medium_list.sort(key=lambda x: x['time'])

        hard_list = []
        for user in self.users:
            for game_name in self.users[user]:
                if game_name != 'password':
                    if self.users[user][game_name]['level'] == 'hard':
                        hard_list.append(self.users[user][game_name])
        hard_list.sort(key=lambda x: x['time'])

        return (easy_list, medium_list, hard_list)

    def pack_data(self, map, level, size_x, size_y, start_x, start_y, end_x, end_y, time, status, username):
        data = {}
        data['map'] = map
        data['level'] = level
        data['size'] = [size_x, size_y]
        data['start'] = [start_x, start_y]
        data['end'] = [end_x, end_y]
        data['time'] = time
        data['status'] = status
        data['username'] = username
        return data


#########################DEMO##########################
'''
db = UserDatabase('user_data.json')

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
db.save_game('user1', 'pas1', 'game1', {'username':'user1', 'password':'pas1', 'time':12308, 'level' : 'easy'})
db.save_game('user2', 'pas1', 'game1', {'username':'user2', 'password':'pas1', 'time':456, 'level' : 'easy'})
db.save_game('user3', 'pas1', 'game1', {'username':'user3', 'password':'pas1', 'time':789, 'level' : 'easy'})
db.save_game('user4', 'pas1', 'game1', {'username':'user4', 'password':'pas1', 'time':1234, 'level' : 'medium'})
db.save_game('user5', 'pas1', 'game1', {'username':'user5', 'password':'pas1', 'time':4567, 'level' : 'medium'})
db.save_game('user6', 'pas1', 'game1', {'username':'user6', 'password':'pas1', 'time':7890, 'level' : 'hard'})
db.save_game('user6', 'pas1', 'game2', {'username':'user6', 'password':'pas1', 'time':23, 'level' : 'hard'})
db.save_game('user6', 'pas1', 'game3', {'username':'user6', 'password':'pas1', 'time':4, 'level' : 'hard'})
db.save_game('user4', 'pas1', 'game2', {'username':'user4', 'password':'pas1', 'time':34, 'level' : 'hard'})
db.save_game('user4', 'pas1', 'game3', {'username':'user4', 'password':'pas1', 'time':455, 'level' : 'hard'})

pprint.pprint(db.leaderboard())
pprint.pprint(db.users)

'''