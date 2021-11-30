import threading
from database import Database
from Socket import Socket
import time


def get_time():
    current = time.localtime()
    exact = time.strftime("%Y-%m-%d %H:%M:%S", current)
    return exact


def checker_to_private(message):
    if message.startswith('[PRIVATE] TO '):
        return True
    else:
        return False


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.users = []
        self.nicknames = []
        self.addresses = []
        self.host = "127.0.0.1"
        self.port = 1234
        self.message_id = 0

    def connect(self):
        self.server.bind(
            (self.host, self.port)
        )
        self.server.listen(4)
        print("Server running!")

    def broadcast(self, message,sender):
        for user in self.users:
            current = get_time()
            user.send(f"[{current}]{sender}: {message.decode('utf-8')}".encode('utf-8'))

    def broadcast_private(self, message,receiver,sender):
        for user in self.users:
            current = get_time()
            index = self.users.index(user)
            if self.nicknames[index] == receiver:
                user.send(f"[{current}]{sender}: {message}".encode('utf-8'))

    def handle(self, user, addr, database):
        while True:
            try:
                message = user.recv(2048)
                print(message.decode('utf-8'))
                index = self.users.index(user)
                if message is None:
                    break
            except:
                index = self.users.index(user)
                self.users.remove(user)
                user.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('utf-8'))
                self.nicknames.remove(nickname)
                break
            else:
                message = message.decode('utf-8')
                database.cursor.execute("SELECT message_id FROM messages ORDER BY message_id DESC LIMIT 1")
                result = database.cursor.fetchone()
                if result is None:
                    self.message_id = 0
                else:
                    self.message_id = self.message_id + 1
                timer = get_time()

                private = checker_to_private(message)

                if private:
                    data = message.split('[PRIVATE] TO')[1].strip()
                    receiver = data.split(' ', 1)[0]
                    private_message = data.split(' ', 1)[1]
                    database.cursor.execute(
                        f"INSERT INTO messages(message_id,username,receiver,message,send_time) VALUES({self.message_id}, '{self.nicknames[index]}', '{receiver}', '{private_message}', '{timer}')")
                    database.conn.commit()
                    database.cursor.execute(
                        f"SELECT * FROM messages WHERE username = '{self.nicknames[index]}' AND receiver = '{receiver}'")
                    messages = database.cursor.fetchall()
                    for i in messages:
                        print(f"{i}")
                    print(private_message)
                    self.broadcast_private(private_message, receiver,self.nicknames[index])
                else:
                    database.cursor.execute(
                        f"INSERT INTO messages(message_id,username,receiver,message,send_time) VALUES({self.message_id}, '{self.nicknames[index]}', 'all', '{message}', '{timer}')")
                    database.conn.commit()
                    database.cursor.execute("SELECT * FROM messages")
                    messages = database.cursor.fetchall()
                    for i in messages:
                        print(f"{i}")
                    message = message.encode('utf-8')
                    self.broadcast(message,self.nicknames[index])


    def database_creation(self, database):
        database.cursor.execute(
            "CREATE TABLE IF NOT EXISTS messages(message_id INTEGER,username TEXT,receiver TEXT,message TEXT, send_time timestamp);")
        database.conn.commit()

        database.cursor.execute("CREATE TABLE IF NOT EXISTS clients(username TEXT,password TEXT);")
        database.conn.commit()

    def receive(self, database):
        receive_thread = threading.Thread(target=self.receive, args=(database,))
        receive_thread.start()
        while True:
            user, address = self.server.accept()
            print("Connected with {}".format(str("address")))
            nickname = user.recv(2048).decode('utf-8')
            self.nicknames.append(nickname)
            self.users.append(user)
            print("Nickname is {}".format(nickname))
            self.broadcast("{} joined!".format(nickname).encode('utf-8'),sender="")
            user.send('Connected to the server!'.encode('utf-8'))
            thread = threading.Thread(target=self.handle, args=(user, address, database))
            thread.start()


if __name__ == "__main__":
    database = Database()
    database.connect()
    server = Server()
    server.database_creation(database)
    server.connect()
    server.receive(database)
