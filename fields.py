from web import form

class Field:
	def __init__(self, name, value=None, field_type="Textbox", label=None):
		if not label:
			self.label = name.title()
		else:
			self.label = label
		self.name = name
		self.value = value
		self.field_type = field_type

	def get_form_field(self):
		field_class = getattr(form, self.field_type)
		form_field = field_class(self.name, value=self.value, description = self.label )
		return form_field
