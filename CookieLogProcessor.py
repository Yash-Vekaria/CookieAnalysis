from datetime import datetime
import re
import os

from InputValidator import InputValidator
from CustomError import CustomError



class CookieLogProcessor():
	'''
	Class to process input cookie log file.
	'''

	def __init__(self, args):
		'''
		Class constructor to validate command line arguments and set datetime_format, query_date, logfilename and filepath if validations are True, else None object is returned
		Input:
			args::namespace -- command line arguments
			args.date::str -- queried date
			args.logfilename::str -- cookie log filename
		'''
		self.error_message = ""
		if self._validate_commandline_inputs(args.date, args.logfilename):
			self.datetime_format = "%Y-%m-%d"
			self.query_date = self._process_date(args.date)
			self.logfilename = args.logfilename
			self.filepath = os.path.join(os.getcwd(), self.logfilename)
		else:
			raise CustomError(f"Class::CookieLogProcessor() creation failed due to: {self.error_message}")


	def _validate_commandline_inputs(self, date, filename):
		'''
		Validates command line input arguments using InputValidator object and returns True if they are both valid, else False
		Input: 
			date::str -- command line argument of queried date
			filename::str -- command line argument of the cookie log filename
		Output:
			bool -- boolean result of whether the command line arguments are valid or not
		'''
		# Creating InputValidator object
		validator = InputValidator()

		# Perform cookie logfile name validation
		filename_validation_flag, self.error_message = validator.validate_filename(filename)

		# Perform query date validation
		date_validation_flag, self.error_message = validator.validate_date(date)
		
		# Return True if both date and filename are valid
		return filename_validation_flag and date_validation_flag


	def _read_logfile(self):
		'''
		Reads cookie logfile
		Input: NA
		Output:
			data::list -- containing each line in file as a list item
		'''
		file_pointer = open(self.filepath, "r")
		file_data = file_pointer.read().strip()
		file_pointer.close()
		
		# Obtaining the logfile data as a list, ignoring the header on the first line
		data = file_data.split("\n")[1:] if len(file_data.split("\n")) > 0 else []
		return data


	def _process_date(self, date):
		'''
		Parse the date string in appropriate format. self.datetime_format is updated within any function based on the requirement
		Input:
			date::str -- date string
		Ouput: 
			date::datetime
		'''
		return datetime.strptime(str(date), self.datetime_format).date()


	def _check_date_format(self, date):
		'''
		Checks if the date is in correct format by trying to parse it without error. Returns True if parsed successfully
		Input: 
			date::str -- date string
		Output:
			bool -- boolean result of whether the datetime timestamp is in correct format
		'''
		try:
			# Attempting to parse the date
			date = self._process_date(date)
		except:
			# The date corresponding to the current entry is not in the required datetime format, hence skipping it
			return False
		return True


	def _preprocess_line(self, array):
		'''
		Preprocess the input line by striping any whitespace at the beginning or the end of the string
		Input: 
			array::list -- array of [cookie string, datetime string]
		Output: Pre-processed line array (list)
		'''
		return [str(array[0]).strip(), str(array[1]).strip()]


	def _is_empty_string(self, input_string):
		'''
		Check if the input string is of length zero
		Input: 
			input_string::str -- string to check
		Output:
			bool -- boolean result of whether the string is empty
		'''
		return True if len(str(input_string)) == 0 else False


	def _has_whitespace(self, input_string):
		'''
		Check if the input string consists of any whitespaces
		Input: 
			input_string::str -- string to check
		Output:
			bool -- boolean result of whether the string has whitespaces in between
		'''
		return bool(re.search(r'\s', str(input_string).strip()))


	def _check_cookie_string_characters(self, input_string):
		'''
		Check if cookie string contains any characters other than a-zA-Z0-9!#$%&'*+-.^_`|~ (disallowing empty string) and return False if it contains any other characters
		RFC 6265: http://www.ietf.org/rfc/rfc6265.txt
		Input: 
			input_string::str -- cookie string to check for containing valid characters
		Output: 
			bool -- boolean result of whether cookie string is valid or not as per RFC 6265 allowed characters
		'''
		# return bool(re.match("[a-zA-Z0-9]+$", str(input_string)))
		return bool(re.match("[a-zA-Z0-9!#$%&'*+-.^_`|~]+$", str(input_string)))


	def _skip_entry(self, line):
		'''
		Checks if a given line in the cookie log file should be skipped due to some issue or parsed. In case of any issue, True is returned.
		Input: 
			line::list -- a line from cookie log file as a list of length two (cookie and timestamp)
		Output: 
			bool -- True is entry is to be skipped else False
		'''
		# Skip the current line if its cookie contains whitespaces or cookie string is empty
		if self._has_whitespace(line[0].strip()) or self._is_empty_string(line[0].strip()):
			return True

		# Skip the current line if its date contains whitespaces or date string is empty
		if self._has_whitespace(line[1].strip()) or self._is_empty_string(line[1].strip()):
			return True

		# Skip the current line if the cookie string has any non-alphanumeric characters
		if not(self._check_cookie_string_characters(line[0].strip())):
			return True

		self.datetime_format = "%Y-%m-%dT%H:%M:%S%z"
		# Skips the current line if date is not in correct format
		if not(self._check_date_format(line[1].strip())):
			return True

		return False


	def _get_sorted_mapping(self, mapping, reverse_ordering=False):
		'''
		Sorts the input dictionary by values based on the passed ordering
		Input: 
			mapping::dict -- dictionary to be sorted by values
			reverse_ordering::bool (default=False) -- order in which dictionary is to be sorted
		Output: sorted dictionary (dict)
		'''
		return dict(sorted(mapping.items(), key=lambda item: item[1], reverse=reverse_ordering))


	def _get_maximum_dict_value(self, input_dict):
		'''
		Returns the maximum value of the dictionary
		Input: 
			input_dict::dict -- dictionary to obtain the max value from
		Output: Maximum value corresponding to any key (int)
		'''
		return max(input_dict.values())


	def get_most_active_cookie(self):
		'''
		Extracts the most active cookie from the logfile (i.e. file_data) corresponding to the queried date (i.e., self.query_date)
		Input: NA
		Output: 
			most_active_cookies::list -- containing all most active cookies corresponding to the input query date
		'''
		# Defining datetime format expected
		self.datetime_format = "%Y-%m-%dT%H:%M:%S%z"
		
		# Variable to store date to cookie map along with number of occurences of each cookie on a given day
		cookie_map = {}
		# Variable to store most active cookies for queried date
		most_active_cookies = []
		# Variable to store cookie log file contents
		data = []

		# Read the cookie logfile a
		data = self._read_logfile()
		if len(data) == 0:
			# raise CustomError("Input cookie logfile is empty!")
			print("ERROR: Input cookie logfile is empty!")
			return []
	
		# Parse the timestamp string (with timezone) into a date object and associate it with cookie
		for entry in data:
			
			# Selecting the first two items: cookie and datetime in case some line comprises of more than two items
			if "," not in entry:
				continue
			items = self._preprocess_line(entry.split(",")[:2])

			# Check if the line has valid entries
			if self._skip_entry(items):
				continue

			cookie = items[0]
			date = self._process_date(items[1])
			
			if date not in cookie_map.keys():
				cookie_map[date] = {}
			if cookie not in cookie_map[date].keys():
				cookie_map[date][cookie] = 0
			cookie_map[date][cookie] += 1

		# print(cookie_map[self.query_date])
		if self.query_date not in cookie_map.keys():
			# This condition will be satisfied when there are no cookies corresponding to the queried date in the log file
			# In that case just return empty list
			return most_active_cookies

		# Sort the sub-dictionary within the cookie_map corresponding to the query date based on values of sub-dictionary in descending order
		sorted_cookie_map = self._get_sorted_mapping(cookie_map[self.query_date], reverse_ordering=True)

		# Extract the count of the highest occurences of any cookie on the queried date
		highest_frequency = self._get_maximum_dict_value(sorted_cookie_map)
		
		# Collecting all cookies whose frequency of occurence is equal to the highest_frequency
		for cookie_key in sorted_cookie_map.keys():
			if int(sorted_cookie_map[cookie_key]) == highest_frequency:
				most_active_cookies.append(cookie_key)
			else:
				break;

		return most_active_cookies


	def print_most_active_cookie(self):
		'''
		Prints the most active cookie values
		Input: NA
		Output: NA
		'''
		cookies = self.get_most_active_cookie()
		for cookie in cookies:
			print(cookie)
		return