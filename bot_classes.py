from collections import UserDict
from datetime import datetime, date, timedelta
from collections import defaultdict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name can't be empty")
        super().__init__(value)

    def __str__(self):
        return super().__str__()


class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10 or not value.isdigit():  # 10 digits check
            raise ValueError("Phone must consist of 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, r"%d.%m.%Y").date() if value else None
            super().__init__(value)
        except:
            raise ValueError(f"The value of birthday must be a 'DD.MM.YYYY' date")

    def __str__(self):
        res = (
            datetime.strftime(self.value, r"%d.%m.%Y") if self.value else None.__str__()
        )
        return res

    def __repr__(self) -> str:
        res = (
            datetime.strftime(self.value, r"%d.%m.%Y")
            if self.value
            else None.__repr__()
        )
        return self.__str__()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday: Birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in map(str, self.phones):
            self.phones = [p for p in self.phones if p.value != phone]
        else:
            raise KeyError(f"Phone {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise KeyError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        if phone in map(str, self.phones):
            return phone
        else:
            raise KeyError(f"Phone {phone} not found")

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: [{', '.join(p.value for p in self.phones)}]"

    def __repr__(self):
        return self.__str__()


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        for record in self.data.keys():
            if record == name:
                return self.data[record]
        raise KeyError("Name not found")

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            return
        raise KeyError("Name not found")

    def change_phone(self, name, old_phone, new_phone):
        if not name in self.keys():
            raise KeyError(f"Name {name} not found")

        self[name].edit_phone(old_phone, new_phone)

    def get_birthdays_per_week(self):
        """
        Функція отримує на вхід список users і виводить у консоль (за допомогою
        print) список користувачів, яких потрібно привітати по днях найближчім
        тижнем.
        Наприклад:

        {"name": "Bill Gates", "birthday": date(1955, 10, 28)}

        Дні тижня сортуються
        """
        today = date.today()
        # today = date(2023, 12, 5)  # перевіримо як працює в понеділок 4-12-2023

        # if today is Monday - move the start_date 2 days earlier to check the weekend
        if today.weekday() == 0:
            start_day = today - timedelta(days=2)
        elif today.weekday() == 6:
            start_day = today - timedelta(days=1)
        else:
            start_day = today

        # debug
        # print(
        #     f"today = {today.strftime('%a %d.%m.%Y')}, start_day = {start_day.strftime('%a %d.%m.%Y')}"
        # )

        birthdays_week = defaultdict(list)
        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # for u in users:
        for u in self.values():
            if not u.birthday.value:
                continue
            name: str = u.name.value
            birthday: date = u.birthday.value
            birthday_this_year = birthday.replace(year=start_day.year)
            if birthday_this_year < start_day:
                birthday_this_year = birthday_this_year.replace(
                    year=birthday_this_year.year + 1
                )
            weekend_add = (birthday_this_year.weekday() - 4) * (
                birthday_this_year.weekday() > 4
            )
            delta_days = (birthday_this_year - start_day).days + weekend_add

            if delta_days < 7:
                # debug
                # print(name, birthday, birthday_this_year.strftime("%A"))

                if birthday_this_year.weekday() < 5:  # skip Sun, Sat
                    birthdays_week[birthday_this_year.weekday()].append(name)
                else:
                    birthdays_week[0].append(name)  # move Sun, Sat to Mon

        start_week_day = 0
        # Згідно умови Тиждень починається з понеділка, тому по замовчуванню сортуємо з Понеділка
        # Але зручніше відсортувати дні так, щоб першим був сьогоднішній день тижня, а останнім - вчорашній
        # для цього потрібно задати start_week_day = start_day.weekday()
        # start_week_day = start_day.weekday()
        birthdays_week = dict(
            sorted(
                birthdays_week.items(),
                key=lambda key: (key[0] < start_week_day) * 7 + key[0] - start_week_day,
            )
        )

        birthday_list = ""
        for u in birthdays_week:
            # print(f"{weekdays[u]}: {', '.join(birthdays_week[u])}")
            birthday_list += f"{weekdays[u]}: {', '.join(birthdays_week[u])}\n"
        return birthday_list.removesuffix("\n")
