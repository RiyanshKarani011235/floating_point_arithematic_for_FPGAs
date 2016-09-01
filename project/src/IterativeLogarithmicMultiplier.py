#!/usr/bin/Python
from Float import Float
import utils

class IntegerIterativeLogarithmicMultiplier() : 
	"""Python implementation of the Iterative Logarithmic Multipler

	Based on work by Zdenka Babic, Aleksej Avramovic and Patricio Bulic	
	.. _An Iterative Logarithmic Multiplier
	   http://ev.fe.uni-lj.si/1-2010/Babic.pdf
	
	Methods: 
		multiply
		p0_approx
		vaildateBinary
		priorityEncoder
		decoder
		clearBit
		shiftLeft
		add

	"""

	""" 
	TODO : 
		wherever int(blah, base=2) is used, replace it with logic
		make the documentation strings more consistent
		make the documentation strings more mathematically rich (explain the concepts)
		add examples for all the non obvious methods of this class	
		make error strings more informative
	"""

	def __init__(self) : 
		pass

	def multiply(self, n1, n2, correctionIterations=1) : 
		"""Multiply two floating point numbers using the Iterative Logarithmic Multiplier algorithm

		Args: 
			n1 (str) -- binary string representing an integer n1
			n2 (str) -- binary string representing an integer n2
			correctionIterations (int) -- number of correction terms to use in the
				implementation of the Iterative Logarithmic Multiplier

		Returns: 
			str -- A binary string representing an approximate value of n1*n2
				correct upto (correctionIterations) number of correction terms

		Raises:
			ValueError -- if n1, n2 are not strings
			ValueError -- if n1, n2 are not valid binary strings
			ValueError -- if correctionIterations is not an `int`

		"""

		if not isinstance(n1, str) or not isinstance(n2, str) : 
			raise ValueError('n1 and n2 should be an instances of Float')

		if not self.validateBinary(n1) or not self.validateBinary(n2) : 
			raise ValueError('n1 and n2 should be valid binary strings')

		if type(correctionIterations) != int : 
			raise ValueError('correctionIterations should be an integer')

		product = '0'
		# print('===============================')
		# print(int(n1, base=2) * int(n2, base=2))
		for iterationNumber in range(correctionIterations) : 
			# print('--------------------------------')
			# print(n1 + ' : ' + n2)
			# calculate k1 and k2
			k1 = int(self.priorityEncoder(n1), base=2)
			k2 = int(self.priorityEncoder(n2), base=2)

			# calculating approximate value
			p0_approx = self.p0_approx(n1, n2)
			# print('p0_approx : ' + str(int(p0_approx, base=2)))

			# adding error term to the approx value
			product = self.add(product, p0_approx)
			if product[1] == '1' : 
				product = '1' + product[0]
			else : 
				product = product[0]
			# print(len(product))

			# n1 and n2 for the next iteration
			n1 = self.clearBit(n1, k1)
			n2 = self.clearBit(n2, k2)

			if int(n1, base=2) == 0 or int(n2, base=2) == 0 : 
				break
		return product

	def p0_approx(self, n1, n2) : 
		"""Generate the first approximation of n1*n2

		If k1 is the index of the 1st bit from left in n1 with value 1
		If k2 is the index of the 1st bit form left in n2 with value 1

		p0_approx = 2**(k1+k2) + (2**k2)*(n1 - 2**k1) + (2**k1)*(n2 - 2**k2)

		Args: 
			n1 (str) -- binary string representing an integer n1
			n2 (str) -- binary string representing an integer n2
			correctionIterations (int) -- number of correction terms to use in the
				implementation of the Iterative Logarithmic Multiplier

		Returns: 
			str -- A binary string representing the first approximation of n1*n2

		"""

		assert self.validateBinary(n1)
		assert self.validateBinary(n2)

		_p0_1 = self._p0_1(n1, n2)
		_p0_2 = self._p0_2(n1, n2)
		_p0_3 = self._p0_3(n1, n2)
		t1 = self.add(self._p0_1(n1, n2), self._p0_2(n1, n2))
		if t1[1] == '1' : 
			t1 = '1' + t1[0]
		else :
			t1 = t1[0]
		t2 = self.add(self._p0_3(n1, n2), t1)
		if t2[1] == '1' : 
			t2 = '1' + t2[0]
		else : 
			t2 = t2[0]
		return t2

	def _p0_1(self, n1, n2) : 
		"""Find 2**(k1+k2)
		"""	

		k1 = self.priorityEncoder(n1)
		k2 = self.priorityEncoder(n2)
		k12 = self.add(k1, k2)
		k12 = k12[1] + k12[0] 	# carry + sum
		_p0_1 = self.decoder(k12)
		return _p0_1

	def _p0_2(self, n1, n2) :
		"""find (2**k2)*(n1 - 2**k1)
		"""	

		# k2
		t1 = self.priorityEncoder(n2)
		# n1 - 2**k1
		t2 = self.clearBit(n1, int(self.priorityEncoder(n1), base=2))
		_p0_2 = self.shiftLeft(t2, int(t1, base=2), len(n1) + len(n2))
		return _p0_2

	def _p0_3(self, n1, n2) : 
		"""find (2**k1)*(n2 - 2**k2)
		"""	

		# k2
		t1 = self.priorityEncoder(n1)
		# n2 - 2**k2
		t2 = self.clearBit(n2, int(self.priorityEncoder(n2), base=2))
		_p0_3 = self.shiftLeft(t2, int(t1, base=2), len(n1) + len(n2))
		return _p0_3

	def validateBinary(self, n) : 
		"""check if a binary string n is a valid binary string

		Args : 
			n(str) -- a binary string (without the prefix 0b)

		Returns : 
			boolean -- True if n is a valid bianry String, else False

		"""	

		assert isinstance(n, str)
		if len(n) == 0 : 
			return False

		for element in n : 
			if element != '0' and element != '1' : 
				return False
		return True

	def priorityEncoder(self, n) : 
		"""Returns the index of the first bit of `n` from left whose value is `1`

		Args : 
			n(str) -- a valid binary String

		Returns : 
			str -- binary value of the index of first bit of `n` from the left whose value is `1`

		"""	

		assert self.validateBinary(n) == True
		minNumberOfEncodedBits = 1
		while 2**minNumberOfEncodedBits < len(n) : 
			minNumberOfEncodedBits += 1

		for i in range(len(n)) : 
			j = i
			if n[i] == '1' :
				break

		encodedValue = bin(len(n) - j - 1)[2:]

		encodedValue = (minNumberOfEncodedBits - len(encodedValue))*'0' + encodedValue
		return encodedValue

	def decoder(self, n) : 
		"""Returns the decoded value of the number represented by the binary string n

		Args :
			n(str) -- binary string

		Returns 
			str -- binary string representing the decoded value of number represented by n

		"""	

		assert self.validateBinary(n) == True
		numberOfDecodedBits = 2**(len(n))
		encodedValue = bin(2**(int(n, base=2)))[2:]
		encodedValue = (numberOfDecodedBits - len(encodedValue))*'0' + encodedValue
		return encodedValue

	def clearBit(self, n, bitNumber) : 
		"""Clears the bit number `bitNumber` of the binary string n

		Args : 
			n(str) -- a valid binary number
			bitNumber(int) -- a valid bitNumber of the binary string n

		Raises : 
			AssertionError -- if bitNumber is less that 0 or greater the index of MSB of n

		"""

		assert self.validateBinary(n)
		assert type(bitNumber) == int
		assert bitNumber >= 0
		assert bitNumber < len(n)
		bitToClear = len(n) - bitNumber - 1
		return n[:bitToClear] + '0' + n[bitToClear+1:]

	def shiftLeft(self, n, bitsToShift, numberOfBitsInResult=None) :
		"""Left shifts the binary value represented by binary string `n`, by `bitsToShift` places 

		Args : 
			n(str) -- a valid binary string
			bitsToShift(int) -- value by which you wish to left shift the number represented by `n`
			numberOfBitsInResult(int) -- length of the result string

		Note : 
			if numberOfBitsInRestult is shorter than the result generated, the left most
			bits will be truncated
	
		Returns : 
			str -- left shifted value of `n`
			
		"""

		assert self.validateBinary(n)
		assert bitsToShift >= 0
		shiftedValue = bin(int(n, base=2)*(2**bitsToShift))[2:]
		if numberOfBitsInResult == None : 
			numberOfBitsInResult = len(n)
		if len(shiftedValue) <= numberOfBitsInResult : 
			shiftedValue = (numberOfBitsInResult - len(shiftedValue))*'0' + shiftedValue
		else : 
			shiftedValue = shiftedValue[len(shiftedValue) - numberOfBitsInResult:]
		return shiftedValue

	def add(self, n1, n2) : 
		"""Adds two binary numbers n1 and n2

		Args : 
			n1(str) -- a valid binary string
			n2(str) -- a valid binary string

		Returns : 
			str -- A binary string representing the sum of n1 and n2

		"""

		assert self.validateBinary(n1)
		assert self.validateBinary(n2)

		sum_ = bin(int(n1, base=2) + int(n2, base=2))[2:]
		carry = '0'
		sumLength = max(len(n1), len(n2))
		assert len(sum_) <= sumLength + 1
		if len(sum_) <= sumLength : 
			sum_ = (sumLength -len(sum_))*'0' + sum_
		else : 
			carry = sum_[0]
			sum_ = sum_[1:]
		return [sum_, carry]

class FixedWidthIntegerMultiplier() : 
	""" Subclass of IntegerIterativeLogarithmicMultiplier for fixed width inputs

	Implement Stricter constraints for the IntegerIterativeLogarithmicMultiplier 
	with respect to number of input bits, number of result bits, etc.
	"""	

	def __init__(self, inputBits, outputBits, correctionIterations=1) :
		"""
		Args :
			inputBits(int) -- width of the binary string representing the numbers
				input to the multiplier
			outputBits(int) -- width of the binary string representing the output
				of the multiplier
			correctionIterations(int) -- number of correction terms to use in the 
				implementation of iterative logarithmic multiplier

		Raises : 
			ValueError -- If inputBits is not an integer
			ValueError -- If outputBits is not an integer
			ValueError -- If correctionIterations is not an integer > 0

		"""

		if type(inputBits) != int : 
			raise ValueError('"inputBits" should be an integer')
		if type(outputBits) != int : 
			raise ValueError('"outputBits" should be an integer')
		if type(correctionIterations) != int : 
			raise ValueError('"correctionIterations" should be an integer')
		if not correctionIterations > 0 : 
			raise ValueError('"correctionIterations" should be an integer > 0')

		self.inputBits = inputBits
		self.outputBits = outputBits
		self.correctionIterations = correctionIterations
		self.multiplier = IntegerIterativeLogarithmicMultiplier()

	def multiply(self, n1, n2) : 
		"""multipliers two numbers represented by binary strings n1 and n2

		Args : 
			n1(str) -- a valid binary string of width `inputBits`
			n2(str) -- a vaild binary string of width `inputBits`

		Returns : 
			str -- a binary string representing the product of n1 and n2
				of width `outputBits`

		Note : 
			If `outputBits` is less than the width of the resultant binary string
			generated, the rightmost bits will be truncated

		Raises :
			ValueError -- If width of n1 is not `inputBits`
			ValueError -- If width of n2 is not `inputBits`
	
		"""

		if type(n1) != str : 
			raise ValueError('invalid type "{0}" for n1, should be a string'.format(type(n1)))
		if type(n2) != str : 
			raise ValueError('invalid type "{0}" for n2, should be a string'.format(type(n2)))

		if not self.multiplier.validateBinary(n1) : 
			raise ValueError('"n1" is not a valid binary number')
		if not self.multiplier.validateBinary(n2) : 
			raise ValueError('"n2" is not a valid binary number')

		if len(n1) != self.inputBits : 
			raise ValueError('width of n1 should be "{0}" bits, but is "{1}" bits'.format(self.inputBits, len(n1)))		
		if len(n2) != self.inputBits : 
			raise ValueError('width of n1 should be "{0}" bits, but is "{1}" bits'.format(self.inputBits, len(n1)))

		output = self.multiplier.multiply(n1, n2, self.correctionIterations)
		output = self.truncateMostSignificantZeros(output)
		assert len(output) <= self.outputBits
		if len(output) > self.outputBits : 
			output = output[:self.outputBits]
		else : 
			output = '0'*(self.outputBits - len(output)) + output
		return output

	def truncateMostSignificantZeros(self, n) : 
		zerosFlag = True
		returnValue = ''
		for i in range(len(n)) : 
			if n[i] == '1' :
				if zerosFlag : 
					zerosFlag = False 
				returnValue += n[i]
			else : 
				if not zerosFlag : 
					returnValue += n[i]
		return returnValue

class FloatingPointIterativeLogarithmicMultiplier() : 

	def __init__(self, length=32, correctionIterations=1) : 
		"""
		Args : 
			length(int) -- length of the floating point number on which the
				multiplier needs to operate
			correctionIterations(int) -- number of correction terms to use in 
				the implementation of the iterative logarithmic multiplier

		Raises : 
			bitstring.CreationError -- if length is not 32 or 64
			ValueError -- if correctionIterations is not an integer > 0

		"""

		Float(length=length) 	# assert that length is correct
		self.integerMultiplier = FixedWidthIntegerMultiplier(length, length*2, correctionIterations)

	def multiply(self, f1, f2) : 
		"""Multiplies two `Float` instances

		Takes two `Float` instances as an input and generates a new `Float`
		instance with its value equal to f1.val * f2.val

		Args : 
			f1(Float) -- First number
			f2(Float) -- Second number

		Returns : 
			Float -- Float instance with its value equal to f1.val * f2.val

		Raises : 
			ValueError -- if either f1 or f2 is not a `Float` instance

		"""

		if not isinstance(f1, Float) : 
			raise ValueError('f1 should be a "Float" instance')
		if not isinstance(f2, Float) : 
			raise ValueError('f2 should be a "Float" instance')

		if f1.length != f2.length : 
			raise ValueError('f1 and f2 should be both of the same floating point format')

	def getBinarySignificand(self, f) : 
		assert isinstance(f, Float)
		return '1' + f.raw_mantissa