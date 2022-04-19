import socket
import logging
import json

logging.basicConfig(filename="server.log",
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

with open("appsettings.json", "r") as read_file:
    config = json.load(read_file)

BUFFSIZE = config["BUFFSIZE"]

def printlog(message):
    print(message)
    logging.info(message)


def handle_connection(conn):
    filename = conn.recv(BUFFSIZE).decode("utf8")
    file = open("sent_"+filename, "ab")
    while True:
        data = conn.recv(BUFFSIZE)
        file.write(data)
        if not data:
            print("Done, file saved as {}".format("sent_"+filename))
            conn.close()
            file.close()
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config["HOST"], config["PORT"]))
    server.listen()
    connection, address = server.accept()
    printlog("Connected")
    handle_connection(connection)


if __name__ == "__main__":
    main()
