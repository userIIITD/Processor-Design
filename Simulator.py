import os

RD1 = 0
RD2 = 0
immExt = ""
ALUResult = ""
ReadValue=0
RegWrite = 0
RegReturn = 0
MemWrite = 0
pc = 0
pc_update_flag = False

zero = False #flag for b-type instruction
dict_instructions = {}
register_after_inst=[]

registers = {"00000" : 0, "00001" : 0, "00010" : 0, "00011" : 0, "00100" : 0, "00101" : 0, "00110" : 0, "00111" : 0, "01000" : 0, "01001" : 0, "01010" : 0, "01011" : 0, "01100" : 0, "01101" : 0, "01110" : 0, "01111" : 0, "10000" : 0, "10001" : 0, "10010" : 0, "10011" : 0, "10100" : 0, "10101" : 0, "10110" : 0, "10111": 0, "11000" : 0, "11001" : 0, "11010" : 0, "11011" : 0, "11100" : 0, "11101" : 0, "11110" : 0, "11111": 0}
pc_values = []


def reset():
	global registers, Data_memory, pc
	for i in registers:
		registers[i] = 0
	registers["00010"] = 380
	for i in Data_memory: Data_memory[i] = 0
	pc = 0

def int_to_binary(num, bit):
    return format(num & (2**bit - 1), f"0{bit}b")

def control_unit(opcode, funct3, funct7):
	global zero
	signals = {"PCSrc": "0", "ResultSrc": "XX", "MemWrite": "0", "ALUControl": "000", "ALUSrc": "0", "ImmSrc": "00", "RegWrite": "0"}

	if len(opcode) != 7 or len(funct3) != 3 or len(funct7) != 1:
		print("Invalid opcode/funct length")
	
	try:
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
			signals["ALUControl"] = "000"

		elif opcode == "0000011":  #LW
			signals["ResultSrc"] = "13"
			signals["ALUSrc"] = "1"
			signals["RegWrite"] = "1"

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
	
	except Exception as e:
		print(f"Control unit error: {e}")

	return signals

def Instruction_Memory(inst):
	inst = str(inst)
	try:
		return {"op":inst[25:32],"func3":inst[17:20],"func7":inst[1],"A1":inst[12:17],"A2":inst[7:12],"A3":inst[20:25],"Extend":inst[0:25]}
	except IndexError:
		print("Invalid instruction")


def PCNext(PCSrc,x6,op="X"):
	global immExt, pc_update_flag
	global pc
	try:
		if PCSrc=="1":
			if (op == "1101111"):
				pc=pc+signed(immExt)
				pc = pc & ~1
			elif (op == "1100111"): #jalr
				pc = x6 + signed(immExt)
				pc = pc & ~1
			else:
				pc = pc + signed(immExt)
			
			if pc % 4 != 0:
				pc -= pc % 4
			return True
		elif PCSrc=="0":
			pc=pc+4
			return True
	
	except Exception as e:
		print(f"PC update error: {e}")
		return False


def PC(instruction):
	global dict_instructions
	PC = 0 #initialising PC with zero
	for i in instruction:
		dict_instructions[PC] = i
		PC += 4
	
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
			if i not in ["1", "0"]:
				print(f"Invalid binary string: {inp}")
			if i == '1':
				new += '0'
			else: new += '1'
		return -(int(new, 2) + 1) #add 1
	else:
		return int(inp, 2)
		
def register_file(A1, A2, A3, WD3, WE3, clk=True):
	global RD1, RD2, registers
	try:
		RD1 = registers[A1]
		RD2 = registers[A2]
		
		if (WE3 == 1): registers[A3] = int(WD3, 2)
	except Exception as e:
		print(f"Register file error: {e}")

def extend(inp, immSrc):
	#31:7
	global immExt
	if not isinstance(inp, str) or len(inp) < 1:
		print("Invalid input for immediate extension")
	
	if not isinstance(immSrc, str) or len(immSrc) != 2:
		print("ImmSrc must be 2-bit string")
	
	try:
		if (immSrc == "00"): #l instruction
			immExt = inp[0:12]
		elif (immSrc == "01"): #s instruction
			immExt = inp[0:7] + inp[20::]
		elif (immSrc == "10"): #b instruction
			immExt = inp[0] + inp[24] + inp[1:7] + inp[20:24] + '0' #changes inp[20:24] during error handling
		elif (immSrc == "11"): #j instruction
			inp = inp[0:20]
			immExt = inp[0] + inp[12:20] + inp[11] + inp[1:11] + '0'
	except Exception as e:
		print(f"Immediate extension error: {e}")

def ALU(SrcA, SrcB, ALUCont, ALUSrc):
	global immExt, ALUResult, zero
	ALUResult = ""

	if not isinstance(ALUCont, str) or len(ALUCont) != 3:
		print("ALUControl must be 3-bit string")
	
	if not isinstance(ALUSrc, str) or ALUSrc not in ['0', '1']:
		print("ALUSrc must be '0' or '1'")
	try:
		if (ALUSrc == '0'): #choosing between RD2 and immExt
			SrcB = int_to_binary(RD2, 32)
		else:
			SrcB = int_to_binary(abs(signed(immExt)), 32) #
		# print("sources : ", SrcA, SrcB)
		if (ALUCont == "000"): #add
			ALUResult = str(SrcA + signed(SrcB))
		elif (ALUCont == "001"): #subtract
			ALUResult = str(SrcA - signed(SrcB))
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
	except Exception as e:
		print(f"ALU operation error: {e}")

def data_memory(index, rs1, rs2, op, memWrite, file):
	global ReadValue, Data_memory
	if (op == "0000011"): #load instruction
		if (index + rs1) in range(256, 384) or (index + rs1) in range(65536, 65664):
			ReadValue = Data_memory[rs1 + index]
		else:
			print("Invalid memory location in", file)
		
	if(memWrite == "1"): #store instruction
		if (index + rs1) in range(256, 384) or (index + rs1) in range(65536, 65664):
			Data_memory[rs1 + index] = rs2
		else:
			print("Invalid memory location in", file)

def execute(idata__, file):
	if "00000000000000000000000001100011" not in idata__:
		print("Error: Halt missing in", file, "execution stopped by the simulator.")
		return
	
	PC(idata__)
	global RD1, RD2, RegWrite, MemWrite, pc, zero,register_after_inst, ReadValue, Data_memory, immExt, pc_update_flag
	pc_update_flag = False
	reset() #resets values in registers before reading a new file

	while dict_instructions[pc] != "00000000000000000000000001100011": #Halting instruction
		
		zero = False
		RD1, RD2, RegWrite, MemWrite, immExt = 0, 0, 0, 0, "" #reinitialises every variable
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
		cu = control_unit(k["op"], k["func3"], k["func7"])
		register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
		extend(k["Extend"], cu["ImmSrc"])

		ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"]) #SrcB is set to 0 but the value is decided in the function

		if (k["op"] == "0000011" or k["op"] == "0100011"):
			data_memory(int(immExt, 2)//4, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], file)

		if (cu["RegWrite"] == "1"):
			if (cu["ResultSrc"] == "01"): #reading from immediate
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt)
			
			elif (cu["ResultSrc"] == "12"): #reading from immediate
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

			elif cu["ResultSrc"] == "00": #reading from AluResult
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = int(ALUResult)
			
			elif cu["ResultSrc"] == "13": #load
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = ReadValue

			elif cu["ResultSrc"] == "10": #jal and jalr
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = pc + 4
			
			elif cu["ResultSrc"] == "11": #jalr
				if k["A3"] == "00000":
					registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = pc + 4

		if PCNext(cu["PCSrc"], registers[k["A1"]], k["op"]) == False:
			break
		
		register_value=list(registers.values())
		for i in range(len(register_value)):
			register_value[i]=int_to_binary(register_value[i],32)
		binary_pc=int_to_binary(pc,32)
		register_after_inst.append([binary_pc,register_value])
		pc_values.append(pc)
	
	#---------------------------------------------------------------------------
	zero = False
	RD1, RD2, RegWrite, MemWrite, immExt = 0, 0, 0, 0, "" #reinitialises every variable
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
	cu = control_unit(k["op"], k["func3"], k["func7"])
	register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
	extend(k["Extend"], cu["ImmSrc"])

	ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"]) #SrcB is set to 0 but the value is decided in the function
	
	if (k["op"] == "0000011" or k["op"] == "0100011"):
		data_memory(int(immExt, 2)//4, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], file) == "stop"

	if (cu["RegWrite"] == "1"):
		if (cu["ResultSrc"] == "01"):
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = signed(immExt)
		
		if (cu["ResultSrc"] == "12"):
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

		elif cu["ResultSrc"] == "00":
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = int(ALUResult)
		
		elif cu["ResultSrc"] == "13": #load
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = ReadValue
		
		elif cu["ResultSrc"] == "10":
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = pc + 4
		
		elif cu["ResultSrc"] == "11":
			if k["A3"] == "00000":
					registers[k["A3"]] = 0
			else:
				registers[k["A3"]] = pc + 4

	PCNext(cu["PCSrc"], registers[k["A1"]], k["op"])
	#---------------------------------------------------------------------------

	register_value=list(registers.values())
	for i in range(len(register_value)):
		register_value[i]=int_to_binary(register_value[i],32)
	binary_pc=int_to_binary(pc,32)
	register_after_inst.append([binary_pc,register_value])
	pc_values.append(pc)

#---------------------------------------------SEPARATING FILE HANDLING FROM MAIN PROGRAM---------------------------------------------
hexa={0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"A",11:"B",12:"C",13:"D",14:"E",15:"F",}
#Taking input from files and giving output
def in_and_out(file,loc):
	global register_after_inst,hexa
	f=open(os.path.join("automatedTesting","tests","bin",loc,file),'r')
	input_data=f.readlines()
	for i in range(len(input_data)):
		input_data[i]=input_data[i].strip()
	new_mem = []
	execute(input_data, file)

	new_mem = (list(Data_memory.values()))[128:256]
	f.close()
	f=open(os.path.join("automatedTesting","tests","user_traces",loc,file),'w')
	for i,j in register_after_inst:
		f.write(f"0b{i} ")
		for k in j:
			f.write(f"0b{k} ")
		f.write("\n")
	register_after_inst=[]
	for j in range(0,32):
		i=4*j
		unit=i%16
		remaing=i//16
		f.write(f"0x000100{str(remaing)}{hexa[unit]}:0b{int_to_binary(new_mem[j],32)}\n")
	f.close()
	
run=True
file_no=1
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("..")
#Reading files in simple 
simple_folder = os.path.join("automatedTesting","tests","bin","simple")
for file in os.listdir(simple_folder):
	in_and_out(file,"simple")
	parent_folder=os.getcwd().split('\\')[-1].split('/')[-1]
	os.chdir("..")
	os.chdir(parent_folder)

#Reading file in hard
simple_folder = os.path.join("automatedTesting","tests","bin","hard")
for file in os.listdir(simple_folder):
	in_and_out(file,"hard")
	parent_folder=os.getcwd().split('\\')[-1].split('/')[-1]
	os.chdir("..")
	os.chdir(parent_folder)
