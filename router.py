import Handler.Handler as Work #вызов команды task(name_command)
from Model.Robot import Robot
import DataLog as Log
from socket import *
from threading import Thread
import json as js
from Manager import SendManager

sock = socket()
sock.bind(('192.168.0.104', 2510))
sock.listen(6)

listing = Log.DataBase()


def push_dataLog(data: dict, ip):
    if data["Type_command"] == "Login":
        new_robot = Robot(ip=ip, state=data["State"], typeo=data["Type_robot"], zone=data["District"])
        listing.attach([new_robot, len(listing.robot) + 1])


def delite_datalog(ip):
    robot = list(filter(lambda x: x[0].ip_robot.getsockname()[0] == ip[0], listing.robot))
    listing.detach(robot[0])


def client(ip_data):
    while True:
        try:
            SendManager.Send().login(ip_data)
            req = ip_data.recv(1024).decode()
            data = js.loads(req)
            push_dataLog(data, ip_data)
            Work.task(data)
            print([i[0].print_sost() for i in listing.robot], "robot")
            # print(listing.task_list_robot, "task")
            # print(listing.task_list_sort, "task")
            # sys.stdout.write("\r list_robot: {0}, list_sort: {1}, qr_flag: {2}, angle: {3}".format(listing.task_list_robot, listing.task_list_sort, listing.list_qr_flag, listing.list_cal))

        except ConnectionResetError:
            delite_datalog(sock.getsockname())
            break


while True:
    print('connection...')
    client1, mass = sock.accept()
    print(mass, 'connect')
    Thread(target=client, args=(client1,), daemon=True).start()