
class CustomError(BaseException):
	'''
	Custom error class. This class has been added to raise exceptions, display custom error message on the console.
	'''
	
	def __init__(self, message="A custom error occurred!"):
		self.message = message
		# print(self.message)
		super().__init__(self.message)