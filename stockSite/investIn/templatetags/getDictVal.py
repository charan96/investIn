from django import template

register = template.Library()


@register.filter(name="getDictVal")
def getDictVal(dictionary, keyVar):
	return dictionary[keyVar]


@register.filter(name="addStrings")
def addStrings(string1, string2):
	return str(string1) + "," + str(string2)


@register.filter(name="getDoubleDictVal")
def getDoubleDictVal(dictionary, keyVar):
	key1, key2 = keyVar.split(",")
	return dictionary[key1][key2]
