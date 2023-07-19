from collections import UserDict
from datetime import datetime

class PhoneError(Exception):
    pass


class BirthdayError(Exception):
    pass


class Field():
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self) 


class Name(Field):
    ...


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if 10 <= len(new_value) <= 12:
            self.__value = new_value
        else:
            raise PhoneError 


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime.strptime(new_value, '%d.%m.%Y')
        except:
            raise BirthdayError
        
    def __str__(self) -> str:
        return self.value.strftime('%d.%m.%Y')


class Record():
    def __init__(self, name: Name, birthday: Birthday = None, phone: Phone = None) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)
   
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"
    
    def change_phone(self, old, new):
        old_ind = [i.value for i in self.phones].index(old)
        self.phones[old_ind] = new
        return 'Contact changed'
    
    def remove_phone(self, phone):
        phone_index = [i.value for i in self.phones].index(phone)
        self.phones.pop(phone_index)
        return 'Contact remove'
    
    def days_to_birthday(self):
        current_datetime = datetime.now()
        current_year = current_datetime.year
        birthday = birthday.replace(year = current_year) if birthday.month != 1 else birthday.replace(year = current_year + 1)
        return (birthday - current_datetime).days

    def __str__(self) -> str:
        return f"{self.name} ({self.birthday}): {', '.join(str(p) for p in self.phones)}"
    
    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"
    
    def show_all_records(self):
        if not len(self):
            return "No contacts"
        return "\n".join([str(i) for i in self.values()])
        
    def search_record(self, key):
        return self[key]