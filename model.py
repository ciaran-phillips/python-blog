import web
from fields import Field


db = web.database(dbn='mysql', user='root', pw='', db='portfolio')

class BaseModel(object):
	_table_name = None
	_model_name = None
	
	_fields = []
	
	def __init__(self, **kwargs):
		for field in self.fields:
			if field.name in kwargs:
				field.value = kwargs[field.name]

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
	
	@classmethod
	def get_instance(cls, db_row=None, **kwargs):
		if db_row:
			instance = cls(**db_row)
		else:
			instance = cls(kwargs)
		return instance
			
		
	
	def save(self):
		

class PostModel(BaseModel):
	_table_name = 'posts'
	_model_name = 'Posts'
	
	def __init__(self, **kwargs):
		self.fields = [
			Field('title',''),
			Field('id', None),
			Field('article',''),
			Field('short_url',''),
			Field('published',False),
			Field('time_published',''),
			Field('time_modified',''),
			Field('time_created','')
		]
		super(PostModel,self).__init__(**kwargs)
		
		
	def publish(self):
		pass
	
	def unpublish(self):
		pass
		
class UserModel:
	
	def delete_user(self):
		pass
		
	def edit_user(self):
		pass
