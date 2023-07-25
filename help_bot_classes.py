from collections import UserDict
from datetime import datetime
import pickle

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
        current_month = current_datetime.month
        birthday = self.birthday.value.replace(year = current_year)
        birthday = birthday if birthday > current_datetime else birthday.replace(year = birthday.year + 1)
        return (birthday - current_datetime).days

    def __str__(self) -> str:
        return "|{:<30}|{:^12}|{:^18}|{:>40}|".format(str(self.name), str(self.birthday), str(self.days_to_birthday()), ', '.join(str(p) for p in self.phones))
    
    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def __init__(self, filename: str):
        UserDict.__init__(self)
        self.filename = filename
        
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"
    
    def show_all_records(self):
        if not len(self):
            return "No contacts"
        return "\n".join([str(i) for i in self.values()])
        
    def search_record_by_name(self, key):
        return self[key]
    
    def search_record(self, key):
        header = "|{:<30}|{:^12}|{:^18}|{:>40}|".format('Name', 'Birthday', 'Days to birthday', 'Phones') + "\n"
        result = ''
        for rec in self.values():
            if key.isdigit():
                found_phones = [str(p) for p in rec.phones if key in str(p)]
                if len(found_phones) > 0:
                    result += str(rec) + "\n"        
            elif key.lower() in str(rec.name).lower():
                result += str(rec) + "\n"
        if result:
            yield header + result
    
    def iterator(self, n):
        header = "|{:<30}|{:^12}|{:^18}|{:>40}|".format('Name', 'Birthday', 'Days to birthday', 'Phones') + "\n"
        result = header
        count = 0
        for rec in self.values():
            result += str(rec) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = header
        if result:
            yield result

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            self.data = pickle.load(file)