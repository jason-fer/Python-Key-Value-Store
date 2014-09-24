import string

MAX_KEY_LENGTH = 128
MAX_VALUE_LENGTH = 2048
DISALLOWED_CHARS = ('[',']')

class InputKeyError(Exception):
	def __init__(self, key, error_msg):
		self.key = key
		self.error_msg = error_msg
	
	def __str__(self):
		return 'Error in key ("%s"): %s' % (self.key, self.error_msg)

class InputValueError(Exception):
	def __init__(self, value, error_msg):
		self.value = value
		self.error_msg = error_msg
	
	def __str__(self):
		return 'Error in value ("%s"): %s' % (self.value, self.error_msg)

def not_empty(mystring, ErrorClass):
	if len(mystring) == 0:
		raise ErrorClass('', 'Empty string as input.')

def is_printable(mystring, ErrorClass):
	for c in mystring:
		if c not in string.printable:
			raise ErrorClass('', 'Contains unprintable ASCII character.')

def no_invalid_chars(mystring, invalid_chars, ErrorClass):
	for c in mystring:
		if c in invalid_chars:
				raise ErrorClass(mystring, 'Contains disallowed character ' + c)

def not_too_long(mystring, max_length, ErrorClass):
	if len(mystring) > max_length:
		shortened = mystring[:4] + '...' + mystring[-4:]
		raise ErrorClass(shortened, 'Longer than %s chars.' % max_length)

def sanitycheck_key(key):
	not_empty(key, InputKeyError)
	not_too_long(key, MAX_KEY_LENGTH, InputKeyError)
	no_invalid_chars(key, DISALLOWED_CHARS, InputKeyError)
	is_printable(key, InputKeyError)


def sanitycheck_value(value):
	not_empty(value, InputValueError)
	not_too_long(value, MAX_VALUE_LENGTH, InputValueError)
	no_invalid_chars(value, DISALLOWED_CHARS, InputValueError)
	is_printable(value, InputValueError)
