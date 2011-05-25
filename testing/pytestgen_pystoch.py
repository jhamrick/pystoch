###Generated using PyTestGenerator
#!/usr/bin/env python

#Format
#test_<Test_Number>_<Entity_Name>[<Arg_Status>]<Predicted_Status>_<Comment>

import unittest
import sys
import pystoch

class PyUnitframework(unittest.TestCase):
	'''Test Cases generated for pystoch module'''
	def test_1_IntegerStack_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.IntegerStack()
	def test_2_IntegerStack_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.IntegerStack,'TestStr0')
	def test_3_MetropolisHastings_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.MetropolisHastings()
	def test_4_MetropolisHastings_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.MetropolisHastings,'TestStr0')
	def test_5_PyStochCompiler_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.PyStochCompiler()
	def test_6_PyStochCompiler_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochCompiler,'TestStr0')
	def test_7_PyStochObj_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.PyStochObj()
	def test_8_PyStochObj_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochObj,'TestStr0')
	def test_9_RejectionQuery_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.RejectionQuery()
	def test_10_RejectionQuery_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.RejectionQuery,'TestStr0')
	def test_11_StringStack_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.StringStack()
	def test_12_StringStack_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.StringStack,'TestStr0')
	def test_13_binomial_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.binomial)
	def test_14_binomial_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.binomial(5,False)
	def test_15_binomial_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.binomial,'TestStr4',False)
	def test_16_binomial_WithArgs_Fail_With_TwoInvalid_Args(self):
		self.assertRaises(Exception,pystoch.binomial,'TestStr4','TestStr4')
	def test_17_binomial_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.binomial,5,False,'TestStr2')
	def test_18_exponential_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.exponential)
	def test_19_exponential_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.exponential(5)
	def test_20_exponential_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.exponential,'TestStr4')
	def test_21_exponential_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.exponential,5,'TestStr2')
	def test_22_gamma_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.gamma)
	def test_23_gamma_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.gamma(5,96)
	def test_24_gamma_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.gamma,'TestStr4',96)
	def test_25_gamma_WithArgs_Fail_With_TwoInvalid_Args(self):
		self.assertRaises(Exception,pystoch.gamma,'TestStr4','TestStr4')
	def test_26_gamma_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.gamma,5,96,'TestStr2')
	def test_27_gaussian_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.gaussian)
	def test_28_gaussian_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.gaussian(5,96)
	def test_29_gaussian_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.gaussian,'TestStr4',96)
	def test_30_gaussian_WithArgs_Fail_With_TwoInvalid_Args(self):
		self.assertRaises(Exception,pystoch.gaussian,'TestStr4','TestStr4')
	def test_31_gaussian_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.gaussian,5,96,'TestStr2')
	def test_32_poisson_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.poisson)
	def test_33_poisson_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.poisson(5)
	def test_34_poisson_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.poisson,'TestStr4')
	def test_35_poisson_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.poisson,5,'TestStr2')
	def test_36_sample_integer_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.sample_integer)
	def test_37_sample_integer_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.sample_integer(5,96)
	def test_38_sample_integer_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.sample_integer,'TestStr4',96)
	def test_39_sample_integer_WithArgs_Fail_With_TwoInvalid_Args(self):
		self.assertRaises(Exception,pystoch.sample_integer,'TestStr4','TestStr4')
	def test_40_sample_integer_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.sample_integer,5,96,'TestStr2')
	def test_41_uniform_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.uniform)
	def test_42_uniform_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.uniform(5,False)
	def test_43_uniform_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.uniform,'TestStr4',False)
	def test_44_uniform_WithArgs_Fail_With_TwoInvalid_Args(self):
		self.assertRaises(Exception,pystoch.uniform,'TestStr4','TestStr4')
	def test_45_uniform_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.uniform,5,False,'TestStr2')
	def test_46_insert_WithoutArgs_Fail_Without_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochCompiler().insert)
	def test_47_insert_WithArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.PyStochCompiler().insert('TestStr')
	def test_48_insert_WithArgs_Fail_With_OneInvalid_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochCompiler().insert,20.11)
	def test_49_insert_WithArgs_Fail_With_Args_Than_Specified(self):
		self.assertRaises(Exception,pystoch.PyStochCompiler().insert,'TestStr','TestStr2')
	def test_50_print_trace_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.PyStochObj().print_trace()
	def test_51_print_trace_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochObj().print_trace,'TestStr0')
	def test_52_clear_trace_WithoutArgs_Pass_With_Only_Valid_Arguments(self):
		pystoch.PyStochObj().clear_trace()
	def test_53_clear_trace_WithArgs_Fail_With_Arg(self):
		self.assertRaises(Exception,pystoch.PyStochObj().clear_trace,'TestStr0')

if __name__=="__main__":
	testlist=unittest.TestSuite()
	testlist.addTest(unittest.makeSuite(PyUnitframework))
	result = unittest.TextTestRunner(verbosity=2).run(testlist)
	if not result.wasSuccessful():
		sys.exit(1)
	sys.exit(0)