from collections import UserDict
from datetime import datetime
import json

class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @property
    def value(self):
        return self.some_other_value
    
    @value.setter
    def value(self, new_value):
        self.some_other_value = new_value
    """
    В умові сказано: "setter та getter логіку для атрибутів value спадкоємців Field",
    але я не знаю, навіщо тут в класі Name потрібні зараз сеттери та геттери. І без них все працює наче))
    """


class Phone(Field):
    @property
    def value(self):
        return self.something
    
    @value.setter
    def value(self, new_value):
        try:
            if not isinstance(new_value, str) or not new_value.isdigit() or len(new_value) != 10:
                raise ValueError
            self.something = new_value
        except ValueError:
            print(f"The 's phone number {new_value} is invalid. Phone number must have 10 digits")
            self.something = None


class Birthday(Field):
    @property
    def value(self):
        return self.some_value

    @value.setter
    def value(self, new_value):
        try:
            self.some_value = datetime.strptime(new_value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Wrong birthday format. Enter 'DD-MM-YYYY'")

    # self.some_value = new_value


class Record:
    def __init__(self, name: Name, *phones: Phone, birthday: Birthday=None, **kwargs) -> None:
        self.name = name
        self.phones = list()
        if phones:
            for num in phones:
                self.phones.append(num)
        if birthday:
            self.birthday = birthday
    
    def add_phone(self, number: Phone):
        phone_number = Phone(number)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def update_phone(self, old_number, new_number):
        index = self.phones.index(old_number)
        self.phones[index] = new_number

    def delete_phone(self, value):
        for num in self.phones:
            if num == value:
                self.phones.remove(value)
    
    def days_to_birthday(self):
        current_date = datetime.now()
        next_birthday = self.birthday.value.replace(year=current_date.year)
        if current_date.date() == next_birthday.date():
            return f"Today's {self.name.value}'s birthday!"
        elif current_date.date() > next_birthday.date():
            next_birthday = next_birthday.replace(year=current_date.year + 1)
        days_left = (next_birthday - current_date).days
        return days_left

    def to_json(self):
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": self.birthday.value.strftime('%d-%m-%Y') if self.birthday else None
        }

def starting_program():
        ab.read_from_json()
        entry_question = input("Would you like to see all records? Type Y/n + ENTER: ")
        if entry_question.lower().startswith("y"):
            print(ab.iterator())
        else:
            search_question = input("Would you like to search for a contact? Type Y/n + ENTER: ")
            if search_question.lower().startswith("y"):
                search_value = input("Enter info for search: ").lower()
                found_records = ab.find_record(search_value)
                if found_records:
                    print("Found records:")
                    for record in found_records:
                        print(f"Name: {record.name.value}")
                        if record.birthday:
                            birthday_formatted = record.birthday.value.strftime('%d-%m-%Y')
                            print(f"Birthday on: {birthday_formatted}, days to birthday: {record.days_to_birthday()}")
                        if record.phones:
                            valid_phones = [phone.value for phone in record.phones if phone.value is not None]
                            print(f"Phones: {', '.join(valid_phones)}")
                        print('-' * 20)
                else:
                    print("No records found.")
            

class AddressBook(UserDict):
    N = 2  # по замовчуванню поставимо по 2 записи

    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def save_to_json(self):  
        serialized_records = [record.to_json() for record in self.data.values()]
        with open("address_book.json", "w") as file:
            return json.dump(serialized_records, file)
    
    def read_from_json(self):
        with open("address_book.json", "r") as file:
            deserialized_records = json.load(file)
            reconstructed_records = []
            for record_data in json.load(file):
                name = Name(record_data["name"])
                phones = [Phone(phone) for phone in record_data["phones"]]
                birthday = Birthday(record_data["birthday"]) if record_data["birthday"] else None
                record = Record(name, *phones, birthday=birthday)
                reconstructed_records.append(record)
                self.add_record(record)
            return reconstructed_records

    def find_record(self, search_item):
        output = []
        search_item = search_item.lower()

        for record in self.data.values():
            if search_item in record.name.value.lower():
                output.append(record)
            else:
                for phone in record.phones:
                    if search_item in phone.value:
                        output.append(record)       
        return output

    def iterator(self, n=None):
        if n:
            AddressBook.N = n
        return self.__next__()

    def __iter__(self):
        temp_lst = []
        counter = 0

        for var in self.data.values():
            temp_lst.append(var)
            counter += 1
            if counter >= AddressBook.N:
                yield temp_lst, False
                temp_lst.clear()
                counter = 0
        yield temp_lst, True

    def __next__(self):
        generator = self.__iter__()
        page = 1
        end_flag = False
        while not end_flag:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result, end_flag = next(generator)
                    if result:
                        print(f"{'-' * 20} Page {page} {'-' * 20}")
                        page += 1
                        for contact in result:
                            print(f"Name: {contact.name.value}")
                            if contact.birthday:
                                birthday_formatted = contact.birthday.value.strftime('%d-%m-%Y')
                                print(f"Birthday on: {birthday_formatted}, days to birthday: {contact.days_to_birthday()}")
                            if contact.phones:
                                valid_phones = [phone.value for phone in contact.phones if phone.value is not None]
                                print(f"Phones: {', '.join(valid_phones)}")
                            print('-' * 20)
                except StopIteration:
                    # print(f"{'-' * 20} END {'-' * 20}")
                    break
            else:
                break


if __name__ == '__main__':

    # далі починаються мої перевірочні тести
    # name_1 = Name('Bill')
    # phone_1 = Phone('1234567890')
    # phone_2 = Phone('0987654321')
    # birthday_1 = Birthday("19-06-2004")
    # rec_1 = Record(name_1, phone_1, phone_2, birthday=birthday_1)
    ab = AddressBook()
    # ab.add_record(rec_1)
  
    # name_2 = Name('Joe')
    # birthday_2 = Birthday("23-11-1984")
    # rec_2 = Record(name_2, birthday=birthday_2)
    # ab.add_record(rec_2)

    # name_3 = Name('Witney')
    # birthday_3 = Birthday("21-01-1985")
    # phone_Witney_1 = Phone('1029384756')
    # phone_Witney_2 = Phone('0192837465')
    # rec_3 = Record(name_3, phone_Witney_1, phone_Witney_2, birthday=birthday_3)
    # ab.add_record(rec_3)

    # name_4 = Name('James')
    # phone_4_1 = Phone('1230984576')
    # birthday_4 = Birthday("02-09-1982")
    # rec_4 = Record(name_4, phone_4_1, birthday=birthday_4)
    # ab.add_record(rec_4)

    # name_5 = Name('Lincoln')
    # phone_5_1 = Phone('5647382910')
    # birthday_5 = Birthday("02-11-2008")
    # rec_5 = Record(name_5, phone_5_1, birthday=birthday_5)
    # ab.add_record(rec_5)

    starting_program()

    # ab.save_to_json()
    # # print(ab.read_from_json())
