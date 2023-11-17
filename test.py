import unittest
from CustomError import CustomError
from InputValidator import InputValidator
from CookieLogProcessor import CookieLogProcessor
from argparse import Namespace
from datetime import datetime
import os, re




class TestInputValidator(unittest.TestCase):
	'''
	Test cases to perform unit tests on InputValidator class functions
	'''

	def setUp(self):
		# Function to setup common test variables before each test function
		# print("In setUp()")
		self.validator = InputValidator()

	def tearDown(self):
		# Function to tear down resources (if any) in use before moving to a new function of test cases
		# print("In tearDown()")
		pass
	
	def test_filename(self):
		# Test cases for validating handling of input filename
		print("Performing Tests for InputValidator.validate_filename()")

		result, _ = self.validator.validate_filename(".csv")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_filename("")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_filename("/cookie_log.csv")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_filename(":.csv")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_filename("c.csv")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_filename("cookie_log.txt")
		self.assertFalse(result)
		
		result, _ = self.validator.validate_filename("cookie_log")
		self.assertFalse(result)
		
		result, _ = self.validator.validate_filename("cookie_log.csv")
		self.assertTrue(result)

	def test_date(self):
		# Test cases for validating handling of input date
		print("Performing Tests for InputValidator.validate_date()")
		
		result, _ = self.validator.validate_date("1234567890")
		self.assertEqual(result, False, _)
		
		result, _ = self.validator.validate_date("1234-12-10")
		self.assertEqual(result, False, _)
		
		result, _ = self.validator.validate_date("2019-5-1")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2019.05.01")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2019/05/01")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("asb67!`&@")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("./Xyz12b#$")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("1897-11-01")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2050-12-20")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2020-02-31")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2021-25-05")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2021- 25-05")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date(" 2021- 25-05")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("2021-43-87")
		self.assertEqual(result, False)
		
		result, _ = self.validator.validate_date("1994-12-21")
		self.assertTrue(result)
		
		result, _ = self.validator.validate_date(" 2017-03-11 ")
		self.assertTrue(result)
		
		result, _ = self.validator.validate_date("2001-05-20")
		self.assertTrue(result)




class TestCookieLogProcessor(unittest.TestCase):
	'''
	Test cases to perform unit tests on CookieLogProcessor class functions
	'''

	@classmethod
	def setUpClass(cls):
		# Function to setup common test variables only once across all test functions
		# Create an instance of argparse.Namespace for testing
		# print("In setUpClass()")
		cls.incorrect_filenames = [".csv", "", "/cookie_log.csv", ":.csv", "c.csv", "cookie_log.txt", "cookie_log"]
		cls.incorrect_dates = ["1234567890", "1234-12-10", "123-12-10", "1234-12-10-", "2019-5-1", "", "2019.05.01", "2019/05/01", "asb67!`&@", "./Xyz12b#$", "1897-11-01", "2050-12-20", "2020-02-31", "2021-25-05", "2021-43-87"]
		cls.correct_filenames = ["cookie_log.csv"]
		cls.correct_dates = ["1994-12-21", "2001-05-20"]
		cls.filenames = list(set(cls.incorrect_filenames).union(set(cls.correct_filenames)))
		cls.dates = list(set(cls.incorrect_dates).union(set(cls.correct_dates)))

	def setUp(self):
		# Function to setup common test variables before each test function
		# print("In setUp()")
		self.args = Namespace()

	def tearDown(self):
		# Function to tear down resources (if any) in use before moving to a new function of test cases
		# print("In tearDown()")
		pass
	
	def test_init(self):
		#Function to check constructor setup of class::CookieLogProcessor()
		print("Performing Tests for CookieLogProcessor.__init__()")
		for filename_ in self.filenames:
			for date_ in self.dates:
				self.args.logfilename, self.args.date = filename_, date_
				if filename_ in self.incorrect_filenames or date_ in self.incorrect_dates:
					self.assertRaises(CustomError, CookieLogProcessor, self.args)
				else:
					processor = CookieLogProcessor(self.args)
					self.assertEqual(processor.query_date, datetime.strptime(str(date_), "%Y-%m-%d").date())
					self.assertEqual(processor.logfilename, filename_)
					self.assertEqual(processor.filepath, os.path.join(os.getcwd(), filename_))

	def test_validate_command_line_inputs(self):
		# Function to test validation of command line inputs. This is only checked for cases that have allowed dates and filenames as disallowed cases are already tested in previous test::test_init()
		print("Performing Tests for CookieLogProcessor._validate_commandline_inputs()")
		for filename_ in self.filenames:
			for date_ in self.dates:
				self.args.logfilename, self.args.date = filename_, date_
				if date_ in self.correct_dates and filename_ in self.correct_filenames:
					processor = CookieLogProcessor(self.args)
					self.assertEqual(processor._validate_commandline_inputs(date_, filename_), True)

	def test_read_logfile(self):
		# Function to test reading of the cookie logfile
		print("Performing Tests for CookieLogProcessor._read_logfile()")
		for filename_ in self.correct_filenames:
			for date_ in self.correct_dates:
				self.args.logfilename, self.args.date = filename_, date_
				processor = CookieLogProcessor(self.args)
				f = open(os.path.join(os.getcwd(), filename_), "r")
				data = f.read().split("\n")[1:]
				f.close()
				self.assertEqual(len(processor._read_logfile()), len(data))

	def test_check_date_format(self):
		# Function to test correct parsing of two types of date formats: one used in query (command line argument) and one used in log file.
		# Correct filename, query date is passed as it is not being tested here, the function itself is being tested
		print("Performing Tests for CookieLogProcessor._check_date_format()")
		self.args.logfilename, self.args.date = "cookie_log.csv", "2023-11-14"
		processor = CookieLogProcessor(self.args)
		processor.datetime_format = "%Y-%m-%d"
		# Testing for datetime format: "%Y-%m-%d"
		for date_ in ["1994-12-21", "2001-05-20", "1897-11-01", "2050-12-20", "1234-12-10", "2019-6-1"]:	
			self.assertEqual(processor._check_date_format(date_), True)
		for date_ in ["1234567890", "", "2019.05.01", "2019/05/01", "asb67!`&@", "./Xyz12b#$", "2020-02-31", "2021-25-05", "2021-43-87"]:	
			self.assertEqual(processor._check_date_format(date_), False)
		
		# Testing for datetime format: "%Y-%m-%dT%H:%M:%S%z"
		# Correct filename is passed as it is not bein tested here.
		self.args.logfilename, self.args.date = "cookie_log.csv", "2023-11-14"
		processor = CookieLogProcessor(self.args)
		processor.datetime_format = "%Y-%m-%dT%H:%M:%S%z"
		for date_ in ["2018-12-09T14:19:00+00:00", "2018-12-09T14:19:00 +00:00", "2018-12-09T14:19:00", "2018-12-09T", "2018-12-09", " 2018-12-09T14:19:00+00:00 ", "2018-12-09T00:00:00+00:00", "2018-12-09Thh:mm:00+00:00", "2018-12-09T@d:kp:00+00:00", "adjcbkYDE3628@#$%!", "", "2018-12-09T14:19:00+pf:mn", "2018/12/09T14:19:00+00:00", "2018-12-09T99:99:00+00:00", "2018-12-09 14:19:00+00:00", "2018.12.09T14:19:00+00:00", "1990-12-09T14:19:00+00:00", "2058-12-09T14:19:00+00:00", "2018-13-89T14:19:00+00:00"]:
			try:
				datetime.strptime(date_, "%Y-%m-%dT%H:%M:%S%z").date()
				result_flag = True
			except:
				result_flag = False
			self.assertEqual(processor._check_date_format(date_), result_flag)

	def test_process_date(self):
		# Function to test processing of date input. This is only checked for cases that have allowed dates and filenames as disallowed cases are already tested in previous test::test_init()
		print("Performing Tests for CookieLogProcessor._process_date()")
		for date_ in self.correct_dates:
			for filename_ in self.correct_filenames:
				self.args.logfilename, self.args.date = filename_, date_
				if date_ in self.correct_dates and filename_ in self.correct_filenames:
					processor = CookieLogProcessor(self.args)
					self.assertEqual(processor._process_date(date_), datetime.strptime(str(date_), "%Y-%m-%d").date())

	def test_preprocess_line(self):
		# Function to test striping of extra whitespaces before or after the cookie or filename values. Testing is done for all generic test cases
		print("Performing Tests for CookieLogProcessor._preprocess_line()")
		test_cases = [["cookie", "filename"], [" cookie", "filename "], ["\ncookie\t", "	filename 		"], ["	\n 	\n\t\v\fcookie\n", "	filename 		"]]
		for test_ in test_cases:
			self.assertEqual(CookieLogProcessor._preprocess_line(CookieLogProcessor, test_), [test_[0].strip().strip(" ").strip("\n").strip("\v").strip("\f").strip("\t").strip("	"), test_[1].strip().strip(" ").strip("\n").strip("\t").strip("\v").strip("\f").strip("	")])
	
	def test_is_empty_string(self):
		# Function to test empty string
		print("Performing Tests for CookieLogProcessor._is_empty_string()")
		test_cases = ["", " ", "\b", "   ", "a", "	", "a ", ".", "\n", "0"]
		for test_ in test_cases:
			self.assertEqual(CookieLogProcessor._is_empty_string(CookieLogProcessor, test_), not(len(test_)))

	def test_has_whitespace(self):
		# Function to test presence of whitespaces within the string. Testing is done for all generic test cases
		print("Performing Tests for CookieLogProcessor._has_whitespace()")
		test_cases = ["text", "te xt", " text", "t ex t ", "\ntext\t", "\ntext\t ", "\nte xt\t ", "	text 		", "	t ext 		", "	\n 	\n\t\v\ftext\n", "	\n 	\n\t\v\fte xt\n", "te\n\t\v\fxt", "t\n\t\v\fe xt", " tex\n\t\v\ft", "t e\n\t\v\fx t ", "\nte\n\t\v\fxt\t", "\nt\n\t\v\fe xt\t ", "	tex\n\t\v\ft 		", "	t ex\n\t\v\ft 		", "	\n 	\n\t\v\fte\n\t\v\fxt\n", "	\n 	\n\t\v\fte x\n\t\v\ft\n"]
		for test_ in test_cases:
			self.assertEqual(CookieLogProcessor._has_whitespace(CookieLogProcessor, test_), bool(re.search(r'\s', str(test_).strip())))
	
	def test_check_cookie_string_charactersg(self):
		# Function to test that cookie strings/values are only alphanumeric. 
		# Note: In real-life, the cookie strings could consist of other characters, however based on the provide sample this determination has been made
		print("Performing Tests for CookieLogProcessor._check_cookie_string_characters()")
		valid_cases = ["Alphanumeric!#$%&'*+-.^_`|~123", "AlphaNumeric123", "!#$%&'*+-.^_`|~", "MixedCase123", "UPPERCASE123", "AtY0laUfhglK3lC7", "fbcn5UAVanZf6UtG","4sMM2LxV07bPJzwf"]
		invalid_cases = ["Invalid String with Space", "Invalid_String_with_@", " ", "\b\n\t\r\v\f", ""]
		test_cases = list(set(valid_cases).union(set(invalid_cases)))
		for test_ in test_cases:
			if test_ in valid_cases:
				self.assertTrue(CookieLogProcessor._check_cookie_string_characters(CookieLogProcessor, test_), True)
			else:
				self.assertFalse(CookieLogProcessor._check_cookie_string_characters(CookieLogProcessor, test_), False)
	
	def test_skip_entry(self):
		# Function to test if entries with whitespaces, incorrect cookie strings, empty strings or incorrect date formats are skipped or not
		print("Performing Tests for CookieLogProcessor._skip_entry()")
		self.args.logfilename, self.args.date = "cookie_log.csv", "2023-11-14"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7","2018-12-09T14:19:00+00:00"]), False)
		self.assertEqual(processor._skip_entry(["AtY0@laUfhglK3lC7","2018-12-0914:19:00+00:00"]), True)
		self.assertEqual(processor._skip_entry([" AtY0laUfhglK3lC7 	","2018-12-0914:19:00+00:00"]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7"," 2018-12-0914:19:00+00:00 	"]), True)
		self.assertEqual(processor._skip_entry([" AtY0laUfhglK3lC7 	","2018-12-09T14:19:00+00:00"]), False)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7"," 2018-12-09T14:19:00+00:00 	"]), False)
		self.assertEqual(processor._skip_entry(["*","2098-12-0914:19:00+00:00"]), True)
		self.assertEqual(processor._skip_entry(["#ASCFNTHDGFSJKMKR!","1890-12-0914:19:00+00:00"]), True)
		self.assertEqual(processor._skip_entry(["#ASCFNTHDGFSJKMKR!","2018-72-9914:19:00+00:00"]), True)
		self.assertEqual(processor._skip_entry(["ASCFNTHDGFSJKMKR","2018-12-0914:19:00"]), True)
		self.assertEqual(processor._skip_entry(["ASCFNTHDGFSJKMKR","2018-12-0914"]), True)
		self.assertEqual(processor._skip_entry(["","2018-12-09"]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7","2018-12-09-06"]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7 "," 2018- 12-09-06 "]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7 "," 2018/12/09"]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7 "," 2018.12.09"]), True)
		self.assertEqual(processor._skip_entry(["AtY0laUfhglK3lC7 ","Ffdfcvkih"]), True)
		self.assertEqual(processor._skip_entry(["AtY0\n\t\f\vlaUfh glK3lC7","2018-12-09 14:19:00+00:00"]), True)

	def test_get_sorted_mapping(self):
		# Function to test sorting of a dictionary
		print("Performing Tests for CookieLogProcessor._get_sorted_mapping()")
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": 3, "c": 2}), {"a": 1, "c": 2, "b": 3})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": 3, "c": 1}), {"a": 1, "c": 1, "b": 3})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": 3, "c": 2}, True), {"b": 3, "c": 2, "a": 1})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": 3, "c": 1}, True), {"b": 3, "a": 1, "c": 1})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": -3, "c": 2}), {"b": -3, "a": 1, "c": 2})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1, "b": -3, "c": 2}, True), {"c": 2, "a": 1, "b": -3})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1.3, "b": -3, "c": 2.89765}), {"b": -3, "a": 1.3, "c": 2.89765})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": 1.3, "b": -3, "c": 2.89765}, True), {"c": 2.89765, "a": 1.3, "b": -3})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": "a", "b": "c", "c": "b"}), {"a": "a", "c": "b", "b": "c"})
		self.assertEqual(CookieLogProcessor._get_sorted_mapping(CookieLogProcessor, {"a": "a", "b": "c", "c": "b"}, True), {"b": "c", "c": "b", "a": "a"})

	def test_get_maximum_dict_value(self):
		# Function to test if maximum value from the dictionary values is returned or not
		print("Performing Tests for CookieLogProcessor._get_maximum_dict_value()")
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": 1, "b": 3, "c": 2}), 3)
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": 1, "b": 1, "c": 0}), 1)
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": 1, "b": -3, "c": 2}), 2)
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": -1, "b": -3, "c": -2}), -1)
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": 1.3, "b": -3, "c": 2.89765}), 2.89765)
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": "a", "b": "c", "c": "b"}), "c")
		self.assertEqual(CookieLogProcessor._get_maximum_dict_value(CookieLogProcessor, {"a": "c", "b": "c", "c": "c"}), "c")

	def test_get_most_active_cookie(self):
		# Function to test if the most active cookie is returned or not
		print("Performing Tests for CookieLogProcessor.get_most_active_cookie()")
		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2018-12-09"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), ["AtY0laUfhglK3lC7"])

		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2018-12-08"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), ["SAZuXPGUrfbcn5UA", "4sMM2LxV07bPJzwf", "fbcn5UAVanZf6UtG"])

		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2018-12-07"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), ["4sMM2LxV07bPJzwf"])

		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2021-12-07"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), [])

		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2018-10-06"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), [])
		
		# Running only the test case below with empty test_cookie_log.csv will test for the scenario where the file is empty
		self.args.logfilename, self.args.date = "test_cookie_log.csv", "2018-11-07"
		processor = CookieLogProcessor(self.args)
		self.assertEqual(processor.get_most_active_cookie(), [])



if __name__ == "__main__":
	unittest.main()


