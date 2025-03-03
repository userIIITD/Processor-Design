#Use these variables to load/read values in register
x0 = 0
x1 = 0
x2 = 0
x3 = 0
x4 = 0
x5 = 0
x6 = 0
x7 = 0
x8 = 0
x9 = 0
x10 = 0
x11 = 0
x12 = 0
x13 = 0
x14 = 0
x15 = 0
x16 = 0
x17 = 0
x18 = 0
x19 = 0
x20 = 0
x21 = 0
x22 = 0
x23 = 0
x24 = 0
x25 = 0
x26 = 0
x27 = 0
x28 = 0
x29 = 0
x30 = 0
x31 = 0

registers = {"00000" : x0, "00001" : x1, "00010" : x2, "00011" : x3, "00100" : x4, "00101" : x5, "00110" : x6, "00111" : x7, "01000" : x8, "01001" : x9, "01010" : x10, "01011" : x11, "01100" : x12, "01101" : x13, "01110" : x14, "01111" : x15, "10000" : x16, "10001" : x17, "10010" : x18, "10011" : x19, "10100" : x20, "10101" : x21, "10110" : x22, "10111", x23, "11000" : x24, "11001" : x25, "11010" : x26, "11011" : x27, "11100" : x28, "11101" : x29. "11110" : x30, "11111", x31}

def register_file(A1, A2, A3, WD3, RD1, RD2, WE3, clk=True):
	RD1 = registers[A1]
	RD2 = registers[A2]
	
	if (WD3 == 1):
		registers[A2] = A3
	
	if (WE3 == 1): pass
	return (RD1, RD2)

def extend(inp, immSrc, immExt=True):
	#31:7
	if (immSrc == "00"): #lw instruction
		#0:12
	elif (immSrc == "01"): #sw instruction
		#0:0+7 + #21:21+5
	elif (immSrc == "10"): #beq instruction
		#
	else: pass
