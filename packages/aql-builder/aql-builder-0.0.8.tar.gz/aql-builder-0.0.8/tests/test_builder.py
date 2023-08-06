import unittest

from arango.collection import Collection

from aql_builder import AQLBuilder as AB
from aql_builder import types
from aql_builder.errors import AqlError


class AQLBuilderCastTest(unittest.TestCase):

	def _test_auto_cast(self, token, should):
		self.assertIsInstance(types.auto_cast_token(token), should)

	def test_cast_none(self):
		self._test_auto_cast(None, types.NullLiteral)

	def test_cast_expr(self):
		self._test_auto_cast(AB.expr('abcd'), types._Expression)

	def test_cast_partial_statement(self):
		self._test_auto_cast(AB.for_('abcd').in_('efgh'), types._PartialStatement)

	def test_cast_bool(self):
		self._test_auto_cast(True, types.BooleanLiteral)

	def test_cast_num(self):
		self._test_auto_cast(5, types.IntegerLiteral)
		self._test_auto_cast(5.5, types.NumberLiteral)

	def test_cast_str(self):
		self._test_auto_cast('5', types.IntegerLiteral)
		self._test_auto_cast('5.5', types.NumberLiteral)
		self._test_auto_cast('"abcd"', types.StringLiteral)
		self._test_auto_cast('5..10', types.RangeExpression)
		self._test_auto_cast('filter', types.Identifier)
		self._test_auto_cast('abcd.efgh', types.SimpleReference)

	def test_cast_obj(self):
		self._test_auto_cast(Collection(None, None, 'abcd'), types.Identifier)
		self._test_auto_cast([1,2,3,4], types.ListLiteral)
		self._test_auto_cast({'1': 2, '3': 4}, types.ObjectLiteral)


class AQLBuilderStaticsTest(unittest.TestCase):

	def _test_static(self, ab, should):
		self.assertEqual(should, ab.to_aql())

	def _test_static_raise(self, expected_exception, ab_callable, *abargs):
		with self.assertRaises(expected_exception):
			ab_callable(*abargs).to_aql()

	def test_static_if(self):
		self._test_static(AB.if_(AB.expr('a == b'), 'c', 'd'), 'a == b ? c : d')
		self._test_static(AB.expr('a == b').then('c').else_('d'), 'a == b ? c : d')
		self._test_static(AB.expr('a == b').then('c').otherwise('d'), 'a == b ? c : d')

	def test_static_literal(self):
		self.assertEqual(len(AB.str('abcd')), 4)
		self.assertIsNone(types.Literal.match('abcd'))

	def test_static_null(self):
		self._test_static(AB.null(), 'null')
		self._test_static(AB.null(None), 'null')
		self._test_static(AB.null(types.NullLiteral()), 'null')
		self._test_static_raise(AqlError, AB.null, False)

	def test_static_bool(self):
		self._test_static(AB.bool(True), 'true')
		self._test_static(AB.bool(False), 'false')
		self._test_static(AB.bool(1), 'true')
		self._test_static(AB.bool(0), 'false')
		self._test_static(AB.bool('aaa'), 'true')
		self._test_static(AB.bool(''), 'false')
		self._test_static(AB.bool(None), 'false')
		self._test_static(AB.bool(types.BooleanLiteral(True)), 'true')

	def test_static_num(self):
		self._test_static(AB.num(0), '0.0')
		self._test_static(AB.num(1), '1.0')
		self._test_static(AB.num(0.00), '0.0')
		self._test_static(AB.num(1.00), '1.0')
		self._test_static(AB.num(-1.00), '-1.0')
		self._test_static(AB.num(12345.67890), '12345.6789')
		self._test_static(AB.num(types.NumberLiteral(12345.67890)), '12345.6789')
		self._test_static(AB.num(types.IntegerLiteral(12345)), '12345.0')

	def test_static_int(self):
		self._test_static(AB.int(0), '0')
		self._test_static(AB.int(1), '1')
		self._test_static(AB.int(0.00), '0')
		self._test_static(AB.int(1.00), '1')
		self._test_static(AB.int(-1.00), '-1')
		self._test_static(AB.int(12345), '12345')
		self._test_static(AB.int(types.NumberLiteral(12345)), '12345')
		self._test_static(AB.int(types.IntegerLiteral(12345)), '12345')

	def test_static_str(self):
		self._test_static(AB.str('abcd'), '"abcd"')
		self._test_static(AB.str('abcd.efgh'), '"abcd.efgh"')
		self._test_static(AB.str('1234'), '"1234"')
		self._test_static(AB.str(''), '""')
		self._test_static(AB.str(types.StringLiteral('abcd')), '"abcd"')
		self._test_static(AB.str(types.NullLiteral()), '"null"')

	def test_static_list(self):
		self._test_static(AB.list(['a', 'b', 'c', 'd']), '[a, b, c, d]')
		self._test_static(AB.list([1, 2, 3, 4]), '[1, 2, 3, 4]')
		self._test_static(AB.list([AB.expr('abcd'), 2, 3, 4]), '[abcd, 2, 3, 4]')
		self._test_static(AB.list(types.ListLiteral([1, 2, 3, 4])), '[1, 2, 3, 4]')

	def test_static_obj(self):
		self._test_static(AB.obj({'a': 'b', 'c': 'd'}), '{"a": b, "c": d}')
		self._test_static(AB.obj({'a': '"b"', 'c': '"d"'}), '{"a": "b", "c": "d"}')
		self._test_static(AB.obj({'1': 2, '3': 4}), '{"1": 2, "3": 4}')
		self._test_static(AB.obj({'"1"': 2, '"3"': 4}), '{"\\"1\\"": 2, "\\"3\\"": 4}')
		self._test_static(AB.obj({'+1': 2, '3': 4}), '{"\\"+1\\"": 2, "3": 4}')

	def test_static_expr(self):
		self._test_static(AB.expr('abcd'), 'abcd')
		self._test_static(AB.expr('abcd.efgh'), 'abcd.efgh')
		self._test_static(
			AB.expr('abcd xyz efgh (1234 OR ijkl)'),
			'abcd xyz efgh (1234 OR ijkl)'
		)
		self._test_static(AB.expr(types.RawExpression('abcd.efgh')), 'abcd.efgh')

	def test_static_range(self):
		self._test_static(AB.range(10, 20), '10..20')
		self._test_static(AB.range('10', '20'), '10..20')

	def test_static_ref(self):
		self._test_static(AB.ref('abcd'), 'abcd')
		self._test_static(AB.ref('abcd.efgh'), 'abcd.efgh')
		self._test_static(AB.ref(Collection(None, None, 'abcd')), 'abcd')
		self._test_static(AB.ref(types.SimpleReference('abcd')), 'abcd')

	def test_static_for(self):
		self._test_static(AB.for_('abcd').in_('efgh'), 'FOR abcd IN efgh')
		self._test_static(AB.for_('ab-cd').in_('ef-gh'), 'FOR `ab-cd` IN `ef-gh`')
		self._test_static(AB.for_(Collection(None, None, 'abcd')).in_('efgh'), 'FOR abcd IN efgh')
		self._test_static(
			AB.for_('abcd').in_('efgh').options({'ijkl': 'mnop'}),
			'FOR abcd IN efgh OPTIONS {"ijkl": mnop}'
		)

	def test_static_filter(self):
		self._test_static(AB.filter('abcd'), 'FILTER abcd')
		self._test_static(AB.filter('abcd.efgh'), 'FILTER abcd.efgh')
		self._test_static(
			AB.filter(AB.expr('abcd xyz efgh (1234 OR ijkl)')),
			'FILTER abcd xyz efgh (1234 OR ijkl)'
		)

	def test_static_search(self):
		self._test_static(AB.search('abcd'), 'SEARCH abcd')
		self._test_static(AB.search('abcd.efgh'), 'SEARCH abcd.efgh')
		self._test_static(
			AB.search(AB.expr('abcd xyz efgh (1234 OR ijkl)')),
			'SEARCH abcd xyz efgh (1234 OR ijkl)'
		)
		self._test_static(
			AB.search(
				AB.ANALYZER(
					AB.expr('abcd.efgh == "X" OR abcd.ijkl == "Y"'),
					AB.str("identity")
				)
			),
			'SEARCH ANALYZER(abcd.efgh == "X" OR abcd.ijkl == "Y", "identity")'
		)

	def test_static_let(self):
		self._test_static(AB.let('abcd', 'efgh'), 'LET abcd = efgh')
		self._test_static(AB.let('abcd', 'efgh.ijkl'), 'LET abcd = efgh.ijkl')

	def test_static_collect(self):
		self._test_static(
			AB.collect('abcd', AB.expr('efgh.ijkl')),
			'COLLECT abcd = efgh.ijkl'
		)
		self._test_static(
			AB.collect([['abcd', AB.expr('efgh.ijkl')]]),
			'COLLECT abcd = efgh.ijkl'
		)
		self._test_static(
			AB.collect([
				['abcd', AB.expr('efgh.ijkl')],
				['mnop', AB.expr('qrst.uvwx')]
			]),
			'COLLECT abcd = efgh.ijkl, mnop = qrst.uvwx'
		)
		# COLLECT variableName = expression
		self._test_static(
			AB.collect({'variableName': 'expression'}),
			'COLLECT variableName = expression'
		)
		self._test_static(
			AB.collect('variableName', 'expression'),
			'COLLECT variableName = expression'
		)
		# COLLECT variableName = expression INTO groupsVariable
		self._test_static(
			AB.collect('variableName', 'expression').into('groupsVariable'),
			'COLLECT variableName = expression INTO groupsVariable'
		)
		# COLLECT variableName = expression INTO groupsVariable = projectionExpression
		self._test_static(
			AB.collect('variableName', AB.expr('expression')
				).into('groupsVariable', AB.expr('projectionExpression')),
			'COLLECT variableName = expression INTO groupsVariable = projectionExpression'
		)
		# COLLECT variableName = expression INTO groupsVariable KEEP keepVariable
		self._test_static(
			AB.collect('variableName', AB.expr('expression')
				).into('groupsVariable').keep('keepVariable'),
			'COLLECT variableName = expression INTO groupsVariable KEEP keepVariable'
		)
		# COLLECT variableName = expression WITH COUNT INTO countVariable
		self._test_static(
			AB.collect('variableName', AB.expr('expression')
				).with_count_into('countVariable'),
			'COLLECT variableName = expression WITH COUNT INTO countVariable'
		)
		# COLLECT variableName = expression AGGREGATE aggregateName = aggregateExpression
		self._test_static(
			AB.collect('variableName', AB.expr('expression')
				).aggregate({'aggregateName': AB.expr('aggregateExpression')}),
			'COLLECT variableName = expression AGGREGATE aggregateName = aggregateExpression'
		)
		# COLLECT variableName = expression AGGREGATE variableName = aggregateExpression INTO groupsVariable
		self._test_static(
			AB.collect('variableName', AB.expr('expression')
				).aggregate({'aggregateName': AB.expr('aggregateExpression')}
				).into('groupsVariable'),
			'COLLECT variableName = expression AGGREGATE aggregateName = aggregateExpression INTO groupsVariable'
		)
		# COLLECT AGGREGATE aggregateName = aggregateExpression
		self._test_static(
			AB.collect().aggregate({'aggregateName': AB.expr('aggregateExpression')}),
			'COLLECT AGGREGATE aggregateName = aggregateExpression'
		)
		# COLLECT AGGREGATE variableName = aggregateExpression INTO groupsVariable
		self._test_static(
			AB.collect().aggregate({'aggregateName': AB.expr('aggregateExpression')}
				).into('groupsVariable'),
			'COLLECT AGGREGATE aggregateName = aggregateExpression INTO groupsVariable'
		)

		# COLLECT AGGREGATE variableName = aggregateExpression INTO groupsVariable OPTIONS {"a": b}
		self._test_static(
			AB.collect().aggregate({'aggregateName': AB.expr('aggregateExpression')}
				).into('groupsVariable').options({'a': 'b'}),
			'COLLECT AGGREGATE aggregateName = aggregateExpression INTO groupsVariable OPTIONS {"a": b}'
		)

	def test_static_collect_with_count_into(self):
		self._test_static(
			AB.collect_with_count_into('abcd'),
			'COLLECT WITH COUNT INTO abcd'
		)
		self._test_static(
			AB.collect_with_count_into('abcd').options({'a': 'b'}),
			'COLLECT WITH COUNT INTO abcd OPTIONS {"a": b}'
		)
		self._test_static(
			AB.for_('abcd').in_('efgh').collect_with_count_into('ijkl'),
			'FOR abcd IN efgh COLLECT WITH COUNT INTO ijkl'
		)

	def test_static_sort(self):
		self._test_static(AB.sort('abcd'), 'SORT abcd')
		self._test_static(AB.sort('abcd', 'ASC'), 'SORT abcd ASC')
		self._test_static(AB.sort('abcd', 'DESC'), 'SORT abcd DESC')
		self._test_static(AB.sort('abcd', 'efgh', 'DESC'), 'SORT abcd, efgh DESC')
		self._test_static(AB.sort('abcd', 'ASC', 'efgh', 'DESC'), 'SORT abcd ASC, efgh DESC')
		self._test_static(AB.sort(None), 'SORT null')
		self._test_static(AB.sort('abcd', types.Keyword(types.Keyword('ASC'))), 'SORT abcd ASC')

	def test_static_limit(self):
		self._test_static(AB.limit(5), 'LIMIT 5')
		self._test_static(AB.limit(2, 5), 'LIMIT 2, 5')

	def test_static_remove(self):
		self._test_static(
			AB.remove(AB.expr('expr')).in_('collection'),
			'REMOVE expr IN collection'
		)
		self._test_static(
			AB.remove(AB.expr('expr')).in_('collection').options({'a': 'b'}),
			'REMOVE expr IN collection OPTIONS {"a": b}'
		)
		self._test_static(
			AB.remove(AB.expr('expr')).into('collection'),
			'REMOVE expr IN collection'
		)

	def test_static_return(self):
		self._test_static(
			AB.return_('abcd'),
			'RETURN abcd'
		)
		self._test_static(
			AB.for_('abcd').in_('efgh').return_('ijkl'),
			'FOR abcd IN efgh RETURN ijkl'
		)

	def test_static_return_distinct(self):
		self._test_static(
			AB.return_distinct('abcd'),
			'RETURN DISTINCT abcd'
		)
		self._test_static(
			AB.for_('abcd').in_('efgh').return_distinct('ijkl'),
			'FOR abcd IN efgh RETURN DISTINCT ijkl'
		)

	def test_static_upsert(self):
		# UPSERT searchExpression INSERT insertExpression UPDATE updateExpression IN collection
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'),
			'UPSERT searchExpression INSERT insertExpression UPDATE updateExpression IN collection'
		)
		# UPSERT searchExpression INSERT insertExpression REPLACE updateExpression IN collection
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).replace('updateExpression'
				).in_('collection'),
			'UPSERT searchExpression INSERT insertExpression REPLACE updateExpression IN collection'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).replace('updateExpression'
				).into('collection'),
			'UPSERT searchExpression INSERT insertExpression REPLACE updateExpression IN collection'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'
				).options({'a': 'b'}),
			'UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection OPTIONS {"a": b}'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'
				).return_new(),
			'UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection '
			'RETURN NEW'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'
				).return_new('newExpression'),
			'UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection '
			'RETURN newExpression'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'
				).return_old(),
			'UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection '
			'RETURN OLD'
		)
		self._test_static(
			AB.upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'
				).return_old('oldExpression'),
			'UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection '
			'RETURN oldExpression'
		)
		self._test_static(
			AB.for_('abcd').in_('efgh'
				).upsert('searchExpression'
				).insert('insertExpression'
				).update('updateExpression'
				).in_('collection'),
			'FOR abcd IN efgh UPSERT searchExpression INSERT insertExpression '
			'UPDATE updateExpression IN collection'
		)

	def test_static_insert(self):
		# INSERT document INTO collection
		self._test_static(
			AB.insert('document'
				).into('collection'),
			'INSERT document INTO collection'
		)
		# INSERT document INTO collection OPTIONS options
		self._test_static(
			AB.insert('document'
				).into('collection'
				).options({'a': 'b'}),
			'INSERT document INTO collection OPTIONS {"a": b}'
		)
		# INSERT document INTO collection RETURN NEW
		self._test_static(
			AB.insert('document'
				).into('collection'
				).return_new(),
			'INSERT document INTO collection RETURN NEW'
		)
		# INSERT document INTO collection RETURN NEW
		self._test_static(
			AB.insert('document'
				).into('collection'
				).return_new('NEW'),
			'INSERT document INTO collection RETURN NEW'
		)
		# INSERT document INTO collection RETURN NEW._key`
		self._test_static(
			AB.insert('document'
				).into('collection'
				).return_new('NEW._key'),
			'INSERT document INTO collection RETURN NEW._key'
		)

	def test_static_update(self):
		# UPDATE document IN collection
		self._test_static(
			AB.update('document'
				).in_('collection'),
			'UPDATE document IN collection'
		)
		self._test_static(
			AB.update('document'
				).into('collection'),
			'UPDATE document IN collection'
		)
		# UPDATE document IN collection OPTIONS {"a": b}
		self._test_static(
			AB.update('document'
				).in_('collection'
				).options({'a': 'b'}),
			'UPDATE document IN collection OPTIONS {"a": b}'
		)
		# UPDATE keyExpression WITH document IN collection
		self._test_static(
			AB.update('keyExpression'
				).with_('document'
				).in_('collection'),
			'UPDATE keyExpression WITH document IN collection'
		)
		self._test_static(
			AB.update('keyExpression'
				).with_('document'
				).into('collection'),
			'UPDATE keyExpression WITH document IN collection'
		)
		self._test_static(
			AB.update('document'
				).in_('collection'
				).return_new(),
			'UPDATE document IN collection RETURN NEW'
		)
		self._test_static(
			AB.update('document'
				).in_('collection'
				).return_new('expr'),
			'UPDATE document IN collection RETURN expr'
		)
		self._test_static(
			AB.update('document'
				).in_('collection'
				).return_old(),
			'UPDATE document IN collection RETURN OLD'
		)
		self._test_static(
			AB.update('document'
				).in_('collection'
				).return_old('expr'),
			'UPDATE document IN collection RETURN expr'
		)

	def test_static_replace(self):
		# REPLACE document IN collection
		self._test_static(
			AB.replace('document'
				).in_('collection'),
			'REPLACE document IN collection'
		)
		self._test_static(
			AB.replace('document'
				).into('collection'),
			'REPLACE document IN collection'
		)
		# REPLACE document IN collection OPTIONS {"a": b}
		self._test_static(
			AB.replace('document'
				).in_('collection'
				).options({'a': 'b'}),
			'REPLACE document IN collection OPTIONS {"a": b}'
		)
		# REPLACE keyExpression WITH document IN collection
		self._test_static(
			AB.replace('keyExpression'
				).with_('document'
				).in_('collection'),
			'REPLACE keyExpression WITH document IN collection'
		)
		self._test_static(
			AB.replace('keyExpression'
				).with_('document'
				).into('collection'),
			'REPLACE keyExpression WITH document IN collection'
		)
		self._test_static(
			AB.replace('document'
				).in_('collection'
				).return_new(),
			'REPLACE document IN collection RETURN NEW'
		)
		self._test_static(
			AB.replace('document'
				).in_('collection'
				).return_new('expr'),
			'REPLACE document IN collection RETURN expr'
		)
		self._test_static(
			AB.replace('document'
				).in_('collection'
				).return_old(),
			'REPLACE document IN collection RETURN OLD'
		)
		self._test_static(
			AB.replace('document'
				).in_('collection'
				).return_old('expr'),
			'REPLACE document IN collection RETURN expr'
		)

	def test_static_function_call(self):
		# call functions on AQLBuilder class
		ab = AB
		self._test_static(
			ab.TO_BOOL(AB.expr('true')),
			'TO_BOOL(true)'
		)
		# call functions on types._Expression classes
		ab = AB.expr('abcd')
		self._test_static(
			ab.TO_BOOL(AB.expr('true')),
			'TO_BOOL(true)'
		)
		# call functions on types._PartialStatement classes
		ab = AB.for_('abcd').in_('efgh')
		self._test_static(
			ab.TO_BOOL(AB.expr('true')),
			'TO_BOOL(true)'
		)

	def test_static_functions(self):
		self._test_static(
			AB.TO_BOOL(AB.expr('true')),
			'TO_BOOL(true)'
		)
		self._test_static(
			AB.CONCAT('abcd', 'efgh', 'ijkl'),
			'CONCAT(abcd, efgh, ijkl)'
		)


class AQLBuilderExpressionTest(unittest.TestCase):

	def _test(self, ab, should):
		self.assertEqual(should, ab.to_aql())

	def test_expr_get(self):
		self._test(AB.expr('obj').get('prop1', '"prop2"'), 'obj[prop1]["prop2"]')

	def test_expr_and(self):
		self._test(AB.expr('obj1').and_('obj2'), 'obj1 && obj2')

	def test_expr_or(self):
		self._test(AB.expr('obj1').or_('obj2'), 'obj1 || obj2')

	def test_expr_add(self):
		self._test(AB.expr('obj1').add('obj2'), 'obj1 + obj2')

	def test_expr_plus(self):
		self._test(AB.expr('obj1').plus('obj2'), 'obj1 + obj2')

	def test_expr_sub(self):
		self._test(AB.expr('obj1').sub('obj2'), 'obj1 - obj2')

	def test_expr_minus(self):
		self._test(AB.expr('obj1').minus('obj2'), 'obj1 - obj2')

	def test_expr_mul(self):
		self._test(AB.expr('obj1').mul('obj2'), 'obj1 * obj2')

	def test_expr_times(self):
		self._test(AB.expr('obj1').times('obj2'), 'obj1 * obj2')

	def test_expr_div(self):
		self._test(AB.expr('obj1').div('obj2'), 'obj1 / obj2')

	def test_expr_mod(self):
		self._test(AB.expr('obj1').mod('obj2'), 'obj1 % obj2')

	def test_expr_eq(self):
		self._test(AB.expr('obj1').eq('obj2'), 'obj1 == obj2')

	def test_expr_gt(self):
		self._test(AB.expr('obj1').gt('obj2'), 'obj1 > obj2')

	def test_expr_gte(self):
		self._test(AB.expr('obj1').gte('obj2'), 'obj1 >= obj2')

	def test_expr_lt(self):
		self._test(AB.expr('obj1').lt('obj2'), 'obj1 < obj2')

	def test_expr_lte(self):
		self._test(AB.expr('obj1').lte('obj2'), 'obj1 <= obj2')

	def test_expr_neq(self):
		self._test(AB.expr('obj1').neq('obj2'), 'obj1 != obj2')

	def test_expr_not(self):
		self._test(AB.expr('obj1').not_(), '!obj1')

	def test_expr_neg(self):
		self._test(AB.expr('obj1').neg(), '-obj1')

	def test_expr_in(self):
		self._test(AB.expr('obj1').in_(['obj2', 'obj3']), 'obj1 in [obj2, obj3]')

	def test_expr_not_in(self):
		self._test(AB.expr('obj1').not_in(['obj2', 'obj3']), 'obj1 not in [obj2, obj3]')


class AQLBuilderExempleTest(unittest.TestCase):

	def _example(self, should, builder):
		self.assertEqual(should, builder.to_aql())

	def test_example_001(self):
		self._example(
			'FOR my IN mycollection RETURN my._key',
			AB.for_('my').in_('mycollection').return_('my._key')
		)

	def test_example_002(self):
		self._example(
			'RETURN "this will be returned"',
			AB.return_('"this will be returned"')
		)

	def test_example_003(self):
		self._example(
			'FOR year IN [2011, 2012, 2013] '
			'FOR quarter IN [1, 2, 3, 4] '
			'RETURN {'
			'"y": year, '
			'"q": quarter, '
			'"nice": CONCAT(TO_STRING(quarter), "/", TO_STRING(year))'
			'}',
			AB.for_('year').in_([2011, 2012, 2013]
				).for_('quarter').in_([1, 2, 3, 4]
				).return_({
					'y': 'year',
					'q': 'quarter',
					'nice': AB.CONCAT(AB.TO_STRING('quarter'), '"/"', AB.TO_STRING('year'))
				})
		)

	def test_example_004(self):
		self._example(
			'FOR u IN users '
			'UPDATE u WITH {'
			'"gender": TRANSLATE(u.gender, {"m": "male", "f": "female"})'
			'} IN users',
			AB.for_('u').in_('users')
				.update('u').with_({
					'gender': AB.TRANSLATE('u.gender', {'m': '"male"', 'f': '"female"'})
				}).in_('users')
		)

	def test_example_005(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'UPDATE u WITH {"numberOfLogins": 0} IN users',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.update('u').with_({'numberOfLogins': 0}).in_('users')
		)

	def test_example_006(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'UPDATE u WITH {'
			'"numberOfLogins": (u.numberOfLogins + 1)'
			'} IN users',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.update('u').with_({
					'numberOfLogins': AB.ref('u.numberOfLogins').add(1)
				}).in_('users')
		)

	def test_example_007(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'UPDATE u WITH {'
			'"lastLogin": DATE_NOW(), '
			'"numberOfLogins": (HAS(u, "numberOfLogins") ? (u.numberOfLogins + 1) : 1)'
			'} IN users',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.update('u').with_({
					'lastLogin': AB.DATE_NOW(),
					'numberOfLogins': (
						AB.HAS('u', '"numberOfLogins"')
						.then(AB.ref('u.numberOfLogins').add(1))
						.else_(1)
					)
				}).in_('users')
		)

	def test_example_008(self):
		self._example(
			'FOR u IN users '
			'REPLACE u IN backup',
			AB.for_('u').in_('users')
				.replace('u').in_('backup')
		)

	def test_example_009(self):
		self._example(
			'FOR u IN users '
			'REPLACE u IN backup OPTIONS {"ignoreErrors": true}',
			AB.for_('u').in_('users')
				.replace('u').in_('backup').options({'ignoreErrors': True})
		)

	def test_example_010(self):
		self._example(
			'FOR u IN users '
			'FILTER (((u.active == true) && (u.age >= 35)) && (u.age <= 37)) '
			'REMOVE u IN users',
			AB.for_('u').in_('users')
				.filter(
					AB.ref('u.active').eq(True)
					.and_(AB.ref('u.age').gte(35))
					.and_(AB.ref('u.age').lte(37))
				)
				.remove('u').in_('users')
		)

	def test_example_011(self):
		self._example(
			'FOR i IN 1..1000 '
			'INSERT {'
			'"id": (100000 + i), '
			'"age": (18 + FLOOR((RAND() * 25))), '
			'"name": CONCAT(test, TO_STRING(i)), '
			'"active": false, '
			'"gender": (((i % 2) == 0) ? "male" : "female")'
			'} INTO users',
			AB.for_('i').in_(AB.range(1, 1000))
				.insert({
					'id': AB(100000).add('i'),
					'age': AB(18).add(AB.FLOOR(AB.RAND().times(25))),
					'name': AB.CONCAT('test', AB.TO_STRING('i')),
					'active': False,
					'gender': (
						AB.ref('i').mod(2).eq(0)
						.then('"male"')
						.else_('"female"')
					)
				}).into('users')
		)

	def test_example_012(self):
		self._example(
			'FOR u IN users '
			'INSERT u INTO backup',
			AB.for_('u').in_('users')
				.insert('u').into('backup')
		)

		self._example(
			'FOR u IN users '
			'LIMIT 0, 3 '
			'RETURN {"users": {'
			'"isActive": (u.active ? "yes" : "no"), '
			'"name": u.name'
			+'}}',
			AB.for_('u').in_('users')
				.limit(0, 3)
				.return_({
					'users': {
						'isActive': AB.ref('u.active').then('"yes"').else_('"no"'),
						'name': 'u.name'
					}
				})
		)

	def test_example_013(self):
		self._example(
			'FOR u IN users '
			'FILTER ((u.active == true) && (u.age >= 30)) '
			'SORT u.age DESC '
			'LIMIT 0, 5 '
			'RETURN {"age": u.age, "name": u.name}',
			AB.for_('u').in_('users')
				.filter(
					AB.ref('u.active').eq(True)
					.and_(AB.ref('u.age').gte(30))
				)
				.sort('u.age', 'DESC')
				.limit(0, 5)
				.return_({
					'age': 'u.age',
					'name': 'u.name'
				})
		)

	def test_example_014(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'LIMIT 0, 4 '
			'FOR f IN relations '
			'FILTER ((f.type == "friend") && (f.from == u.id)) '
			'RETURN {"user": u.name, "friendId": f.to}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.limit(0, 4)
				.for_('f').in_('relations')
				.filter(
					AB.ref('f.type').eq('"friend"')
					.and_(AB.ref('f.from').eq('u.id'))
				)
				.return_({
					'user': 'u.name',
					'friendId': 'f.to'
				})
		)

	def test_example_015(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'LIMIT 0, 4 '
			'RETURN {'
			'"user": u.name, '
			'"friendIds": ('
			'FOR f IN relations '
			'FILTER ((f.from == u.id) && (f.type == "friend")) '
			'RETURN f.to'
			')'
			'}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.limit(0, 4)
				.return_({
					'user': 'u.name',
					'friendIds': AB.for_('f').in_('relations').filter(
						AB.ref('f.from').eq('u.id')
						.and_(AB.ref('f.type').eq('"friend"'))
					).return_('f.to')
				})
		)

	def test_example_016(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'LIMIT 0, 4 '
			'RETURN {'
			'"user": u.name, '
			'"friendIds": ('
			'FOR f IN relations '
			'FILTER ((f.from == u.id) && (f.type == "friend")) '
			'FOR u2 IN users '
			'FILTER (f.to == u2.id) '
			'RETURN u2.name'
			')'
			'}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.limit(0, 4)
				.return_({
					'user': 'u.name',
					'friendIds': AB.for_('f').in_('relations').filter(
						AB.ref('f.from').eq('u.id')
						.and_(AB.ref('f.type').eq('"friend"'))
					).for_('u2').in_('users').filter(
						AB.ref('f.to').eq('u2.id')
					).return_('u2.name')
				})
		)

	def test_example_017(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'COLLECT age = u.age INTO usersByAge '
			'SORT age DESC '
			'LIMIT 0, 5 '
			'RETURN {"age": age, "users": usersByAge[*].u.name}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.collect({'age': 'u.age'}).into('usersByAge')
				.sort('age', 'DESC').limit(0, 5)
				.return_({
					'age': 'age',
					'users': 'usersByAge[*].u.name'
				})
		)

	def test_example_018(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'COLLECT age = u.age INTO usersByAge '
			'SORT age DESC '
			'LIMIT 0, 5 '
			'RETURN {"age": age, "users": ('
			'FOR temp IN usersByAge '
			'RETURN temp.u.name'
			')}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.collect({'age': 'u.age'}).into('usersByAge')
				.sort('age', 'DESC').limit(0, 5)
				.return_({
					'age': 'age',
					'users': AB.for_('temp').in_('usersByAge').return_('temp.u.name')
				})
		)

	def test_example_019(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'COLLECT ageGroup = (FLOOR((u.age / 5)) * 5), gender = u.gender INTO group '
			'SORT ageGroup DESC '
			'RETURN {"ageGroup": ageGroup, "gender": gender}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.collect({
					'ageGroup': AB.FLOOR(AB.ref('u.age').div(5)).times(5),
					'gender': 'u.gender'
				}).into('group')
				.sort('ageGroup', 'DESC')
				.return_({
					'ageGroup': 'ageGroup',
					'gender': 'gender'
				})
		)

	def test_example_020(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'COLLECT ageGroup = (FLOOR((u.age / 5)) * 5), gender = u.gender INTO group '
			'SORT ageGroup DESC '
			'RETURN {"ageGroup": ageGroup, "gender": gender, "numUsers": LENGTH(group)}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.collect({
					'ageGroup': AB.FLOOR(AB.ref('u.age').div(5)).times(5),
					'gender': 'u.gender'
				}).into('group')
				.sort('ageGroup', 'DESC')
				.return_({
					'ageGroup': 'ageGroup',
					'gender': 'gender',
					'numUsers': AB.LENGTH('group')
				})
		)

	def test_example_021(self):
		self._example(
			'FOR u IN users '
			'FILTER (u.active == true) '
			'COLLECT ageGroup = (FLOOR((u.age / 5)) * 5) INTO group '
			'LET numUsers = LENGTH(group) '
			'FILTER (numUsers > 2) '
			'SORT numUsers DESC '
			'LIMIT 0, 3 '
			'RETURN {"ageGroup": ageGroup, "numUsers": numUsers, "users": group[*].u.name}',
			AB.for_('u').in_('users')
				.filter(AB.ref('u.active').eq(True))
				.collect({
					'ageGroup': AB.FLOOR(AB.ref('u.age').div(5)).times(5)
				}).into('group')
				.let('numUsers', AB.LENGTH('group'))
				.filter(AB.ref('numUsers').gt(2))
				.sort('numUsers', 'DESC')
				.limit(0, 3)
				.return_({
					'ageGroup': 'ageGroup',
					'numUsers': 'numUsers',
					'users': 'group[*].u.name'
				})
		)

	def test_example_022(self):
		x = AB.str('192.168.173.13')
		AB.upsert(x)
		self._example(
			'UPSERT {"ip": "192.168.173.13"} '
			'INSERT {"ip": "192.168.173.13", "name": "flittard"} '
			'UPDATE {} '
			'IN hosts',
			AB.upsert({'ip': AB.str('192.168.173.13')})
				.insert({'ip': AB.str('192.168.173.13'), 'name': AB.str('flittard')})
				.update({})
				.in_('hosts')
		)

	def test_example_023(self):
		self._example(
			'UPSERT {"ip": "192.168.173.13"} '
			'INSERT {"ip": "192.168.173.13", "name": "flittard"} '
			'UPDATE {} '
			'IN hosts '
			'LET isNewInstance = (OLD ? false : true) '
			'RETURN {"doc": NEW, "isNewInstance": isNewInstance}',
			AB.upsert({'ip': AB.str('192.168.173.13')})
				.insert({'ip': AB.str('192.168.173.13'), 'name': AB.str('flittard')})
				.update({})
				.in_('hosts')
				.let('isNewInstance', AB.ref('OLD').then(False).else_(True))
				.return_({'doc': 'NEW', 'isNewInstance': 'isNewInstance'})
		)

	def test_example_024(self):
		self._example(
			'foo[1][2][3]',
			AB.ref('foo').get(1, 2, 3)
		)

	def test_example_025(self):
		self._example(
			'FOR doc IN viewName '
			'SEARCH true OPTIONS {"collections": ["coll1", "coll2"]} '
			'SORT BM25(doc) DESC '
			'RETURN doc',
			AB.for_('doc').in_('viewName')
				.search(AB.bool(True))
				.options({'collections': [AB.str('coll1'), AB.str('coll2')]})
				.sort(AB.BM25('doc'), 'DESC')
				.return_('doc')
		)

