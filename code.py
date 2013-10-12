import web
from web import form
import time
import datetime
import os.path, sys

sys.path.append(os.path.dirname(__file__))
import model

render = web.template.render('/home/ciaran/Documents/Dropbox/web_design/active/gone/templates/')

urls = (
    "/", "hello",
    "/add", "add",
    "/edit", "edit",
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
        pass
    
    

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
            
        
class list_posts(BaseController):
    def GET(self):
        i = web.input(page=1)
        posts = db.select('posts',limit=4, order=" id DESC ")
        page_content =  render.list_posts(posts)
        return self.render_page(page_content)
      
class article(BaseController):
    def GET(self):
        i = web.input(article_id=1)
        article_id = i.article_id
        post = model.PostModel.load(article_id)
        page_content = render.article(post)
        return self.render_page(page_content)
    

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

application = web.application(urls, globals()).wsgifunc()
