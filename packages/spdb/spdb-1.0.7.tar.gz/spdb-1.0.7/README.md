=====================================

# Sassy Python Database(and auth) utils

=====================================


## Requirements

============

- Python 3.7 or higher
- pyotp
- qrcode
- setuptools


## Usage 

=====

	import spdb

### Database

--------
	spdb.Database(path: str)
	spdb.Database.create_tables(tables_names: list[str]) -> None
	spdb.Database.execute(code) -> str
	spdb.Database.read_dict(name: str, data_id: str) -> dict
	spdb.Database.read_object(Class: class, name: str, data_id: str) -> Class
	spdb.Database.write_dict(name: str, data_id: str, data: dict) -> None
	spdb.Database.write_object(name: str, object_id: str, object: Class) -> None

	Static:
		spdb.Database.object_to_dict(object: Class) -> dict
		spdb.Database.dict_to_object(Class: class, Dict: dict) -> Class

### TOTP - HOTP

-----------
	spdb.OTP(token: str=None, app_name: str=None)
	spdb.OTP.now() -> str
	stdb.OTP.at(index: int) -> str
	stdb.OTP.time_verify(code: str) -> bool
	stdb.OTP.counter_verify(index: int, code: str) -> bool
	stdb.OTP.TQR(name: str) ->
	stdb.OTP.HQR(name: str) ->

	Static:
		stdb.OTP.generate_token() -> str

### Token Generator

---------------
	stdb.TokenGenerator(code: str)
	stdb.TokenGenerator.gen(type: str, ID: str, key: str) -> str

	Static:
		stdb.TokenGenerator.parse_token(token: str) -> dict

### Text Validator

--------------
	stdb.TextValidator(min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+')
	stdb.TextValidator.check(text: str) -> bool

### Utils

-----
	stdb.utils.sha256(text: str) -> str
	stdb.utils.b32encode(text: str) -> str
	stdb.utils.random_text(length: int=None) -> str
	stdb.utils.random_sha256() -> str
	stdb.utils.random_b32 -> str