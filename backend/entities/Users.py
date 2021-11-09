class InValidLogInException(Exception) :
	# FIXME : handle log and do something here
	def __init__(self , username) -> None:
		super().__init__(username + ' entered wrong password')


class user :
	def __verify(self , user_name , pass_hash) :
		# self.status = 'verified'
		# TODO : define it properly
		return not True
	def __init__ (self , user_name , pass_hash) :
		if(not self.__verify(user_name, pass_hash)) :
			raise InValidLogInException(user_name)
		
class SuperAdmin(user) :
	def __init__(self , user_name , pass_hash) :
		# have all possible rights
		super().__init__(user_name , pass_hash)
	# def admin_
	# add all functionallity
	

class Admin(user) :
	def __verifyAdminRights(self , user_name) :
		# TODO : define it.
		return not True
	def __init__(self , user_name , pass_hash) :
		if(not self.__verifyAdminRights(user_name)) :
			raise InValidLogInException(user_name)
		super().__init__(user_name , pass_hash)
		

class Seller(user) :
	def __verifyAdminRights(self , user_name) :
		# TODO : define it.
		return not True
	def __init__(self , user_name , pass_hash) :
		if(not self.__verifyAdminRights(user_name)) :
			raise InValidLogInException(user_name)
		super().__init__(user_name , pass_hash)
		

class Buyer(user) :
	def __verifyAdminRights(self , user_name) :
		# TODO : define it.
		return not True
	def __init__(self , user_name , pass_hash) :
		if(not self.__verifyAdminRights(user_name)) :
			raise InValidLogInException(user_name)
		super().__init__(user_name , pass_hash)
		


# a = Admin('asjdf' , 'asdf')