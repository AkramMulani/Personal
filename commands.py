import csv

import pyautogui


class Commands:
    def __init__(self):
        self.commands = dict()
        self.load_commands()

    def load_commands(self) -> dict:
        try:
            with open("commands.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        command_id, command_name, command_key = row
                        self.commands[int(command_id)] = [command_name, command_key]
                    else:
                        print(f'Ignoring data: {row}')
        except FileNotFoundError:
            print('File not found')
        return self.commands

    def _run_command_(self, key: str):
        command = key.split('+')
        pyautogui.hotkey(command[0].strip(), command[1].strip())

    def handle_commands(self, command_id: int):
        try:
            command_name, command_key = self.commands[command_id]
            print(f'Running command for: {command_name}')
            self._run_command_(command_key)
        except KeyError:
            print(f'The command is invalid for id: {command_id}')

    def handle_gui_commands(self, command: str):
        try:
            key = 0
            for index, com in self.commands.items():
                command_name, command_key = com
                if str(command_name).lower().strip() == command.lower().strip():
                    key = index
                    print(f'{key}. {command_key} : {str(command_name).lower()}')
                    break
            self.handle_commands(key)
        except Exception as e:
            print(e)
