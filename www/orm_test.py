from orm import Model, StringField, BooleanField, FloatField, TextField, create_pool, IntegerField, destory_pool
import asyncio


class User(Model):
	__table__ = 'user'
	
	id = IntegerField(primary_key = True)
	name = StringField()



@asyncio.coroutine	
def test():
	yield from create_pool(loop,user = 'root',password = 'zxzx',db = 'orm_test',host = '127.0.0.1')
	u = User(id = 337, name = 'zxlw')
	#yield from u.save()
	yield from u.findAll()
	yield from destory_pool()
	

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()