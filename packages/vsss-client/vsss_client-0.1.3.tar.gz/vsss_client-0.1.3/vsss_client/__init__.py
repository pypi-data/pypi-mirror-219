
import socket
import configparser
import os

from enum import Enum
from typing import List

from vsss_client import packet_pb2 as packet
from vsss_client import command_pb2 as command

class Team(Enum):
    BLUE = False
    YELLOW = True

class Command:
    def __init__(self, team: Team, id: int, wheel_left: int, wheel_right: int):
        self.team = team
        self.id = id
        self.wheel_left = wheel_left
        self.wheel_right = wheel_right

    def to_proto(self):
        cmd = command.Command()
        cmd.id = self.id
        cmd.yellowteam = self.team.value
        cmd.wheel_left = self.wheel_left
        cmd.wheel_right = self.wheel_right
        return cmd

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class FIRASim(metaclass=SingletonMeta):
    def __init__(self, config_path: str = None):
        config = configparser.ConfigParser()
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

        print(config_path)
        config.read(config_path)
        
        self.vision_address = str(config['FIRA']['vision_address'])
        self.vision_port = int(config['FIRA']['vision_port'])
        self.command_address = str(config['FIRA']['command_address'])
        self.command_port = int(config['FIRA']['command_port'])

        self.vision_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.vision_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.vision_sock.bind((self.vision_address, self.vision_port))

    def receive(self):
        data, addr = self.vision_sock.recvfrom(2048)
        return data
    
    def send(self, package):
        self.command_sock.sendto(package, (self.address, self.command_port))

    def close(self):
        self.vision_sock.close()
        # self.command_sock.close()

    def env(self):
        data = self.receive()
        env = packet.Environment()
        env.ParseFromString(data)
        return env
    
    def frame(self):
        return self.env().frame
    
    def ball(self):
        return self.frame().ball
    
    def robots(self):
        return self.frame().robots_blue
    
    def robot(self, team: Team, id: int):
        if team:
            return self.frame().robots_blue[id]
        else:
            return self.frame().robots_yellow[id]
        
    def ball(self):
        return self.frame().ball 
    
    def send_command(self, cmds: List[Command]):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.command_address, self.command_port))

        robot_cmd = command.Commands()

        for cmd in cmds:
            robot_cmd.robot_commands.append(cmd.to_proto())

        package = packet.Packet()
        package.cmd.CopyFrom(robot_cmd)

        sock.send(package.SerializeToString())
        sock.close()
            
# class Referee(metaclass=SingletonMeta):
# class SSLVision(metaclass=SingletonMeta):