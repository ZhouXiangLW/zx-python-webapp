' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coreweb import get, post

from models import User, Comment, Blog, next_id
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, Page

from config import configs

from aiohttp import web

from urllib import request

import markdown2

import simplejson

import os

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

class MarkDownFilter(object):

	def __init__(self ,md, *symbols):

		self.symbols = symbols or ['#','>','`','*','+','-','[',']'] 
		self.md = '''%s''' % md;

	def checkMd(self,str):

		return str not in self.symbols


	def Parser(self):
		l = list(filter(self.checkMd, list(self.md)))
		return ''.join(l)

def getSummary(index,details):
	while True:
		try:
			summary = MarkDownFilter(details).Parser().encode()[:index].decode()
		except:
			index = index + 1
		else:
			summary = summary + '...'
			break
	return summary


def check_admin(request):
	print(request.__user__)
	if request.__user__ is None or not request.__user__.admin:
		raise APIPermissionError('您没有权限')
		
def get_page_index(page_str):
	p = 1
	try:
		p = int(page_str)
	except ValueError as e:
		pass
	if p < 1:
		p = 1
	return p
	
def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

def user2cookie(user, max_age):
	'''
	Generate cookie by user
	'''
	#build cookie string by: id-expires-sha1
	expires = str(int(time.time() + max_age))
	s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
	L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(L)
	
async def cookie2user(cookie_str):
	'''
	Parse cookie and load user if cookie is vaild.
	'''
	if not cookie_str:
		return None
	try:
		L = cookie_str.split('-')
		if len(L) != 3:
			return None
		uid, expires, sha1 = L
		if int(expires) < time.time():
			return None
		user = await User.find(uid)
		if user is None:
			return None
		s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
		if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
			logging.info('invalid sha1')
			return None
		user.passwd = '******'
		return user
	except Exception as e:
		logging.info(e)
		return None
	
	



#注册处理函数	
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
async def api_register_user(*, email, name, passwd):
	if not name or not name.strip():
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not passwd or not _RE_SHA1.match(passwd):
		raise APIValueError('passwd')
	users = await User.findAll('email=?', [email])
	if len(users) > 0:
		raise APIError('register:failed','email', 'Email is already in use')
	uid = next_id()
	sha1_passwd = '%s:%s' % (uid, passwd)
	user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravater.com/avater/%s?d=mm&s=120' %hashlib.md5(email.encode('utf-8')).hexdigest())
	await user.save()
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r



#登陆处理函数	
@post('/api/authenticate')
async def authenticate(request, *, email, passwd):
	if not email:
		raise APIValueError('email','Invalid email')
	if not passwd:
		raise APIValueError('passwd','Invalid password')
	users = await User.findAll('email=?', [email])
	if len(users) == 0:
		raise APIValueError('email','email not exist')
	user = users[0]
	#check passwd
	sha1 = hashlib.sha1()
	sha1.update(user.id.encode('utf-8'))
	sha1.update(b':')
	sha1.update(passwd.encode('utf-8'))
	if user.passwd != sha1.hexdigest():
		raise APIValueError('passwd','Invalid password')
	#authenticate ok, set cookie
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age = 86400, httponly = True)
	user.passwd = '********'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r

#登出处理函数	
@get('/signout')
def signout(request):
	referer = request.headers.get('Referer')
	r = web.HTTPFound(referer or '/')
	r.set_cookie(COOKIE_NAME, '-deleted-', max_age = 0, httponly = True)
	logging.info('user signed out.')
	return r
	
#删除用户函数
@post('/api/users/{id}/delete')
async def api_user_delete(id):
	user = await User.find(id)
	if not user:
		raise APIResourceNotFoundError('用户不存在')
	await User.remove(user)
	return user

#请求编辑日志页面
@get('/manage/blogs/create')
def manage_create_blog():
	return{
		'__template__': 'manage_blog_edit.html',
		'id': '',
		'action': '/api/blogs'
	}
	


#日志更新函数	
@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, content):
	check_admin(request)
	blog = await Blog.find(id)
	if not name or not name.strip():
		raise APIValueError('name', 'name cannot be empty.')
	summary = content[:100] + '...'
	if not summary or not summary.strip():
		raise APIValueError('summary', 'summary cannot be empty.')
	if not content or not content.strip():
		raise APIValueError('content', 'content cannot be empty.')
	blog.name = name.strip()
	blog.summary = summary.strip()
	blog.content = content.strip()
	await blog.update()
	return blog
	
#请求日志详情页面
@get('/blog/{id}')
async def get_blog(id):
	blog = await Blog.find(id)
	html_content = markdown2.markdown(blog.content)
	rd_times = blog.rd_times + 1
	blog.rd_times = rd_times
	await blog.update()
	comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
	 
	for c in comments:
		c.html_content = text2html(c.content)
	return{
		'__template__': 'bs_blog.html',
		'blog': blog,
		'comments':comments,
		'html_content':html_content
	}
	
#日志保存函数
@post('/api/blogs')
async def api_create_blogs(request, *, name, content):
	check_admin(request)
	if not name or not name.strip():
		raise APIValueError('name', 'name connot be empty')
	summary = content[:100] + '...'
	if not summary or not summary.strip():
		raise APIValueError('summary', 'summary connot be empty')
	if not content or not content.strip():
		raise APIValueError('content', 'content connot be empty')
	blog = Blog(id=next_id(), user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
	await blog.save()
	return blog

#日志删除函数
@post('/api/blogs/{id}/delete')
async def api_blog_delete(id):
	blog = await Blog.find(id)
	if not blog:
		raise APIResourceNotFoundError('没有找到博客')
	await Blog.remove(blog)
	return blog
	

#评论保存函数	
@post('/api/blogs/{id}/comments')
async def creat_comments(request, *, content, id):
	if not content or not content.strip():
		raise APIValueError('请输入评论内容')
	comment = Comment(id=next_id(), blog_id=id, user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, content=content)
	await comment.save();
	return comment 

#删除评论函数	
@post('/api/comments/{id}/delete')
async def api_comment_delete(id):
	comment = await Comment.find(id)
	if not comment:
		raise APIResourceNotFoundError('没有找到该挑评论')
	await Comment.remove(comment)
	return comment

#请求日志管理页面
@get('/manage/blogs')
def manage_blogs(*, page=1):
	return{
		'__template__':'manage_blogs.html',
		'page_index':get_page_index(page)
	}
	
#请求评论管理页面
@get('/manage/comments')
def manage_comments(*, page=1):
	return{
		'__template__':'manage_comments.html',
		'page_index':get_page_index(page)
	}
	
#请求用户管理页面
@get('/manage/users')
def manage_users(*, page=1):
	return{
		'__template__':'manage_users.html',
		'page_index':get_page_index(page)
	}
	
	

#以下是开放的api
@get('/api/blogs/{id}')
async def api_get_blog(*, id):
	blog = await Blog.find(id)
	return blog

@get('/api/users')
async def api_get_user(*, page='1'):
	page_index = get_page_index(page)
	num = await User.findNumber(User, 'count(id)')
	p = Page(num, page_index)
	p.totalPage = num // 10 + 1
	users = await User.findAll(orderBy='created_at desc')
	return dict(page=p,users=users)

@get('/api/blogs')
async def api_blogs(*, page='1'):
	page_index = get_page_index(page)
	num = await Blog.findNumber(Blog, 'count(id)')
	p = Page(num, page_index)
	p.totalPage = num // 10 + 1
	if num == 0:
		return dict(page=p, blogs=())
	blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
	return dict(page=p, blogs=blogs)
	
@get('/api/comments')
async def api_comments(*, page='1'):
	page_index = get_page_index(page)
	num = await Comment.findNumber(Comment, 'count(id)')
	p = Page(num, page_index)
	p.totalPage = num // 10 + 1
	if num == 0:
		return dict(page=p, comments=())
	comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
	return dict(page=p, comments=comments)
	
@get('/api/get_bing_photo')
async def api_get_bing_photo(*,callback=''):
	'Get photo from Bing '
	url = 'http://www.bing.com'
	f = request.urlopen(url)
	html = f.read().decode()
	f.close()
	a = html[html.index('/az/hprichbg'):]
	path = a[:a.index('.jpg')+4]
	url = url + path
	data = simplejson.dumps(dict(url=url))
	if callback:
		return callback + '(' + data + ')'
	else:
		return data;

@get('/api/get_qiubai')
async def getQiubai(*,page=1,callback=''):

	url = 'http://www.qiushibaike.com/text/page/' + str(page)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent':user_agent}
	req = request.Request(url,headers = headers)
	res = request.urlopen(req)
	html = res.read().decode()
	pattern = re.compile('<div class="content">(.*?)</div>',re.S)
	items = re.findall(pattern,html)

	data = simplejson.dumps(dict(items=items), ensure_ascii=False)
	if callback:
		return callback + '(' + data + ')'
	else:
		return data;


#以下是新首页测试内容
@get('/')
async def get_bs_index():
	page_index = get_page_index(1)
	num = await Blog.findNumber(Blog, 'count(id)')
	page = Page(num, page_index, page_size=3)
	blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
	for blog in blogs:
		blog.comment_count = await Comment.findNumber(Comment, 'count(id)', 'blog_id=?', [blog.id])
		if len(blog.name) > 17:
			blog.shortname = blog.name[:17] + '...'
		else:
			blog.shortname = blog.name
		blog.summary = getSummary(270,blog.content)	
	return{
		'__template__': 'bs-index.html',
		'blogs': blogs,
		'page':page
	}

@get('/bs/blogs')
async def get_bs_blogs(*, page=1):
	page_index = get_page_index(page)
	num = await Blog.findNumber(Blog, 'count(id)')
	page = Page(num, page_index, page_size=5)
	blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
	totalPage = num//5 + 1
	for blog in blogs:
		blog.comment_count = await Comment.findNumber(Comment, 'count(id)', 'blog_id=?', [blog.id])
		blog.summary = getSummary(500,blog.content)
	return{
		'__template__': 'bs_blogs.html',
		'totalPage': totalPage,
		'blogs': blogs,
		'page':page
	}

#请求日志管理页面
@get('/bs/manage/blogs')
def manage_bs_blogs(*, page=1):
	return{
		'__template__':'bs_manage_blogs.html',
		'page_index':get_page_index(page)
	}
#请求评论管理页面
@get('/bs/manage/comments')
def manage_comments(*, page=1):
	return{
		'__template__':'bs_manage_comments.html',
		'page_index':get_page_index(page)
	}
#请求用户管理页面
@get('/bs/manage/users')
def manage_users(*, page=1):
	return{
		'__template__':'bs_manage_users.html',
		'page_index':get_page_index(page)
	}

#请求重新编辑日志页面
@get('/bs/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'bs_manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

 #请求编辑日志页面
@get('/bs/manage/blogs/create')
def manage_create_blog():
	return{
		'__template__': 'bs_manage_blog_edit.html',
		'id': '',
		'action': '/api/blogs'
	}

@get('/about')
def get_obout_page(request):

	return {
	    '__template__':'aboutme.html'
	}

	
@post('/upload')
async def upload_image(request):
	data = request.__data__
	filename = next_id()[10:20] + '.jpg'
	path = os.path.abspath('.') + '/static/img/' + filename
	img = data['file'].file
	content = img.read()
	with open(path, 'wb') as f:
		f.write(content)
	return '/static/img/' + filename