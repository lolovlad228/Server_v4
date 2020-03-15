from Observers.IObserver import Observer
from itertools import takewhile
from socket import socket
import json as js


class Robot(Observer):

    ip_robot = None
    type_robot = None
    state_robot = None
    zone = None

    def __init__(self, ip, typeo, state, zone):
        self.ip_robot = ip
        self.type_robot = typeo
        self.state_robot = state
        self.zone = zone

    def print_sost(self):
        print(self.ip_robot, self.type_robot, self.state_robot, self.zone)

    def update(self, subject):
        task_zone = list(takewhile(lambda x: x[1]["District"] == "A", subject.task_list_robot))
        if self.zone == "A":
            for i in task_zone:
                self.ip_robot.send(js.dumps(i).encode())
                subject.task_list_robot.remove(i)
        elif self.zone == "B":
            for i in task_zone:
                Robot.ip_robot.send(js.dumps(i).encode())
                subject.task_list_robot.remove(i)

        elif Robot.zone == "Mid":
            for i in subject.task_list_sort:
                Robot.ip_robot.send(js.dumps(i).encode())
                subject.task_list_sort.remove(i)
