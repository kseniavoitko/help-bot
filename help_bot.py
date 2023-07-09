from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, rec):
        has_record = self.get(rec.name.value, 0)
        if has_record:
            has_record.add_phones(rec.phones)
            return "Phone saved"
        else:
            self[rec.name.value] = rec
            return 'Contact saved'
        
    def show_all_records(self):
        if not len(self):
            return "No contacts"
        return "\n".join([str(i) for i in self.values()])
        
    def search_record(self, key):
        return self[key]
    

class Record():
    def __init__(self, name, phones):
        self.name = name
        self.phones = phones

    def __repr__(self):
        return f'{self.name}: {", ".join([str(i) for i in self.phones])}'
    
    def change_phone(self, old, new):
        old_ind = [i.value for i in self.phones].index(old)
        self.phones[old_ind] = new
        return 'Contact changed'
    
    def add_phones(self, phones):
        for phone in phones:
            self.phones.append(phone)

    def remove_phone(self, phone):
        phone_index = [i.value for i in self.phones].index(phone)
        self.phones.pop(phone_index)
        return 'Contact remove'


class Field():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}' 


class Name(Field):
    pass


class Phone(Field):
    pass


addressbook = AddressBook()

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
    return inner


def hello(args):
    return 'How can I help you?'


@input_error
def add(args):   
    name = Name(args[0])
    phones = []
    for phone in args[1:]:
        phones.append(Phone(phone))
    rec = Record(name, phones)
    return addressbook.add_record(rec)


@input_error
def change(args):
    """Get 2 phones to change
    or 1 phone to remove"""
    record = addressbook.search_record(args[0])
    try:
        new_phone = Phone(args[2])
        return record.change_phone(args[1], new_phone)
    except:
        return record.remove_phone(args[1])


@input_error
def phone(args):
    return addressbook.search_record(args[0])


def show_all(args):
    return addressbook.show_all_records()  


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