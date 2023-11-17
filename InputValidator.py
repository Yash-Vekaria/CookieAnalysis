from CustomError import CustomError
from datetime import datetime
import os



class InputValidator():
	'''
	Custom class to maintain and validate inputs.
	'''
	
	def __init__(self):
		self.error_message = ""


	def validate_filename(self, logfilename):
		'''
		Validating input cookie log filename
		Input: 
			logfilename::str -- command line argument of the cookie log filename
		Output: 
			bool -- Returns True to caller if logfile is successfully validated else returns False.
			error_message::str -- Return appropriate message in case validation is unsuccessful else None
		'''

		logfilename = str(logfilename).strip()
		
		# Validating if log file argument is not provided by the user. 4 characters are used by ".csv", so len(filename) should be 5 or more
		if len(logfilename) < 5:
			# raise CustomError("Filename not provided!")
			self.error_message = "ERROR: Filename not provided!"
			return False, self.error_message
		
		# Validating if incorrect log file is provided by the user
		if not(logfilename.endswith(".csv")):
			# raise CustomError("Provided logfile has incorrect filetype! .csv required!")
			self.error_message = "ERROR: Provided logfile has incorrect filetype! .csv required!"
			return False, self.error_message

		# Validating if the file exists in the current directory
		if not(os.path.exists(os.path.join(os.getcwd(), logfilename))):
			# raise CustomError(f"The cookie log file does not exist in the current working directory. Move the file to: {os.getcwd()}")
			self.error_message = f"ERROR: The cookie log file does not exist in the current working directory. Move the file to: {os.getcwd()}"
			return False, self.error_message
		
		return True, None


	def validate_date(self, date):
		'''
		Validate input query date
		Input:
			date::str -- command line argument of queried date
		Output:
			bool -- Returns True to caller if date is successfully validated else returns False
			error_message::str -- Return appropriate message in case validation is unsuccessful else None
		'''

		date = str(date).strip()

		# Validating if incorrect date format is input by the user
		if "-" not in date:
			# raise CustomError("Provided date is incorrect! It should be in YYYY-MM-DD format!")
			self.error_message = "ERROR: Provided date is incorrect! It should be in YYYY-MM-DD format!"
			return False, self.error_message
		else:
			date_split = date.split("-")
			if len(date_split) != 3:
				# raise CustomError("Provided date is incorrect! It should be in YYYY-MM-DD format!")
				self.error_message = "ERROR: Provided date is incorrect! It should be in YYYY-MM-DD format!"
				return False, self.error_message
			else:
				if len(date_split[1])!=2 or len(date_split[2])!=2 or len(date_split[0])!=4:
					# raise CustomError("Provided date is incorrect! It should be in YYYY-MM-DD format!")
					self.error_message = "ERROR: Provided date is incorrect! It should be in YYYY-MM-DD format!"
					return False, self.error_message

		# Validating if incorrect date format is input by the user
		if len(date) != 10:
			# raise CustomError("Provided date is incorrect! It should be in YYYY-MM-DD format!")
			self.error_message = "ERROR: Provided date is incorrect! It should be in YYYY-MM-DD format!"
			return False, self.error_message
		
		# Validating if entered date is valid (i.e., year, month and day takes valid realistic values)
		try:
			valid_date = datetime.strptime(date, "%Y-%m-%d")
			# Fetching current date and time and obtaining the difference between the two for a future test case below
			current_date = datetime.now()
			date_difference = valid_date - current_date
			seconds_difference = date_difference.total_seconds()
		except ValueError:
			# raise CustomError("ValueError: The entered date is not valid! Enter the date in YYYY-MM-DD format!")
			self.error_message = "ERROR: ValueError: The entered date is not valid! Enter the date in YYYY-MM-DD format!"
			return False, self.error_message
		
		# Validating if the queried date is not before 1944 as ookies were first introduced in the web in 1994, so the log file should not be queried with a date before 1994.
		if valid_date.date().year < 1994:
			# raise CustomError("At the entered date, cookies did not exist in the web! Please enter an appropriate date!")
			self.error_message = "ERROR: At the entered date, cookies did not exist in the web! Please enter an appropriate date!"
			return False, self.error_message

		# Validating if the queried date is a future date as cookies should not be queried for a future date as they will not exist in the data. 5 secs difference check is added to cover querying close to midnight.
		if (valid_date > current_date) and (seconds_difference > 5):
			# raise CustomError("The entered date is a date in future! Enter an appropriate date to query!")
			self.error_message = "ERROR: The entered date is a date in future! Enter an appropriate date to query!"
			return False, self.error_message
		
		return True, None
