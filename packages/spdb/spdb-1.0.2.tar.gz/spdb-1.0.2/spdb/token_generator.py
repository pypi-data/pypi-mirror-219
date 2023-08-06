from spdb import generator_utils


class TokenGenerator:
	def __init__(self, code):
		self.code = code


	def gen(self, type: str, ID: str, key: str):
		return f'{self.code}.t.{type}.{ID}:{generator_utils.sha256(ID+generator_utils.sha256(key))}_{generator_utils.sha256(generator_utils.sha256(key)+ID+generator_utils.random_sha256())}'

	@staticmethod
	def parseToken(token: str):
		return {
			'code': token.split('.')[0],
			'type': token.split('.')[2],
			'ID': token.split('.')[3].split(':')[0],
			'owner_hash': token.split('.')[3].split(':')[1].split('_')[0],
			'token_hash': token.split('.')[3].split(':')[1].split('_')[1]
		}