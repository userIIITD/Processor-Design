Register= {"zero": "00000", "ra":"00001", "sp": "00010", "gp": "00011", "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "fp": "01000", "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111"}

def sext(num, bit = 12):
    return format(num & (2**bit - 1), f"0{bit}b")

def R(i, f):
    global error
    opcode = "0110011"
    funcs = {"add":["000","0000000"],"sub":["000","0100000"],"slt":["010","0000000"],"sltu":["011","0000000"],"srl":["101","0000000"],"or":["110","0000000"],"and":["111","0000000"]} #func3, func7
    name = i.split()[0]
    try:
        rd=Register[i.split()[1].split(",")[0]]
        rs1=Register[i.split()[1].split(",")[1]]
        rs2=Register[i.split()[1].split(",")[2]]
        f.write(f"{funcs[name][1]}{rs2}{rs1}{funcs[name][0]}{rd}{opcode}\n")
    except:
        print("Register name cannot be resolved")
        error = True

def I(i, s):
    global error
    f3={"lw":["010","0000011"],"addi":["000","0010011"],"jalr":["000","1100111"]} #[f3,opcode]
    name=i.split()[0]
    if name == "lw": 
            imm=int(i.split()[1].split(",")[1].split("(")[0])
    else: 
            imm =int(i.split()[1].split(",")[2])
    if imm not in range(-2048, 2048):
        print("Immediate out of bound")
    else:
        try:
            if name == "lw": 
                imm=sext(int(i.split()[1].split(",")[1].split("(")[0]),12)
                rd=Register[i.split()[1].split(",")[0]]
                rs1=Register[i.split()[1].split(",")[1].split("(")[1].rstrip(")")]
            else: 
                imm = sext(int(i.split()[1].split(",")[2]))
                rd=Register[i.split()[1].split(",")[0]]  
                rs1=Register[i.split()[1].split(",")[1]]
            f.write(f"{imm}{rs1}{f3[name][0]}{rd}{f3[name][1]}")
        except:
            print("Register name cannot be resolved")
            error = True
    

def S(i, f):
    global error
    opcode = "0100011"
    func3 = "010"
    imm = int(i.split()[1].split(",")[1][0:i.split()[1].split(",")[1].find('(')])
    if imm not in range(-2048, 2048):
        print("Immediate out of bound")
        error = True
    else:
        try: 
            imm = sext(int(i.split()[1].split(",")[1][0:i.split()[1].split(",")[1].find('(')]), 12)
            rs1 = Register[i[i.find('(') + 1:i.find(')')]]
            rs2 = Register[i.split()[1].split(",")[0]]
            f.write(f"{imm[:7]}{rs2}{rs1}{func3}{imm[7:]}{opcode}\n")
        except:
            print("Register name cannot be resolved")
            error = True

def B(i, f):
    global error
    opcode = "1100011"
    func3 = {"beq" : "000", "bne" : "001", "blt" : "100"}
    name = i.split()[0]
    imm = int(i.split()[1].split(",")[2])
    if imm not in range(-2048, 2048):
        print("Immediate out of bound")
        error = True
    else:
        try:
            imm = sext(int(i.split()[1].split(",")[2]), 12)
            rs1 = Register[i.split()[1].split(",")[0]]
            rs2 = Register[i.split()[1].split(",")[1]]
            f.write(f"{imm[:7]}{rs2}{rs1}{func3[name]}{imm[7:]}{opcode}\n")
        except:
            print("Register name cannot be resolved")
            error = True

def J(i, f):
    opcode="1100011"
    name=i.split()[0]
    imm=sext(int(i.split()[1].split(',')[1]), 21)
    rd=Register[i.split()[1].split(',')[0]]
    f.write(imm[31:12:-1]+rd+opcode+'\n')

type_of_inst = {"add" : "R", "sub" : "R", "slt" : "R", "srl" : "R", "or" : "R", "and" : "R", "addi" : "I", "lw" : "I", "jalr" : "I", "sw" : "S", "beq" : "B", "blt" : "B", "bne" : "B", "jal" : "J"}

def main():
    import os
    fin = open("Ex_test_2.txt", "r") #input text file
    temp = fin.readlines()
    fin.close()
    
    instruction_list = []
    for i in temp:
        type = i.split(" ")[0]
        if type in type_of_inst:
            instruction_list.append([i, type_of_inst[type]])
        else:
            print(f"Error. No {type} instruction.")

    fout = open("out.txt", "a") #output text file

    error = False

    for i in instruction_list:
        if error == False:
            if i[1] == 'R':
                R(i[0], fout)
            elif i[1] == 'I':
                I(i[0], fout)
            elif i[1] == 'S':
                S(i[0], fout)
            elif i[1] == 'B':
                B(i[0], fout)
            elif i[1] == 'J':
                J(i[0], fout)
        else:
            error = False
            break

    fout.close()
