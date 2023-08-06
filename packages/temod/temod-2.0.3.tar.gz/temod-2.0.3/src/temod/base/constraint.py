from .attribute import Attribute
from .entity import Entity

from .condition import Equals, And

from typing import Type



class ConstraintException(Exception):
	pass


class Multiplicity(object):
	def __init__(self, start=None, end=None, min_start=None, max_start=None, min_end=None, max_end=None):
		if start is not None:
			min_start = start; max_start = start
		if end is not None:
			min_end = end; max_end = end
		self.start = start
		self.end = end
		self.min_start = min_start
		self.min_end = min_end
		self.max_start = max_start
		self.max_end = max_end

class Constraint(object):
	"""docstring for Constraint"""
	def __init__(self, *attributes, multiplicity=None,**kwargs):
		super(Constraint, self).__init__()
		self.attributes = []
		for attr in getattr(self,'ATTRIBUTES',[]):
			found = [a for a in attr['entity'].ATTRIBUTES if a['name'] == attr['name']][0]
			self.attributes.append(found['type'](found['name'],owner_type=attr['entity']))

		self.multiplicity = getattr(self,"MULTIPLICITY",multiplicity)
		if self.multiplicity is None:
			self.multiplicity = Multiplicity(start=1,end=1)


class EqualityConstraint(Constraint):
	def condition(self):
		return Equals(*self.attributes)


class BindConstraint(Constraint):
	"""docstring for Constraint"""
	def __init__(self, *constraints, multiplicity=None,**kwargs):
		self.constraints = []; self.attributes = []
		for constraint in getattr(self,'CONSTRAINTS',[]):
			attributes = []
			for attr in constraint:
				found = [a for a in attr['entity'].ATTRIBUTES if a['name'] == attr['name']][0]
				attributes.append(found['type'](found['name'],owner_type=attr['entity']))
			self.attributes.extend(attributes)
			self.constraints.append(EqualityConstraint(attributes,multiplicity=multiplicity))
		self.multiplicity = getattr(self,"MULTIPLICITY",multiplicity)

	def condition(self):
		return And(*[Equals(*constraint.attributes) for constraint in self.constraints])