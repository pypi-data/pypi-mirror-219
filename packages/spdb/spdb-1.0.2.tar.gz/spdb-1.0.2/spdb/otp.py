import pyotp
import qrcode
from spdb import generator_utils


class OTP:
	def __init__(self, token: str=None):
		self.token = token

		if self.token is None:
			self.token = TOTP.generate_token()

	@staticmethod
	def generate_token() -> str:
		return generator_utils.b32encode(generator_utils.random_text(length=8) + generator_utils.random_b32())


	def now(self):
		return pyotp.TOTP(self.token).now()


	def at(self, index: int):
		return pyotp.HOTP(self.token).at(index)


	def time_verify(self, code: str):
		return pyotp.TOTP(self.token).verify(code)


	def counter_verify(self, index: int, code: str):
		return pyotp.HOTP(self.token).verify(index, code)


	def TQR(self, name, app_name='SPDB PyOTP generator'):
		return qrcode.make(pyotp.totp.TOTP(self.token).provisioning_uri(name=name, issuer_name=app_name))


	def HQR(self, name, app_name='SPDB PyOTP generator'):
		return qrcode.make(pyotp.hotp.HOTP(self.token).provisioning_uri(name=name, issuer_name=app_name))
