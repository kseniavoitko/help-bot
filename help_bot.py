contacts = {}

def input_error(func):
    def inner(args):
        try:
            result = func(args)
            return result
        except IndexError:
            if func.__name__ == 'add' or func.__name__ == 'change':
                return 'Give me name and phone please'
            elif func.__name__ == 'phone':
                return 'Give me phone please'
            else:
                return 'Wrong parameters!'
        except KeyError:
            if func.__name__ == 'phone' or func.__name__ == 'change':
                return "Contact doesn't exist"
    return inner


def hello(args):
    return 'How can I help you?'


@input_error
def add(args):
    if contacts.get(args[0], 0):
        return "Сontact already exists"
    else:
        contacts[args[0]] = args[1]
        return 'Contact saved'


@input_error
def change(args):
    if contacts[args[0]]:
        contacts[args[0]] = args[1]
        return 'Contact changed'


@input_error
def phone(args):
    return contacts[args[0]]


def show_all(args):
    if not len(contacts):
        return "No contacts"
    for key, value in contacts.items():
        return key, value     


def no_command(args):
    return 'Unknown command'


COMMANDS = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show all': show_all,
    'good bye': exit,
    'close': exit,
    'exit': exit
}

def parser(text: str) -> tuple[callable, list[str]]:
    for key in COMMANDS:
        if text.lower().startswith(key):
            return COMMANDS[key], text.replace(key, '').strip().split()  
    return no_command, ''     


def main():
    while True:
        user_input = input('>>>')
        command, data = parser(user_input)
        if command == exit:
            print('Buy!')
            break
        result = command(data)
        print(result)


if __name__ == '__main__':
    main()