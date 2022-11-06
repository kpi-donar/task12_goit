from collections import UserDict
from dateutil import parser
from datetime import *


class Field:
	def __init__(self, value):
		self.value = value


class Name(Field):
	pass

class Phone(Field):
	def __checkValue(x):
		if x.isnumeric():
			return True
		return False

	@property
	def value(self):
		return self._value


	@value.setter
	def value(self, x):
		if Phone.__checkValue(x):
			self._value = x
		elif x.startswith('+'):
			self._value = x[1:]
		else:
			raise ValueError('This phone format is unacceptable!')


class Birthday(Field):

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, x):
		if '-' in x or ':' in x or '/' in x:
			self._value = x
		elif ' ' in x:
			x = x.replace(' ', '-')
			self._value = x
		else:
			raise ValueError('This birthday format is unacceptable!')


class Record():
	def __init__(self, name):
		self.name = Name(name)
		self.phones = []
		self.birthday = None


	def add(self, phone=None, birthday=None):
		if phone:
			self.phones.append(Phone(phone))
		if birthday:
			self.birthday = Birthday(birthday)

	def remove(self, phone):
		if self.phones:
			for ph in self.phones:
				if ph.value == phone:
					self.phones.remove(ph)

	def edit(self, phone_old, phone_new):
		if self.phones:
			for ph in self.phones:
				if ph.value == phone_old:
					self.phones.remove(ph)
		self.phones.append(Phone(phone_new))

	def days_to_birthday(self):
		if self.birthday:
			birth_day = parser.parse(self.birthday.value)
			birth_day = date(year = date.today().year+1, month = birth_day.month, day = birth_day.day)
			return (birth_day - date.today()).days

class AddressBook(UserDict):
	def add_record(self, record):
		self.data[record.name.value] = record

	def search(self, value):
		if self.data.get(value):
			return self.data[value].name.value, [x.value for x in self.data[value].phones]

		for record in self.data.values():
			for phone in record.phones:
				if phone.value == value:
					return record.name.value, [x.value for x in record.phones]

		return "Contact unavailable."

	def search_contacts(self, text):
		if self.data:
			result = []
			for record in self.data.values():
				if text in record.name.value:
					result.append(record)
				for phone in record.phones:
					if text in phone.value:
						result.append(record)
			if result:
				return result
			else:
				return f'The contact(s) with "{text}" such data is not found'
		else:
			return "Adress Book is empty"


	def iterator(self, N):
		book = [self.data[key] for key in self.data]
		n = 0
		while n <= len(book):
			yield book[n: n + N]
			n += N

