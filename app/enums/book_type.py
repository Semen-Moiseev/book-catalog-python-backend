from enum import Enum

class BookType(str, Enum):
	GRAPHIC = "graphic"
	DIGITAL = "digital"
	PRINTED = "print"