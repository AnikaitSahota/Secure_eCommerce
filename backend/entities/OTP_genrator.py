import random

def get_OTP(random_timebased_seed_flag = False , num_digit = 6) :

	if(random_timebased_seed_flag) :
		# random.seed(hash())
		pass


	OTP = ''
	for i in range(num_digit) :																	# selecting required number of digits for OTP from rand_num
		OTP += str(random.randint(0,9))																# using this way; we will have more unique possible OTPs as we are including non-contiguous and rearranged OTPs
		
	return OTP																						# returning OTP
	



def OTP_genrator(print_flag = 0 , OTP_count = 100) -> float :
	"""since we could not import 2018016_2_a becuse literals in python should not start with numericals;
		hence I have dumped all code from that file into this function which returns the computational time

	Parameters
	----------
	print_flag : int, optional
		dectats verbosity, by default 0
	OTP_count : int, optional
		number of OTPs required

	Returns
	-------
	float
		computational time taken by algorithm
	"""
	# random.seed(0)																						# optional ; for regenrating same OTPs

	def genrate_random_num(num_digits : int) -> str :
		"""function to genrate a random number with num_digits in it.
		if num_digits == 1 ; then 0 to 9 are valid outputs

		Parameters
		----------
		num_digits : int
			number of required digits in random number

		Returns
		-------
		str
			random number with num_digits in it.
		"""
		rand_num = str(random.randint(0 , 10**num_digits -1))											# genrating random number in range [0 , 10**num_digits)
		# rand_num = str(random.randint(10**(num_digits-1) , 10**num_digits -1))						# genrating random number in range [10**(num_digits-1) , 10**num_digits)
		return '0'*(num_digits - len(rand_num)) + rand_num												# adding prefix of '0's if number have less than num_digits digits; and returning the final string


	def generate_OTP(rand_num : str , OTPnum_digits : int = 6) -> str :
		"""function to genrate a OTP containing OTPnum_digits digits from rand_num

		Parameters
		----------
		rand_num : str
			a large random integer in string, from which OTP will be genrated
		OTPnum_digits : int, optional
			exact number of digits OTP must contain, by default 6

		Returns
		-------
		str
			random OTP having OTPnum_digits
		"""
		rand_num_digits = len(rand_num)																	# number of digits available in large random interger
		OTP = ''
		for i in range(OTPnum_digits) :																	# selecting required number of digits for OTP from rand_num
			OTP += rand_num[random.randint(0,rand_num_digits-1)]										# using this way; we will have more unique possible OTPs as we are including non-contiguous and rearranged OTPs
		
		return OTP																						# returning OTP


	# start_time = time.time()																			# storing the start time, for furthur calculating the execution time
	rand_num = genrate_random_num(1023)
	# print(rand_num)

	##### code for genrating a single OTP 
	# OTP = generate_OTP(rand_num)
	# print(OTP)


	#### code for genrating 100 OTPs
	OTPs = set()

	while(len(OTPs) < OTP_count) :
		OTPs.add(generate_OTP(rand_num))
	
	if(print_flag == 1) :
		print('Printing' , len(OTPs) , 'unique OTPs')
		for OTP in OTPs :
			print(OTP)

	# computational_time = time.time() - start_time
	# if(print_flag == 2) :
	# 	print(computational_time , 'seconds')															# estimated time for genrating 1 OTP (i.e, 2A) is 0.0003261566162109375 seconds
	# return computational_time


