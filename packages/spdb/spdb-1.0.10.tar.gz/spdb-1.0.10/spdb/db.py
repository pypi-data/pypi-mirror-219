import sqlite3
import json


class Database:
	def __init__(self, path: str):
		self.path = path


	def create_tables(self, tables_names: list[str]):
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
		if object is None:
			return {}
		return json.loads(json.dumps(object.__dict__))


	@staticmethod
	def dict_to_object(Class, Dict: dict):
		try:
			return Class(**Dict)
		except TypeError:
			return None


	def read_dict(self, name: str, data_id: str) -> dict:
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			return {}
		return json.loads(objects[0][0])


	def read_object(self, Class, name: str, object_id: str):
		return Database.dict_to_object(Class, self.read_dict(name, object_id))


	def write_dict(self, name: str, data_id: str, data: str):
		data = json.dumps(data)
		objects = self.execute(f'select data from {name} where id = \'{data_id}\'')
		if len(objects) == 0:
			self.execute(f'insert into {name}(id, data) values(\'{data_id}\', \'{data}\')')
		else:
			self.execute(f'update {name} set data = \'{data}\' where id = \'{data_id}\'')


	def write_object(self, name: str, object_id: str, object: str):
		self.write_dict(name, object_id, Database.object_to_dict(object))


	def delete_object(self, name: str, data_id: str):
		self.execute(f'delete from {name} where id = {data_id}')
