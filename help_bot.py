from help_bot_classes import AddressBook, Name, Phone, Record, Birthday, PhoneError, BirthdayError

address_book = AddressBook()

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
        except ValueError:
            if func.__name__ == 'change':
                return "Contact doesn't exist"
            else:
                return 'Wrong parameters'
        except PhoneError:
            return 'Phone must contain 10-12 numbers'
        except BirthdayError:
            return 'Birthday format is dd.mm.yyyy'
        except:
            return 'Wrong parameters'
    return inner


def hello(args):
    return 'How can I help you?'


@input_error
def add(args):   
    name = Name(args[0])
    phone = None
    birthday = None
    for a in args[1:]:     
        if a.isdigit():
            phone = Phone(a)   
        else:     
            birthday = Birthday(a)
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, birthday, phone)
    return address_book.add_record(rec)


@input_error
def change(args):
    """Get 2 phones to change
    or 1 phone to remove"""
    record = address_book.search_record(args[0])
    try:
        new_phone = Phone(args[2])
        return record.change_phone(args[1], new_phone)
    except:
        return record.remove_phone(args[1])


@input_error
def phone(args):
    return address_book.search_record(args[0])


@input_error
def show_all(args):   
    page = 0
    result = 'No contacts'
    for rec in address_book.iterator(int(args[0]) if len(args) else 5): 
        page += 1
        print(f"page {page}")
        print(rec)   
        result = 'END'  

    return result   


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