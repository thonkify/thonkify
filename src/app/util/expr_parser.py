# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from pyparsing import *


############
# Classes
############

class ExpressionElement(object):
	def is_specific(self):
		"""Returns whether this operand is guaranteed to select at most one user."""
		return False

	def eval(self, user):
		# Default never matches
		return False


class Operand(ExpressionElement):
	pass


class Operator(ExpressionElement):
	pass


class SimpleOperand(Operand):
	def __init__(self, t):
		self.label = t[0].lower().replace('-', '_')
		try:
			self.test = getattr(self, 'test_%s' % self.label)
		except AttributeError:
			tests = [x[5:] for x in dir(self) if x.startswith('test_')]
			raise KeyError('"%s" is not a valid test; valid tests are %s' % (self.label, tests))

	def __str__(self):
		return self.label

	__repr__ = __str__

	def eval(self, user):
		return self.test(user)

	def test_admin(self, user):
		return user.is_admin

	def test_accepted_tos(self, user):
		return user.accepted_tos

	def test_event_admin(self, user):
		return user.is_event_admin

	def test_banned(self, user):
		return user.is_banned


class AxisOperand(Operand):
	"""Generic base class for an axis-based operand."""

	def __init__(self, t):
		self.axis = t[0].lower()
		self.value = t[1]
		try:
			self.test = getattr(self, 'test_%s' % self.axis)
		except AttributeError:
			tests = [x[5:] for x in dir(self) if x.startswith('test_')]
			raise KeyError('"%s" is not a valid axis; valid axes are %s' % (self.axis, tests))

		if not self.validate_value():
			raise ValueError('"%s" is not a valid value for the %s axis.' % (self.value, self.axis))

	def validate_value(self):
		# by default, all values are valid
		return True

	def __str__(self):
		return '%s:%s' % (self.axis, self.value)

	__repr__ = __str__

	def eval(self, user):
		return self.test(user)


class UserAxisOperand(AxisOperand):
	"""Base class for an axis operand that works just on user models."""

	def validate_value(self):
		if self.axis == 'guid':
			self.value = self.value.lower()
			return re.match(r'[0-9a-f]{32}\.[0-9a-f]{1,2}$', self.value)
		elif self.axis == 'email':
			self.value = self.value.lower()
			return re.match(r'\S+@\S+\.\S+$', self.value)
		elif self.axis == 'nickname':
			self.value = self.value.lower()
			return re.match(r'[0-9a-z_*]{3,15}$', self.value)
		elif self.axis == 'faction':
			self.value = self.value.upper()
			return self.value in ('RESISTANCE', 'ENLIGHTENED')
		return super(UserAxisOperand, self).validate_value()

	def is_specific(self):
		"""Returns whether this operand is guaranteed to select at most one user."""
		return (
			(self.axis == 'guid')
			or (('*' not in self.value) and (self.axis in ('email', 'nickname')))
		)

	def test_guid(self, user):
		return user.guid == self.value

	def test_email(self, user):
		if '*' in self.value:
			return re.match(
				re.escape(self.value.replace('*', '!')).replace('!', '.*'),
				user.email
			)
		else:
			return user.email.lower() == self.value

	def test_nickname(self, user):
		if '*' in self.value:
			return re.match(
				re.escape(self.value.replace('*', '!')).replace('!', '.*'),
				user.nickname.lower()
			)
		else:
			return user.nickname.lower() == self.value

	def test_faction(self, user):
		return user.faction == self.value

	def has_op_node(self):
		return False


class BoolNot(Operator):
	def __init__(self, t):
		self.arg = t[0][1]

	def __str__(self):
		return '!' + str(self.arg)

	__repr__ = __str__

	def eval(self, user):
		return not self.arg.eval(user)

	def has_op_node(self):
		return self.arg.has_op_node()


class BoolBinOp(Operator):
	def __init__(self, t):
		self.args = t[0][0::2]

	def __str__(self):
		sep = " %s " % self.reprsymbol
		return "(" + sep.join(map(str, self.args)) + ")"

	__repr__ = __str__

	def eval(self, user):
		return self.evalfunc(a.eval(user) for a in self.args)

	def has_op_node(self):
		return any(a.has_op_node() for a in self.args)


class BoolAnd(BoolBinOp):
	reprsymbol = '&&'
	evalfunc = all


class BoolOr(BoolBinOp):
	reprsymbol = '||'
	evalfunc = any


############
# Grammar
##########

simpleOperand = Word(alphas + '-_')
simpleOperand.setParseAction(SimpleOperand)

# opAxisKeyword = MatchFirst(CaselessKeyword(x) for x in [
#  'guid', 'op-role', 'op_role', 'op', 'full-member', 'full_member', 'invited', 'applied'
# ])
#
# opAxisOperand = opAxisKeyword.setName('operation axis') + Suppress(':') + Word(alphanums + '*-_.').setName('value')
# opAxisOperand.setParseAction(OpAxisOperand)

userAxisKeyword = MatchFirst(CaselessKeyword(x) for x in ['guid', 'email', 'nickname', 'faction'])

userAxisOperand = userAxisKeyword.setName('user axis') + Suppress(':') + Combine(
	Optional(oneOf('>= > <= <')) + Word(alphanums + '*-_.@')).setName('value')
userAxisOperand.setParseAction(UserAxisOperand)

boolOperand = userAxisOperand | simpleOperand

# define expression, based on expression operand and
# list of operations in precedence order
BoolExpr = infixNotation(boolOperand,
						 [
							 ("!", 1, opAssoc.RIGHT, BoolNot),
							 ("-", 1, opAssoc.RIGHT, BoolNot),
							 ("~", 1, opAssoc.RIGHT, BoolNot),
							 ("&", 2, opAssoc.LEFT, BoolAnd),
							 ("&&", 2, opAssoc.LEFT, BoolAnd),
							 ("|", 2, opAssoc.LEFT, BoolOr),
							 ("||", 2, opAssoc.LEFT, BoolOr),
						 ]) + StringEnd()


def parse(s):
	return BoolExpr.parseString(s)[0]
