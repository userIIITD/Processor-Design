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
Data_memory = {256: 0, 257: 0, 258: 0, 259: 0, 260: 0, 261: 0, 262: 0, 263: 0, 264: 0, 265: 0, 266: 0, 267: 0, 268: 0, 269: 0, 270: 0, 271: 0, 272: 0, 273: 0, 274: 0, 275: 0, 276: 0, 277: 0, 278: 0, 279: 0, 280: 0, 281: 0, 282: 0, 283: 0, 284: 0, 285: 0, 286: 0, 287: 0, 288: 0, 289: 0, 290: 0, 291: 0, 292: 0, 293: 0, 294: 0, 295: 0, 296: 0, 297: 0, 298: 0, 299: 0, 300: 0, 301: 0, 302: 0, 303: 0, 304: 0, 305: 0, 306: 0, 307: 0, 308: 0, 309: 0, 310: 0, 311: 0, 312: 0, 313: 0, 314: 0, 315: 0, 316: 0, 317: 0, 318: 0, 319: 0, 320: 0, 321: 0, 322: 0, 323: 0, 324: 0, 325: 0, 326: 0, 327: 0, 328: 0, 329: 0, 330: 0, 331: 0, 332: 0, 333: 0, 334: 0, 335: 0, 336: 0, 337: 0, 338: 0, 339: 0, 340: 0, 341: 0, 342: 0, 343: 0, 344: 0, 345: 0, 346: 0, 347: 0, 348: 0, 349: 0, 350: 0, 351: 0, 352: 0, 353: 0, 354: 0, 355: 0, 356: 0, 357: 0, 358: 0, 359: 0, 360: 0, 361: 0, 362: 0, 363: 0, 364: 0, 365: 0, 366: 0, 367: 0, 368: 0, 369: 0, 370: 0, 371: 0, 372: 0, 373: 0, 374: 0, 375: 0, 376: 0, 377: 0, 378: 0, 379: 0, 380: 0, 381: 0, 382: 0, 383: 0, 65536: 0, 65537: 0, 65538: 0, 65539: 0, 65540: 0, 65541: 0, 65542: 0, 65543: 0, 65544: 0, 65545: 0, 65546: 0, 65547: 0, 65548: 0, 65549: 0, 65550: 0, 65551: 0, 65552: 0, 65553: 0, 65554: 0, 65555: 0, 65556: 0, 65557: 0, 65558: 0, 65559: 0, 65560: 0, 65561: 0, 65562: 0, 65563: 0, 65564: 0, 65565: 0, 65566: 0, 65567: 0, 65568: 0, 65569: 0, 65570: 0, 65571: 0, 65572: 0, 65573: 0, 65574: 0, 65575: 0, 65576: 0, 65577: 0, 65578: 0, 65579: 0, 65580: 0, 65581: 0, 65582: 0, 65583: 0, 65584: 0, 65585: 0, 65586: 0, 65587: 0, 65588: 0, 65589: 0, 65590: 0, 65591: 0, 65592: 0, 65593: 0, 65594: 0, 65595: 0, 65596: 0, 65597: 0, 65598: 0, 65599: 0, 65600: 0, 65601: 0, 65602: 0, 65603: 0, 65604: 0, 65605: 0, 65606: 0, 65607: 0, 65608: 0, 65609: 0, 65610: 0, 65611: 0, 65612: 0, 65613: 0, 65614: 0, 65615: 0, 65616: 0, 65617: 0, 65618: 0, 65619: 0, 65620: 0, 65621: 0, 65622: 0, 65623: 0, 65624: 0, 65625: 0, 65626: 0, 65627: 0, 65628: 0, 65629: 0, 65630: 0, 65631: 0, 65632: 0, 65633: 0, 65634: 0, 65635: 0, 65636: 0, 65637: 0, 65638: 0, 65639: 0, 65640: 0, 65641: 0, 65642: 0, 65643: 0, 65644: 0, 65645: 0, 65646: 0, 65647: 0, 65648: 0, 65649: 0, 65650: 0, 65651: 0, 65652: 0, 65653: 0, 65654: 0, 65655: 0, 65656: 0, 65657: 0, 65658: 0, 65659: 0, 65660: 0, 65661: 0, 65662: 0, 65663: 0}

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
	
	if not all(isinstance(x, str) for x in [opcode, funct3, funct7]):
		raise ValueError("Control unit inputs must be strings")
	if len(opcode) != 7 or len(funct3) != 3 or len(funct7) != 1:
		raise ValueError("Invalid opcode/funct length")
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

			# if funct3 == "000":
			signals["ALUControl"] = "000"
			# elif funct3 == "110":
			# 	signals["ALUControl"] = "011"
			# elif funct3 == "111":
			# 	signals["ALUControl"] = "010"

		elif opcode == "0000011":  #LW
			signals["ResultSrc"] = "13"
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
	except Exception as e:
		raise ValueError(f"Control unit error: {e}")
	return signals

def Instruction_Memory(inst):
	if not isinstance(inst, str) or len(inst) != 32:
		raise ValueError("Instruction must be a 32-bit binary string")
	try:
		return {"op": inst[25:32],"func3": inst[17:20],"func7": inst[1],"A1": inst[12:17],"A2": inst[7:12],"A3": inst[20:25],"Extend": inst[0:25]}
	except IndexError:
		raise ValueError("Invalid instruction format")

def PCNext(PCSrc,x6,op="X"):
	global pc,immExt
	if not isinstance(PCSrc, str) or PCSrc not in ["0", "1"]:
		raise ValueError("PCSrc must be '0' or '1'")
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
		elif PCSrc=="0":
			pc=pc+4
	except Exception as e:
		raise ValueError(f"PC update error: {e}")

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
		raise ValueError(f"Register file error: {e}")
def extend(inp, immSrc):
	#31:7
	global immExt
	if not isinstance(inp, str) or len(inp) < 1:
		raise ValueError("Invalid input for immediate extension")
	
	if not isinstance(immSrc, str) or len(immSrc) != 2:
		raise ValueError("ImmSrc must be 2-bit string")
	try:
		if (immSrc == "00"): #l instruction
			immExt = inp[0:12]
		elif (immSrc == "01"): #s instruction
			immExt = inp[0:7] + inp[20::]
		elif (immSrc == "10"): #b instruction
			# immExt = inp[0] + inp[1:8] + inp[19:23] + inp[23] + '0'
			immExt = inp[0] + inp[24] + inp[1:7] + inp[20:24] + '0' #changes inp[20:24] during error handling
		elif (immSrc == "11"): #j instruction
			inp = inp[0:20]
			# immExt = inp[0] + inp[12:19] + inp[12] + inp[1:10] + '0'
			immExt = inp[0] + inp[12:20] + inp[11] + inp[1:11] + '0'
	except Exception as e:
		raise ValueError(f"Immediate extension error: {e}")

def ALU(SrcA, SrcB, ALUCont, ALUSrc):
	global immExt, ALUResult, zero
	ALUResult = ""
	
	if not isinstance(ALUCont, str) or len(ALUCont) != 3:
		raise ValueError("ALUControl must be 3-bit string")
	
	if not isinstance(ALUSrc, str) or ALUSrc not in ['0', '1']:
		raise ValueError("ALUSrc must be '0' or '1'")
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
	except Exception as e:
		raise ValueError(f"ALU operation error: {e}")
	# immExt = "" #initialise both to empty # LINE SHIFTED

def data_memory(index, memory, rs1, rs2, op, memWrite, value=0):
	global ReadValue, Data_memory

	if (op == "0000011"): #load instruction
		ReadValue = Data_memory[rs1 + index]
	
	if(memWrite == "1"): #store instruction
		Data_memory[rs1 + index] = rs2

def execute(idata__):
	PC(idata__)
	global RD1, RD2, RegWrite, MemWrite, pc, zero,register_after_inst, ReadValue, Data_memory, immExt
	reset() #resets values in registers before reading a new file
	while 1:
		try:
			if pc not in dict_instructions:
				print(f"PC {pc} Not Found in instruction memory")
				break
			current_instruction=dict_instructions[pc]
			if current_instruction=="00000000000000000000000001100011":
				break
			# time.sleep(1)
		
			zero=False
			RD1,RD2,RegWrite,MemWrite,immExt=0,0,0,0,0
			try:
				k=Instruction_Memory(current_instruction)
			except Exception as e:
				print(f"Error decoding instruction at PC {pc}:{e}")
				pc+=4
				continue
			if(k["op"]=="1100011"):
				if k["A1"] not in registers or k["A2"] not in registers:
					print(f"Invalid register access at PC {pc}")
					pc+=4
					continue
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
				else:
					print(f"Unsupported dunc3 {k['func3']} for branch at PC {pc}")
					pc+=4
					continue
	
			try:
				cu = control_unit(k["op"], k["func3"], k["func7"])
			except Exception as e:
				print(f"Control unit error at PC {pc}: {e}")
				pc+=4
				continue
		
			try:
				register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
			except Exception as e:
				print(f"Register file error at PC {pc}: {e}")
				pc+=4
				continue
			try:
				extend(k["Extend"], cu["ImmSrc"])
			except Exception as e:
				print(f"Immediate extension error at PC {pc}: {e}")
				pc+=4
				continue
	
			try:
				alu=ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"])
			except Exception as e:
				print(f"ALU error at PC {pc}: {e}")
				pc+=4
				continue
			
			if k["op"]=="0000011" or k["op"]=="010011":
				try:
					dm = data_memory(int(immExt, 2)//4, Data_memory, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], RD2)
				except Exception as e:
					print(f"Memory access error at PC {pc}: {e}")
					pc+=4
					continue
			
			if cu["RegWrite"]=="1":
				try:
					if (cu["ResultSrc"] == "01"): #reading from immediate
						# if k["A3"] == "00010":
							# registers[k["A3"]] = registers[k["A3"]] + signed(immExt) #x2 is stack pointer register
							#registers[k["A3"]] - ReadValue + 380
						if k["A3"] == "00000":
							registers[k["A3"]] = 0
						else:
							registers[k["A3"]] = signed(immExt)
			
					elif (cu["ResultSrc"] == "12"): #reading from immediate
						# if k["A3"] == "00010":
							# registers[k["A3"]] = registers[k["A3"]] + signed(immExt) #x2 is stack pointer register
							#registers[k["A3"]] - ReadValue + 380
						if k["A3"] == "00000":
							registers[k["A3"]] = 0
						else:
							registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

					elif cu["ResultSrc"] == "00": #reading from AluResult
						# if k["A3"] == "00010":
							# registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380 #x2 is stack pointer register
						if k["A3"] == "00000":
							registers[k["A3"]] = 0
						else:
							registers[k["A3"]] = int(ALUResult)
					
					elif cu["ResultSrc"] == "13": #load
						# if k["A3"] == "00010":
							# registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380 #x2 is stack pointer register
						if k["A3"] == "00000":
							registers[k["A3"]] = 0
						else:
							# print("Memory Read for load", int(ALUResult) + ReadValue)
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
				except Exception as e:
					print(f"Register writeback error at PC {pc}: {e}")
			
			try:
				PCNext(cu["PCSrc"], registers[k["A1"]], k["op"])
			except Exception as e:
				print(f"PC update error at PC {pc}: {e}")
				pc+=4
				continue
			try:
				register_value=list(registers.values())
				for i in range(len(register_value)):
					register_value[i]=int_to_binary(register_value[i],32)
				binary_pc=int_to_binary(pc,32)
				register_after_inst.append([binary_pc,register_value])
				
				pc_values.append(pc)
			except Exception as e:
				print(f"State capture error at PC {pc}: {e}")
		except Exception as e:
			print(f"Unexpected error at PC {pc}:{e}")
			pc+=4
			if (pc>=max(dict_instructions.keys(),default=0)+4):
				break
	try:
		
		zero = False
		
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
		
		cu = control_unit(k["op"], k["func3"], k["func7"])
		
		rf = register_file(k["A1"], k["A2"], k["A3"], ReadValue, RegWrite)
		ex = extend(k["Extend"], cu["ImmSrc"])
		

		# if cu["ALUSrc"] == "1":
		# 	aluin = int(immExt, 2) #might have error 
		# elif cu["ALUSrc"] == "0":
		# 	aluin = RD2
		alu = ALU(RD1, 0, cu["ALUControl"], cu["ALUSrc"]) #SrcB is set to 0 but the value is decided in the function
		

		if (k["op"] == "0000011" or k["op"] == "0100011"):
			dm = data_memory(int(immExt, 2)//4, Data_memory, registers[k["A1"]], registers[k["A2"]], k["op"], cu["MemWrite"], RD2)

		if (cu["RegWrite"] == "1"):
			if (cu["ResultSrc"] == "01"):
				# if k["A3"] == "00010":
					# registers[k["A3"]] = registers[k["A3"]] + signed(immExt)#x2 is stack pointer register
				if k["A3"] == "00000":
						registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt)
			
			if (cu["ResultSrc"] == "12"):
				# if k["A3"] == "00010":
					# registers[k["A3"]] = registers[k["A3"]] + signed(immExt)#x2 is stack pointer register
				if k["A3"] == "00000":
						registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = signed(immExt) + registers[k["A1"]]

			elif cu["ResultSrc"] == "00":
				# if k["A3"] == "00010":
					# registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380#x2 is stack pointer register
				if k["A3"] == "00000":
						registers[k["A3"]] = 0
				else:
					registers[k["A3"]] = int(ALUResult)
			
			elif cu["ResultSrc"] == "13": #load
				# if k["A3"] == "00010":
					# registers[k["A3"]] = - registers[k["A3"]] + int(ALUResult) + 380#x2 is stack pointer register
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
		register_value=list(registers.values())
		for i in range(len(register_value)):
			register_value[i]=int_to_binary(register_value[i],32)
		binary_pc=int_to_binary(pc,32)
		register_after_inst.append([binary_pc,register_value])
	except Exception as e:
		print(f"Error procesing in final instruction {e}")
	pc_values.append(pc)
	pc=0
	

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
	execute(input_data)

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
