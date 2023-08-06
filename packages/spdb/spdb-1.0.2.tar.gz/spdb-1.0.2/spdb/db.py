import sqlite3
import json


class Database:
	def __init__(self, path):
		self.path = path


	def create_tables(self, tables_names):
		for table_name in tables_names:
			self.execute(f'create table if not exists {table_name}(id text, data text)')


	def execute(self, code: str) -> str:
		database = sqlite3.connect(self.path, isolation_level=None)
		cursor = database.cursor()
		cursor.execute(code)
		result = cursor.fetchall()
		database.commit()
		database.close()
		return result


	@staticmethod
	def object_to_dict(object) -> dict:
		return json.loads(json.dumps(object.__dict__))


	@staticmethod
	def dict_to_object(Class, Dict):
		return Class(**Dict)


	def read_dict(self, name, data_id) -> dict:
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			return {}
		return json.loads(objects[0][0])


	def read_object(self, Class, name, object_id):
		return Database.dict_to_object(Class, self.read_dict(name, object_id))


	def write_dict(self, name, data_id, data):
		data = json.dumps(data)
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			self.execute(f'insert into {name}(id, data) values(\'{data_id}\', \'{data}\')')
		else:
			self.execute(f'update {name} set data = \'{data}\' where id = \'{data_id}\'')


	def write_object(self, name, object_id, object):
		self.write_dict(name, object_id, Database.object_to_dict(object))
