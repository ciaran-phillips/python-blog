import web
from fields import Field
from web import form

import time
import datetime

db = web.database(dbn='mysql', user='root', pw='', db='portfolio')

class BaseModel(object):
	_table_name = None
	_model_name = None
	
	
	def __init__(self, **kwargs):
		
		self.fields['id'] = Field('id', None)
		self.update(**kwargs)

	def delete(self,id):
		pass
	
	@classmethod
	def load(cls, id):
		# TODO - check whether a result was returned before accessing index
		result = db.select(cls._table_name, where = " id = $id ", vars=locals())[0]
		if result:
			instance = cls.get_instance(db_row = result)
		else:
			instance = False
		return instance

	@classmethod
	def load_group(cls, conditions = "", limit = ""):
		pass
	
	
	def save(self):
		value_dict = {}
		for fieldname in self.fields:
			value_dict[fieldname] = self.fields[fieldname].value
		
		if not value_dict['id']:
			result = db.insert(self._table_name, **value_dict)
		else:
			cons = {}
			cons['id'] = value_dict['id']
			del value_dict['id']
			result = db.update(self._table_name , where = ' id = $id ', vars = cons, **value_dict )
		
	@classmethod
	def get_instance(cls, db_row=None, **kwargs):
		if db_row:
			instance = cls(**db_row)
		else:
			instance = cls(kwargs)
		return instance
			
	
	def update(self, **kwargs):
		for fieldname in self.fields:
			if fieldname in kwargs:
				self.fields[fieldname].value = kwargs[fieldname]
		
	def get_form(self):
		field_list = []
		for fieldname in self.fields:
			input_field = self.fields[fieldname].get_form_field()
			field_list.append(input_field)
		model_form_class = form.Form(*field_list)
		model_form = model_form_class()
		return model_form

class PostModel(BaseModel):
	_table_name = 'posts'
	_model_name = 'Posts'
	
	def __init__(self, **kwargs):
		self.fields = {
			'title' : Field('title',label="Title"),
			'article' : Field('article',label="Blog Content", field_type="Textarea"),
			'short_url' : Field('short_url',label="Short URL"),
			'published' : Field('published',value=False, label="Published",field_type="Checkbox"),
			'time_published' : Field('time_published', label= "Time Published"),
			'time_modified' : Field('time_modified', label="Time Modified", field_type="Hidden"),
			'time_created' : Field('time_created', label="Time Created", field_type="Hidden"),
		}
		super(PostModel,self).__init__(**kwargs)
		
	def save(self):
		self.fields['time_modified'].value = time.time()
		if not self.fields['id'].value:
			self.fields['time_created'] = time.time()
		super(PostModel,self).save()
		
	def publish(self):
		pass
	
	def unpublish(self):
		pass


class UserModel:
	
	def delete_user(self):
		pass
		
	def edit_user(self):
		pass
