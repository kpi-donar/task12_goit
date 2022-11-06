from class_rep import AddressBook, Record
import pickle
import os


def creation_adressbook():
	global CONTACTS
	if os.path.exists('AdressBook.pickle'):
		with open('AdressBook.pickle', 'rb') as f:
			CONTACTS = pickle.load(f)
	else:
		CONTACTS = AddressBook()


def input_error(handler):
	def wrapper(*args, **kargs):
		try:
			return handler(*args, **kargs)
		except KeyError:
			return 'Enter user name'
		except ValueError:
			return 'Give me name and phone please'
		except IndexError:
			return 'Try again'
		except TypeError:
			return 'Give me name and phone please'
	return wrapper


def hello():
	return  "How can I help you?"

@input_error
def quit_func():
	if CONTACTS:
		with open('AdressBook.pickle', 'wb') as f:
			pickle.dump(CONTACTS, f)
	return 'Good bye!'

@input_error
def show():
	contact_book = {}
	for key, ph in CONTACTS.items():
		if ph.phones or ph.birthday:
			contact_phone = []
			for phone in ph.phones:
				contact_phone.append(phone.value)
			if ph.birthday:
				contact_phone.append(ph.birthday.value)
			contact_book[key] = contact_phone
		else:
			contact_book[key] = key
	return contact_book


@input_error
def add_phone_func(data):
	name, phones, birthday = create_data(data)
	if name in CONTACTS:
		if phones:
			for phone in phones:
				CONTACTS[name].add_phone(phone)
			return "Phone added!"
	else:
		record = Record(name)	
		if phones:
			for phone in phones:
				record.add_phone(phone)
		CONTACTS.add_record(record)
		return "Contact added!"


@input_error
def add_birthday_func(data):
	name, phones, birthday = create_data(data)
	if name in CONTACTS:
		if birthday:
			CONTACTS[name].add_birthday(birthday)
			return "birthday added!"
	else:
		record = Record(name)	
		if birthday:
			record.add_birthday(birthday)
		CONTACTS.add_record(record)
		return "Contact added!"

@input_error
def edit_phone(data):
	change_data = data.split()
	phone_old = change_data[0]
	phone_new = change_data[1]
	for key, record in CONTACTS.items():
		for phone in record.phones:
			if phone_old == phone.value:
				record.edit(phone_old, phone_new)
				CONTACTS[key] = record
	return f"{phone_old} --> {phone_new}: Changed!"

@input_error
def remove_phone(phone_to_delete):
	phone_to_delete = phone_to_delete.strip()
	for key, record in CONTACTS.items():
		for phone in record.phones:
			if phone_to_delete == phone.value:
				record.remove(phone.value)
				CONTACTS[key] = record
	return f"{phone_to_delete}: Deleted!"


@input_error
def edit_birthday(data):
	change_data = data.split()
	name = change_data[0]
	birthday_new = change_data[1]
	if name in CONTACTS:
		record = CONTACTS[name]
		record.edit_birthday(name, birthday_new)
		CONTACTS[name] = record
		return f"{name}: new date --> {birthday_new}: birthday Changed!"
	return f'{name} is not in AddressBook'

@input_error
def remove_birthday(name):
	name = name.strip()
	if name in CONTACTS:
		record = CONTACTS[name]
		record.remove_birthday(name)
		return f"{name}: birthday Deleted!"
	return f'{name} is not in AddressBook'


@input_error
def search_func(data):

	return CONTACTS.search(data.strip())

@input_error
def search_contacts_func(data):

	return CONTACTS.search_contacts(data.strip())


@input_error
def days_to_birthday(data):
	contact = CONTACTS[data.strip()]
	if contact.birthday:
		return contact.days_to_birthday()



def iterator_func(N):
	for i in CONTACTS.iterator(N.strip()):
		yield i


def change_input(user_input):
	new_input = user_input
	data = ''
	for key in COMMANDS:
		if user_input.lower().startswith(key):
			new_input = key
			data = user_input[len(new_input):]
			break
	if data:
		return reaction_func(new_input)(data)
	return reaction_func(new_input)()


def reaction_func(reaction):
	return COMMANDS.get(reaction, break_func)


def break_func():
    return 'Wrong enter.'


def create_data(data):
	new_data = data.split()
	name = new_data[0]
	phones = []
	birthday = ''
	for value in new_data[1:]:
		if value.isnumeric():
			phones.append(value)
		else:
			birthday += value	
	return name, phones, birthday

COMMANDS = {
'hello': hello, 
'add phone': add_phone_func, 
'add birthday': add_birthday_func,
'edit phone': edit_phone,
'remove phone' : remove_phone,
'edit birthday': edit_birthday,
'remove birthday' : remove_birthday,
'search': search_func, 
'show all': show,
'birthday' : days_to_birthday,
'good bye': quit_func, 
'close': quit_func, 
'exit': quit_func,
'iterator' : iterator_func,
'find contact': search_contacts_func
}

@input_error
def main():
	while True:
		user_input = input('Enter command for bot: ')
		result = change_input(user_input)
		print(result)
		if result == 'Good bye!':
			break


if __name__ == '__main__':
	creation_adressbook()
	main()