from temod.base.attribute import *

import base64

STRING_ESCAPE = str.maketrans({'"':  r'\"'})

class MysqlAttributeException(Exception):
	"""docstring for MysqlAttributeException"""
	def __init__(self, *args, **kwargs):
		super(MysqlAttributeException, self).__init__(*args, **kwargs)

class MysqlAttributesTranslator(object):
	"""docstring for MysqlAttributesTranslator"""

	def translate(attribute):
		if attribute.value is None:
			return "null"
		if type(attribute) is StringAttribute:
			return MysqlAttributesTranslator.translateString(attribute)
		elif type(attribute) is IntegerAttribute:
			return MysqlAttributesTranslator.translateInteger(attribute)
		elif type(attribute) is RealAttribute:
			return MysqlAttributesTranslator.translateReal(attribute)
		elif type(attribute) is BooleanAttribute:
			return MysqlAttributesTranslator.translateBool(attribute)
		elif type(attribute) is DateAttribute:
			return MysqlAttributesTranslator.translateDate(attribute)
		elif type(attribute) is DateTimeAttribute:
			return MysqlAttributesTranslator.translateDatetime(attribute)
		elif type(attribute) is UUID4Attribute:
			return MysqlAttributesTranslator.translateString(attribute)
		elif type(attribute) is UTF8BASE64Attribute:
			return MysqlAttributesTranslator.translateBase64UTF8(attribute)
		elif type(attribute) is RangeAttribute:
			return MysqlAttributesTranslator.translateInteger(attribute)
		else:
			raise MysqlAttributeException(f"Can't translate attribute of type {type(attribute).__name__}")

	####################################
	# BASIC TRANSLATORS
	####################################

	def translateString(attribute):
		return f'"{attribute.value.translate(STRING_ESCAPE)}"'

	def translateInteger(attribute):
		return str(attribute.value)

	def translateReal(attribute):
		return str(attribute.value)

	def translateBool(attribute):
		if attribute.value is True:
			return "1"
		elif attribute.value is False:
			return "0"
		raise MysqlAttributeException(f"Can't translate value {attribute.value} for boolean attribute")

	def translateDate(attribute):
		return f'"{attribute.value.strftime("%Y-%m-%d")}"'

	def translateDatetime(attribute):
		return f'"{attribute.value.strftime("%Y-%m-%d %H:%M:%S")}"'

	def translateBase64UTF8(attribute):
		return f'"{base64.b64encode(attribute.value.encode()).decode("utf-8")}"'

		