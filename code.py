import web
from web import form
import time
import datetime
import os.path, sys

sys.path.append(os.path.dirname(__file__))
import model

render = web.template.render(os.path.dirname(__file__) + '/templates/')

urls = (
    "/", "hello",
    "/add", "add",
    "/edit", "edit",
    "/edit_category", "edit_category",
    "/list_categories", "list_categories",
    "/edit_user", "edit_user",
    "/list_posts", "list_posts",
    "/article", "article",
)


app = web.application(urls, globals())
db = web.database(dbn='mysql', user='root', pw='', db='portfolio')

class BaseController:
    def __init__(self):
        pass

    def render_page(self, content):
        page = render.base(content)
        return page


class PostController(BaseController):
    model_class = model.PostModel
    
    def __init__(self):
        self.render = web.template.render(os.path.dirname(__file__) + '/templates/posts/')

class UserController(BaseController):
    model_class = model.UserModel
    
    def __init__(self):
        self.render = web.template.render(os.path.dirname(__file__) + '/templates/users/')
    
class CategoryController(BaseController):
    model_class = model.CategoryModel
    
    def __init__(self):
        self.render = web.template.render(os.path.dirname(__file__) + '/templates/categories/')
        
        
class hello(BaseController):
    def GET(self):
        name = 'Bob'
        return render.index(name)
    

add_form_class = form.Form(
            form.Textbox('title'),
            form.Textbox('short_url'),
            form.Textarea('article'),
            form.Checkbox('published'),
            form.Textbox('time_published',
                value = datetime.datetime.today()
            )
        )

class add(BaseController):
    def GET(self):
        add_form = add_form_class()
        form_html = add_form.render()
        page_content = render.add(form_html=form_html)
        return self.render_page(page_content)
        
    def POST(self):
        
        add_form = add_form_class()
        if add_form.validates():
            time_modified = int(
                            time.time()
                        )
            if add_form.d.published:
                published = 1
            else:
                published = 0
            
            new_post = model.PostModel(title = add_form.d.title,
                                article = add_form.d.article,
                                published = published,
                                short_url = add_form.d.short_url,
                                time_published = add_form.d.time_published,
                                time_modified = time_modified)
            
            
            new_post.save()
            form_html = add_form.render()
            page_content =  render.add(form_html=form_html)
            return self.render_page(page_content)

class edit(BaseController):
        
    def GET(self):
        return edit_model(self, model.PostModel)
    
    def POST(self):
        return edit_model(self, model.PostModel, True)
            
        
class list_posts(PostController):
    def GET(self):
        return list_models(self, limit=4, order=" id DESC ")
        
class list_categories(CategoryController):
    def GET(self):
        return list_models(self)
        
class edit_category(BaseController):
    def GET(self):
        return edit_model(self, model.CategoryModel)
    
    def POST(self):
        return edit_model(self, model.CategoryModel, True)
      
class article(PostController):
    def GET(self):
        return view(self)


class edit_user(UserController):
    def GET(self):
        return edit_model(self, model.UserModel)
    
    def POST(self):
        return edit_model(self, model.UserModel, True)
    
def edit_model(controller, model_class, submit = False):
    i = web.input(id=None)
    model_id = i.id
    
    if model_id:
        inst = model_class.load(model_id)
    else:
        inst = model_class()
    model_form = inst.get_form()
    if submit and model_form.validates():
        inst.update(**model_form.d)
        inst.save()
    form_html = model_form.render()
    page_content = render.add(form_html = form_html)
    return controller.render_page(page_content)
    
def list_models(controller, **kwargs):
    model_class = controller.model_class
    models = model_class.load_group(**kwargs)
    page_content = controller.render.list(models)
    return controller.render_page(page_content)

def view(controller):
    i = web.input(id=1)
    model_id = i.id
    model_class = controller.model_class
    inst = model_class.load(model_id)
    page_content = controller.render.view(inst)
    return controller.render_page(page_content)
    
application = web.application(urls, globals()).wsgifunc()
