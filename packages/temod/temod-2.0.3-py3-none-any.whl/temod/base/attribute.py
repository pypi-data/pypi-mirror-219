from datetime import datetime, date
from temod.base.exceptions import *

import traceback
import random
import base64
import uuid

ASCII_ALPHABET =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE16_ALPHABET = "abcdef0123456789"
BASE64_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/="
		
class Attribute(object):
	"""docstring for Attribute"""
	def __init__(self, name, value_type, value=None, is_id=False,is_auto=False,is_nullable=True,default_value=None,force_cast=None,
		owner=None,owner_name=None,owner_type=None,no_check=False):
		super(Attribute, self).__init__()
		self.name = name
		self.is_id = is_id
		self.is_auto = is_auto
		self.no_check = no_check
		self.value_type = value_type
		self.is_nullable = is_nullable
		self.default_value = default_value		
		self.value = value if value is not None else default_value
		if force_cast is not None and self.value is not None:
			try:
				self.value = force_cast(self.value)
			except:
				raise ForceCastError(self,f"Cannot force cast value {self.value}")
		
		self.owner = owner
		self.owner_type = owner_type if not owner_type is None else (type(owner) if self.owner is not None else None)
		self.owner_name = owner_name if not owner_name is None else (owner.name() if self.owner is not None else (
			getattr(self.owner_type,'ENTITY_NAME',self.owner_type.__name__) if self.owner_type is not None else None
		))

	def check_value(self):
		if self.no_check:
			return False
		if not self.is_nullable and self.value is None:
			raise NonNullableError(self,f"Non nullable attribute set to null. ({self.name})")
		if self.value is not None and not issubclass(type(self.value),self.value_type):
			raise WrongTypeError(self,f"Wrong value type {type(self.value).__name__} for {type(self).__name__} (attribute: {self.name})")


class StringAttribute(Attribute):
	"""docstring for StringAttribute"""
	def __init__(self, name, non_empty=False,force_lower_case=False,length=None,max_length=None,min_length=None,**kwargs):
		super(StringAttribute, self).__init__(name,str,**kwargs)
		self.length = length
		self.max_length = max_length if length is None else length
		self.min_length = min_length if length is None else length
		self.non_empty = non_empty
		self.force_lower_case = force_lower_case
		self.check_value()
		if force_lower_case and self.value is not None:
			self.value = self.value.lower()

	def set_value(self,value):
		self.value = value
		self.check_value()
		if self.force_lower_case and self.value is not None:
			self.value = self.value.lower()

	def check_value(self):
		if super(StringAttribute,self).check_value() is False:
			return False
		if self.non_empty and self.value == "":
			raise EmptyStringError(self,"Value of non empty StringAttribute set to null or empty str")
		if self.value is not None and self.max_length is not None:
			if len(self.value) > self.max_length:
				raise OverMaxLengthError(
					self,f"Value of StringAttribute exceeds the max_length allowed. (value: {self.value}, max_length: {self.max_length})"
				)
		if self.value is not None and self.min_length is not None:
			if len(self.value) < self.min_length:
				raise BelowMinLengthError(
					self,f"Value of StringAttribute doesn't comply with the min_length needed. (value: {self.value}, max_length: {self.min_length})"
				)

	def to_scalar(self):
		return self.value

	def generate_random_value(length):
		str_ = ""
		for i in range(length):
			str_ += ASCII_ALPHABET[random.randint(0,len(ASCII_ALPHABET)-1)]
		return str_


class UUID4Attribute(StringAttribute):
	"""docstring for UUID4Attribute"""
	def __init__(self, *args, **kwargs):
		super(UUID4Attribute, self).__init__(*args, non_empty=kwargs.pop('non_empty',True), **kwargs)
		self.check_value()

	def check_value(self):
		if super(UUID4Attribute,self).check_value() is False:
			return False
		if self.value is not None:
			try:
				assert(len(self.value) == 36)
				assert(all([c in BASE16_ALPHABET+'-' for c in self.value.lower()]))
				lens = [len(o) for o in self.value.split('-')]
				assert(lens.count(4) == 3 and set(lens) == {8,4,12})
			except AssertionError: 
				raise StringFormatError(self,f"Wrong str format for UUID4Attribute {self.value}")

	def set_value(self,value):
		self.value = value
		self.check_value()

	def generate_random_value():
		return str(uuid.uuid4())


class UTF8BASE64Attribute(StringAttribute):
	"""docstring for UTF8BASE64Attribute"""
	def __init__(self, *args, **kwargs):
		force_lower_case = kwargs.pop('force_lower_case',False)
		kwargs['force_cast'] = kwargs.get('force_cast',lambda x:UTF8BASE64Attribute.decode(x,force_lower_case=force_lower_case))
		super(UTF8BASE64Attribute, self).__init__(*args, force_lower_case=force_lower_case, **kwargs)
		self.check_value()

	def set_value(self,value):
		if self.force_lower_case and value is not None:
			self.value = value.lower()
		else:
			self.value = value
		self.check_value()

	def decode(x,force_lower_case=False):
		try:
			return base64.b64decode(x).decode('utf-8')
		except:
			if force_lower_case and x is not None:
				return x.lower()
			return x


class NumericAttribute(Attribute):
	"""docstring for NumericAttribute"""
	def __init__(self, name, value_type, min=None, max=None, *args, **kwargs):
		super(NumericAttribute, self).__init__(name, value_type, *args, **kwargs)
		self.min = min
		self.max = max
		self.check_value()

	def check_value(self):
		if super(NumericAttribute,self).check_value() is False:
			return False
		if self.value is not None and self.max is not None:
			if self.value > self.max:
				raise NumericOverBoundError(self,f"Value of NumericAttribute exceeds the maximum allowed. (value: {self.value}, max: {self.max})")
		if self.value is not None and self.min is not None:
			if self.value < self.min:
				raise NumericBelowBoundError(self,f"Value of NumericAttribute is less than the minimum allowed. (value: {self.value}, min: {self.min})")
		
class ClockAttribute(Attribute):
	"""docstring for ClockAttribute"""
	def __init__(self, name, value_type, *args, min=None, max=None, **kwargs):
		super(ClockAttribute, self).__init__(name, value_type, *args, **kwargs)
		self.min = min
		self.max = max
		self.check_value()

	def check_value(self):
		if super(ClockAttribute,self).check_value() is False:
			return False
		if self.value is not None and self.max is not None:
			if self.value > self.max:
				raise DateOverBoundError(self,f"Value of ClockAttribute exceeds the maximum allowed. (value: {self.value}, max: {self.max})")
		if self.value is not None and self.min is not None:
			if self.value < self.min:
				raise DateBelowBoundError(self,f"Value of ClockAttribute is less than the minimum allowed. (value: {self.value}, min: {self.min})")
		

class IntegerAttribute(NumericAttribute):
	"""docstring for IntegerAttribute"""
	def __init__(self, name, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',IntegerAttribute.cast)
		super(IntegerAttribute, self).__init__(name,int,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def to_scalar(self):
		return self.value

	def cast(value):
		if not value is None:
			return int(value)


class RealAttribute(NumericAttribute):
	"""docstring for RealAttribute"""
	def __init__(self, name, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',RealAttribute.cast)
		super(RealAttribute, self).__init__(name,float,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def to_scalar(self):
		return self.value

	def cast(value):
		if not value is None:
			return float(value)


class BooleanAttribute(Attribute):
	"""docstring for BooleanAttribute"""
	def __init__(self, name, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',bool)
		super(BooleanAttribute, self).__init__(name,bool,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def to_scalar(self):
		return self.value


class DateAttribute(ClockAttribute):
	"""docstring for DateAttribute"""
	def __init__(self, name, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',DateAttribute.cast)
		super(DateAttribute, self).__init__(name,date,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def to_scalar(self):
		return self.value.isoformat()

	def cast(value):
		if issubclass(type(value),str):
			if value == "":
				return None
			return datetime.strptime(value).date()
		elif issubclass(type(value),datetime):
			return value.date()
		return value


class DateTimeAttribute(ClockAttribute):
	"""docstring for DateTimeAttribute"""
	def __init__(self, name, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',DateTimeAttribute.cast)
		super(DateTimeAttribute, self).__init__(name,datetime,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def to_scalar(self):
		return self.value.isoformat()

	def cast(value):
		if issubclass(type(value),str):
			if value == "":
				return None
			return datetime.strptime(value)
		return value
		

class RangeAttribute(IntegerAttribute):
	"""docstring for RangeAttribute"""
	def __init__(self, name, values, **kwargs):
		kwargs['force_cast'] = kwargs.get('force_cast',RangeAttribute.cast)
		kwargs['min'] = kwargs.get('min',0); kwargs['max'] = kwargs.get('max',len(values)); 
		self.values = values if type(values) is dict else {i:v for i,v in enumerate(values)}
		self.reversed = {v:k for k,v in self.values.items()} 
		super(RangeAttribute, self).__init__(name,**kwargs)
		self.check_value()

	def set_value(self,value):
		self.value = value
		self.check_value()

	def check_value(self):
		if super(RangeAttribute,self).check_value() is False:
			return False
		if not (self.value in self.values):
			raise UnknownValueError(f"Unknown value for RangeAttribute. (value: {self.value}, min: {self.min}, max: {self.max})")

	def to_scalar(self):
		return self.value

	def cast(value):
		if not value is None:
			try:
				return int(value)
			except:
				return self.reversed[value]