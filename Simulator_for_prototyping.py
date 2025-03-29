import os

#Global Variables
RD1 = 0
RD2 = 0
immExt = ""
ALUResult = ""
# PCNext=0
ReadValue=0
RegWrite = 0
RegReturn = 0
MemWrite = 0
pc = 0
Data_memory=[0]*128 #starts from 65536 and ends at 65663(included)
Stack_memory = [0]*128 #starts from 256 and ends at 383(included)
zero = False #flag for b-type instruction
dict_instructions = {}
register_after_inst=[]
# registers = {"00000" : x0, "00001" : x1, "00010" : x2, "00011" : x3, "00100" : x4, "00101" : x5, "00110" : x6, "00111" : x7, "01000" : x8, "01001" : x9, "01010" : x10, "01011" : x11, "01100" : x12, "01101" : x13, "01110" : x14, "01111" : x15, "10000" : x16, "10001" : x17, "10010" : x18, "10011" : x19, "10100" : x20, "10101" : x21, "10110" : x22, "10111": x23, "11000" : x24, "11001" : x25, "11010" : x26, "11011" : x27, "11100" : x28, "11101" : x29, "11110" : x30, "11111": x31}

registers = {"00000" : 0, "00001" : 0, "00010" : 0, "00011" : 0, "00100" : 0, "00101" : 0, "00110" : 0, "00111" : 0, "01000" : 0, "01001" : 0, "01010" : 0, "01011" : 0, "01100" : 0, "01101" : 0, "01110" : 0, "01111" : 0, "10000" : 0, "10001" : 0, "10010" : 0, "10011" : 0, "10100" : 0, "10101" : 0, "10110" : 0, "10111": 0, "11000" : 0, "11001" : 0, "11010" : 0, "11011" : 0, "11100" : 0, "11101" : 0, "11110" : 0, "11111": 0}
pc_values = []


def reset():
	global registers, Data_memory, Stack_memory
	for i in registers:
		registers[i] = 0
	registers["00010"] = 380
	Data_memory=[0]*128
	Stack_memory = [0]*128

def int_to_binary(num, bit):
    return format(num & (2**bit - 1), f"0{bit}b")

def control_unit(opcode, funct3, funct7):
	global zero
	signals = {"PCSrc": "0", "ResultSrc": "XX", "MemWrite": "0", "ALUControl": "000", "ALUSrc": "0", "ImmSrc": "00", "RegWrite": "0"}
	
	if opcode == "0110011": #R-type
		signals["RegWrite"] = "1"
		signals["ResultSrc"] = "00"
		if funct7 == "1":
			if funct3 == "000":
				signals["ALUControl"] = "001" #subtract
		elif funct7 == "0":
			if funct3 == "000":
				signals["ALUControl"] = "000" #add
			elif funct3 == "111":
				signals["ALUControl"] = "010" #and
			elif funct3 == "110":
				signals["ALUControl"] = "011" #or
			elif funct3 == "010":
				signals["ALUControl"] = "101" #SLT
			elif funct3 == "101":
				signals["ALUControl"] = "111" #SRL #111 is added by me and not real value

	elif opcode == "0010011":  #addi
		signals["ALUSrc"] = "1"
		signals["RegWrite"] = "1"
		signals["ResultSrc"] = "12"

		# if funct3 == "000":
		signals["ALUControl"] = "000"
		# elif funct3 == "110":
		# 	signals["ALUControl"] = "011"
		# elif funct3 == "111":
		# 	signals["ALUControl"] = "010"

	elif opcode == "0000011":  #LW
		signals["ResultSrc"] = "01"
		signals["ALUSrc"] = "1"
		signals["RegWrite"] = "1"
		# signals["PCSrc"] = "1"

	elif opcode == "0100011":  #SW
		signals["MemWrite"] = "1"
		signals["ALUControl"] = "010"
		signals["ALUSrc"] = "1"
		signals["ImmSrc"] = "01"

	elif opcode == "1100011":  #Branch
		signals["ALUControl"] = "001"
		signals["ImmSrc"] = "10"
		signals["ResultSrc"] = "00"

		if funct3 == "000":
			if zero == True:
				signals["PCSrc"] = "1"
			else:
				signals["PCSrc"] = "0"

		elif funct3 == "001":
			if zero == True:
				signals["PCSrc"] = "1"
			else:
				signals["PCSrc"] = "0"
		
		elif funct3 == "100":
			if zero == True:
				signals["PCSrc"] = "1"
			else:
				signals["PCSrc"] = "0"

	elif opcode == "1101111":  #j-type
		signals["RegWrite"] = "1"
		signals["PCSrc"] = "1"
		signals["ImmSrc"] = "11"
		signals["ResultSrc"] = "10"
		signals["ALUSrc"] = "1"
	
	elif opcode == "1100111":  #jalr-type
		signals["RegWrite"] = "1"
		signals["PCSrc"] = "1"
		signals["ImmSrc"] = "00"
		signals["ResultSrc"] = "11"
		signals["ALUSrc"] = "1"

	return signals

def Instruction_Memory(inst):
	instr={"op":inst[25:32],"func3":inst[17:20],"func7":inst[1],"A1":inst[12:17],"A2":inst[7:12],"A3":inst[20:25],"Extend":inst[0:25]}
	return instr
# 00000000011110100000101000010011
def PCNext(PCSrc,op="X"):
	global immExt
	global pc
	if PCSrc=="1":
		if (op == "1101111"):
			pc=pc+signed(immExt)
			if (pc % 2 == 1):
				pc -= 1
		elif (op == "1100111"):
			pc = signed(immExt)
			if (pc % 2 == 1):
				pc -= 1
		else:
			pc = pc + signed(immExt)
	elif PCSrc=="0":
		pc=pc+4
	# return PC

def PC(instruction):
	global dict_instructions
	PC = 0 #initialising PC with zero
	for i in instruction:
		dict_instructions[PC] = i
		PC += 4
	# dict_instructions[PC] = False
	
def mux(input1,input2,input3,ch1):
	if(ch1=='00'):
		return input1
	elif(ch1=='01'):
		return input2
	else:
		return input3
		
def signed(inp):
	#signed integer representation of binary
	if (inp[0] == '1'): #represents 2's complement
		new = ""
		for i in inp: #flip the bits
			if i == '1':
				new += '0'
			else: new += '1'
		return -(int(new, 2) + 1) #add 1
	else:
		return int(inp, 2)
		
def register_file(A1, A2, A3, WD3, WE3, clk=True):
	global RD1, RD2, registers
	RD1 = registers[A1]
	RD2 = registers[A2]
	
	if (WE3 == 1): registers[A3] = int(WD3, 2)

def extend(inp, immSrc):
	#31:7
	# inp += '0'
	global immExt
	if (immSrc == "00"): #l instruction
		immExt = inp[0:12]
	elif (immSrc == "01"): #s instruction
		immExt = inp[0:7] + inp[20::]
	elif (immSrc == "10"): #b instruction
		# immExt = inp[0] + inp[1:8] + inp[19:23] + inp[23] + '0'
		immExt = inp[0] + inp[24] + inp[1:7] + inp[20:24] + '0' #changes inp[20:24] during error handling
	elif (immSrc == "11"): #j instruction
		inp = inp[0:20]
		immExt = inp[0] + inp[12:19] + inp[12] + inp[1:10] + '0'

def ALU(SrcA, SrcB, ALUCont, ALUSrc):
	global immExt, ALUResult, zero
	ALUResult = ""
	
	if (ALUSrc == '0'): #choosing between RD2 and immExt
		SrcB = int_to_binary(RD2, 32)
	else:
		SrcB = int_to_binary(abs(signed(immExt)), 32) #
	# print("sources : ", SrcA, SrcB)
	if (ALUCont == "000"): #add
		ALUResult = str(SrcA + signed(SrcB))
	elif (ALUCont == "001"): #subtract
		ALUResult = str(SrcA + signed(SrcB))
	elif (ALUCont == "010"): #bitwise_and
		ALUResult = ""
		bin_A = int_to_binary(SrcA, 32)
		for i, j in zip(bin_A, SrcB):
			ALUResult += str(int(i, 2) & int(j, 2))
		ALUResult = str(int(ALUResult, 2))
	elif (ALUCont == "011"): #bitwise_or
		ALUResult = ""
		bin_A = int_to_binary(SrcA, 32)
		for i, j in zip(bin_A, SrcB):
			ALUResult += str(int(i, 2) | int(j, 2))
		ALUResult = str(int(ALUResult, 2))
	elif (ALUCont == "101"): #set less than
		if (SrcA < signed(SrcB)): ALUResult = '1'
		else: ALUResult = '0'
	elif (ALUCont == "111"): #shift right logical
		ALUResult = str(SrcA >> int(SrcB, 2))
	# immExt = "" #initialise both to empty # LINE SHIFTED

def data_memory(index, memory, rs1, rs2, op, memWrite, value=0):
	global ReadValue

	if (op == "0000011"): #load instruction
		ReadValue = memory[(rs1 + index) - 65536]
		# print("MemIndex : ", (rs1 + index) - 65536)
	
	if(memWrite == "1"): #store instruction
		memory[(rs1 + index) - 65536] = rs2
		# print("MemIndex : ", (rs1 + index) - 65536)
	
def stack_memory(index):
	global ReadValue, Stack_memory
	ReadValue = Stack_memory[index - 256]

# idata__ =["00000000100010010000101000010011",
# "00000000010010110000101100010011",
# "00000000100101000110111100110011",
# "00000001000010110000101100010011",
# "00000001100000001000000001100111",
# "00000000100101000000010001100011",
# "00000000010000000000001010010011",
# "00000000100001000000010000010011",
# "00000000101000000000000011101111",
# "00000001001101000101101000110011",
# "00000000100011110111010100110011",
# "00010000000000000000101010010011",
# "00010000000000000000101010010011",
# "00010000000000000000101010010011",
# "00010000000000000000101010010011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000001010110101000101010110011",
# "00000000000010101010111010000011",
# "00000000000000000000000001100011"]

# idata__ = ["00000000010100000000010010010011",
# "00000000000000000000100100010011",
# "00000000010100000010001100110011",
# "11111111100000010000000100010011",
# "00000001100000000000000001100111",
# "00000000100010010000100110010011",
# "00010000000000000000101000010011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000001010010100000101000110011",
# "00000000101010100010000000100011",
# "00000000000010100010101100000011",
# "00000000101010100010000000100011",
# "00000000000010100010110000000011",
# "00000000101010100010000000100011",
# "00000001001010100010000000100011",
# "00000000010000010000000100010011",
# "00000000000000010010001010000011",
# "00000000000000000000000001100011"]

idata__ = ["00000000000100000000000010010011",
"00000000001000000000010100010011",
"00000000000101010000000110110011",
"01000000000100011000001000110011",
"00000000010000000010001010110011",
"00000000101000101101001010110011",
"00000000000100101110001100110011",
"00000000011000110111001110110011",
"00000000000000000000000001100011"]

def execute(idata__):
	PC(idata__)
	print(dict_instructions)
	global RD1, RD2, RegWrite, MemWrite, pc, zero,register_after_inst, ReadValue
	reset() #resets values in registers before reading a new file

	while dict_instructions[pc] != "00000000000000000000000001100011": #Halting instruction
		print(dict_instructions[pc])
		zero = False
		print("Current PC : ", pc)
		print(registers)
		RD1, RD2, RegWrite, MemWrite = 0, 0, 0, 0 #reinitialises every variable
		k = Instruction_Memory(dict_instructions[pc])
		if (k["op"] == "1100011"): #b-type condition checking
			if (k["func3"] == "000"):
				if (registers[k["A1"]] == registers[k["A2"]]):
					zero = True
				else:
					zero = False
			elif (k["func3"] == "001"):
				if (registers[k["A1"]] != registers[k["A2"]]):
					zero = True
				else:
					zero = False
			elif (k["func3"] == "100"):
				if (registers[k["A1"]] < registers[k["A2"]]):
					zero = True
				else:
					zero = False
		print(k)
		cu = control_unit(k["op"], k["func3"], k["func7"])
		print(cu)
		rf = register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
		ex = extend(k["Extend"], cu["ImmSrc"])
		print("immExt", immExt, signed(immExt))

		# if cu["ALUSrc"] == "1":
		# 	aluin = int(immExt, 2) #might have error 
		# elif cu["ALUSrc"] == "0":
		# 	aluin = RD2
		alu = ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"]) #SrcB is set to 0 but the value is decided in the function
		print("alucont", cu["ALUControl"])
		print(alu)
		print("ALUResult :", ALUResult)
		print("ALUResult type:", type(ALUResult))

		if (k['A1'] == "00010"):
			dm = stack_memory(registers["00010"])
		else:
			dm = data_memory(int(immExt, 2)//4, Data_memory, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], RD2)
		print(Data_memory)
		print("Value read:", ReadValue)
		# Upgrading registers with values
		if (cu["RegWrite"] == "1"):
			if (cu["ResultSrc"] == "01"): #reading from immediate
				if k["A3"] == "00010":
					registers[k["A3"]] = registers[k["A3"]] + signed(immExt) #x2 is stack pointer register
					#registers[k["A3"]] - ReadValue + 380
				elif k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt)
			
			if (cu["ResultSrc"] == "12"): #reading from immediate
				if k["A3"] == "00010":
					registers[k["A3"]] = registers[k["A3"]] + signed(immExt) #x2 is stack pointer register
					#registers[k["A3"]] - ReadValue + 380
				elif k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

			elif cu["ResultSrc"] == "00": #reading from AluResult
				if k["A3"] == "00010":
					registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380 #x2 is stack pointer register
				elif k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = int(ALUResult)
			
			elif cu["ResultSrc"] == "10": #jal and jalr
				registers[k["A3"]] = pc + 4

		print()
		PCNext(cu["PCSrc"], k["op"])
		register_value=list(registers.values())
		for i in range(len(register_value)):
			register_value[i]=int_to_binary(register_value[i],32)
		binary_pc=int_to_binary(pc,32)
		register_after_inst.append([binary_pc,register_value])
		print(binary_pc)
		pc_values.append(pc)
	
	#---------------------------------------------------------------------------
	print(dict_instructions[pc])
	zero = False
	print("Current PC : ", pc)
	print(registers)
	RD1, RD2, RegWrite, MemWrite = 0, 0, 0, 0 #reinitialises every variable
	k = Instruction_Memory(dict_instructions[pc])
	if (k["op"] == "1100011"): #b-type condition checking
		if (k["func3"] == "000"):
			if (registers[k["A1"]] == registers[k["A2"]]):
				zero = True
			else:
				zero = False
		elif (k["func3"] == "001"):
			if (registers[k["A1"]] != registers[k["A2"]]):
				zero = True
			else:
				zero = False
		elif (k["func3"] == "100"):
			if (registers[k["A1"]] < registers[k["A2"]]):
				zero = True
			else:
				zero = False
	print(k)
	cu = control_unit(k["op"], k["func3"], k["func7"])
	print(cu)
	rf = register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
	ex = extend(k["Extend"], cu["ImmSrc"])
	print("immExt", immExt, signed(immExt))

	# if cu["ALUSrc"] == "1":
	# 	aluin = int(immExt, 2) #might have error 
	# elif cu["ALUSrc"] == "0":
	# 	aluin = RD2
	alu = ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"]) #SrcB is set to 0 but the value is decided in the function
	print("alucont", cu["ALUControl"])
	print(alu)
	print("ALUResult :", ALUResult)
	print("ALUResult type:", type(ALUResult))

	if (k['A1'] == "00010"):
		dm = stack_memory(registers["00010"])
		print("stack_mem location :", registers["00010"] )
	else:
		dm = data_memory(int(immExt, 2)//4, Data_memory, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], RD2)

	if (cu["RegWrite"] == "1"):
		if (cu["ResultSrc"] == "01"):
			if k["A3"] == "00010":
				registers[k["A3"]] = registers[k["A3"]] + signed(immExt)#x2 is stack pointer register
			elif k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = signed(immExt)
		
		if (cu["ResultSrc"] == "12"):
			if k["A3"] == "00010":
				registers[k["A3"]] = registers[k["A3"]] + signed(immExt)#x2 is stack pointer register
			elif k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

		elif cu["ResultSrc"] == "00":
			if k["A3"] == "00010":
				registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380#x2 is stack pointer register
			elif k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = int(ALUResult)
		
		elif cu["ResultSrc"] == "10":
			registers[k["A3"]] = pc + 4
		
		elif cu["ResultSrc"] == "11":
			registers[k["A3"]] = pc + 4

	print()
	PCNext(cu["PCSrc"], k["op"])
	#---------------------------------------------------------------------------

	register_value=list(registers.values())
	for i in range(len(register_value)):
		register_value[i]=int_to_binary(register_value[i],32)
	binary_pc=int_to_binary(pc,32)
	register_after_inst.append([binary_pc,register_value])
	pc=0

pc_values.append(pc)
execute(idata__)
