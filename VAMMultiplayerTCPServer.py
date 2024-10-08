# VAM Multiplayer TCP Server
# vamrobotics (7-28-2021)
# https://github.com/vamrobot/vammultiplayer
# vammultipl (06-10-2024)
# https://github.com/vammultipl/vammultiplayer_revamped

import socket
import threading
import sys
import struct
import time
import logging
from VamMultiplayerTCP import VAMMultiplayerTCP

class VAMMultiplayerServer(VAMMultiplayerTCP):
    def __init__(self, host, port):
        super().__init__(host, port)

    def load_allowlist(self, filename):
        allowlist = set()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        allowlist.add(parts[0])
        except FileNotFoundError:
            logging.error(f"Allowlist file {filename} not found.")
        return allowlist


    def on_user_change(self):
        filename = f'current_players_port{self.port}.txt'
        timestamp = int(time.time())

        def format_user_data(ip_port, player_name):
            base_info = f"{ip_port}:{player_name.decode()}"
            scene_name = self.usersScenes.get(ip_port)
            return f"{base_info}:{scene_name}" if scene_name else base_info

        user_data = [format_user_data(ip_port, player_name) for ip_port, player_name in self.users.items()]
        state = ",".join(user_data)

        with open(filename, 'a') as f:
            f.write(f"{timestamp};{state}\n")

def main():
    host = "0.0.0.0"
    port = 8888  # Default port
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Check for command line arguments for port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logging.error("Invalid port number. Using default port 8888.")

    logging.info("VAM Multiplayer Server running:")
    logging.info(f"IP: {host}")
    logging.info(f"Port: {port}")
    VAMMultiplayerServer(host, port).listen()

if __name__ == "__main__":
    main()
