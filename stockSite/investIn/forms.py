import calendar
import datetime
from crispy_forms.bootstrap import PrependedText, FormActions, Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Div
from django import forms


class submitForm(forms.Form):
	# creating lists for using list comprehension
	dateList = list(range(1, 32))
	monthList = calendar.month_abbr[1:]
	yearList = list(reversed(range(1776, datetime.datetime.now().year + 1)))

	# building tuples using appropriate lists using list comprehension
	DATE_CHOICES = tuple((str(element), str(element)) for element in dateList)
	MONTH_CHOICES = tuple((str(element), str(element)) for element in monthList)
	YEAR_CHOICES = tuple((str(element), str(element)) for element in yearList)

	ticker = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. AAPL or Sbux'}))
	date = forms.ChoiceField(choices=DATE_CHOICES, required=True, label='dates', initial=datetime.datetime.now().day)
	month = forms.ChoiceField(choices=MONTH_CHOICES, required=True, label='months',
					  initial=calendar.month_abbr[datetime.datetime.now().month])
	year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label='years', initial=datetime.datetime.now().year)

	def __init__(self, *args, **kwargs):
		super(submitForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-inline'
		self.helper.form_method = 'post'
		self.helper.form_action = ""
		self.helper.form_show_labels = False
		self.helper.layout = Layout(
			Div('submit', css_class="col-md-6 col-lg-offset-4"),
			PrependedText('ticker', 'Ticker Symbol&nbsp', autocomplete='off'),
			HTML("&nbsp&nbsp&nbsp&nbsp&nbsp"),
			FormActions(
				Submit('submit', 'Submit', css_class="btn btn-success")
			),
			HTML("<br><br>"),
			Div('month', 'date', 'year', css_class="col-md-8 col-md-offset-2")
		)


class doubleStockForm(forms.Form):
	ticker1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Stock 1'}))
	ticker2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Stock 2'}))

	def __init__(self, *args, **kwargs):
		super(doubleStockForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-inline'
		self.helper.form_method = 'post'
		self.helper.form_action = ""
		self.helper.form_show_labels = False
		self.helper.layout = Layout(
			HTML("<br><br><br>"),
			Field('ticker1', 'Stock 1&nbsp', autocomplete='off'),
			HTML("<br><br>"),
			Field('ticker2', 'Stock 2&nbsp', autocomplete='off'),
			HTML("&nbsp&nbsp&nbsp&nbsp&nbsp"),
			HTML("<br><br><br>"),
			FormActions(
				Submit('submit', 'Submit', css_class="btn btn-success col-md-offset-8")
			),
		)
