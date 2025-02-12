#waiting for Bhumik's code

file = open('')

Register={"zero": "00000", "ra":"00001", "sp": "00010", "gp": "00011", "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "fp": "01000", "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111"}

def sext(self, value, range):
    pass

def R(instruction, f):
    opcode = "0110011"
    funcs = {"add":["000","0000000"],"sub":["000","0100000"],"slt":["010","0000000"],"sltu":["011","0000000"],"xor":["100","0000000"],"srl":["101","0000000"],"or":["110","0000000"],"and":["111","0000000"],"sra":["101","0100000"]} #func3, func7
    for i in instruction:
        name = i.split()[0]
        rd=Register[i.split()[1].split(",")[0]]
        rs1=Register[i.split()[1].split(",")[1]]
        rs2=Register[i.split()[1].split(",")[2]]
        f.write(f"{funcs[name][1]}{rs2}{rs1}{funcs[name][0]}{rd}{opcode}")

def I(instruction, f):
    f3={"lw":["010","0010011"],"addi":["000","0010011"],"jalr":["000","1100111"]} #[f3,opcode]
    for i in self.I:
        name=i.split()[0]
        if name=="lw":
            imm=sext(int(i.split()[1].split(",")[1].split("(")[0]),12)
            rd=Regiseter[i.split()[1].split(",")[0]]
            rs1=Regiseter[i.split()[1].split(",")[1].split("(")[1].rstrip(")")]
            f.write(f"{imm}{rs1}{f3[name][0]}{rd}{f3[name][1]}")
        elif name=="addi":
            rd=Regiseter[i.split()[1].split(",")[0]]
            rs1=Regiseter[i.split()[1].split(",")[1]]
            imm=sext(int(i.split()[1].split(",")[2]))
            f.write(f"{imm}{rs1}{f3[name][0]}{rd}{f3[name][1]}")
        elif name=="jalr":
            rd=Regiseter[i.split()[1].split(",")[0]]
            rs1=Regiseter[i.split()[1].split(",")[1]]
            offset=sext(int(i.split()[1].split(",")[2]))
            f.write(f"{offset}{rs1}{f3[name][0]}{rd}{f3[name][1]}")

def S(instruction, f):
    opcode = "0100011"
    func3 = "010"
    for i in instruction:
        imm = sext(int(i.split()[1].split(",")[1][0:i.split()[1].split(",")[1].find('(')]), 12) 
        rs1 = Register[i[i.find('(') + 1:i.find(')')]]
        rs2 = Register[i.split()[1].split(",")[0]]
        f.write(f"{imm[:7]}{rs2}{rs1}{func3}{imm[7:]}{opcode}")

def B(instruction, f):
    opcode = "1100011"
    func3 = {"beq" : "000", "bne" : "001", "blt" : "100"}
    for i in instruction:
        name = i.split()[0]
        imm = sext(int(i.split()[1].split(",")[2]), 12)
        rs1 = Register[i.split()[1].split(",")[0]]
        rs2 = Register[i.split()[1].split(",")[1]]

        f.write(f"{imm[:7]}{rs2}{rs1}{func3[name]}{imm[7:]}{opcode}")

def J(instruction, f):
    pass

def U(instruction, f):
    pass
