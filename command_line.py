from commands import Commands


commands = Commands()


def menu():
    command = commands.load_commands()
    print('Menu')
    print('********For menu card enter M***********')
    for command_id, command_list in command.items():
        print(f'\t{command_id}. {command_list[0]}')
    print('**********For exit enter -1**************')


def start():
    menu()
    while True:
        try:
            index = int(input('Choice: '))
            if index == -1:
                break
            else:
                commands.handle_commands(index)
        except Exception as e:
            print(e)
            menu()

    print("Thank you for using this... please visit again!!!!!")


def init():
    start()
