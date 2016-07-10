from django import template

register = template.Library()


@register.filter(name="getDictVal")
def getDictVal(dictionary, keyVar):
	return dictionary[keyVar]