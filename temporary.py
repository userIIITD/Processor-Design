type_of_inst = {"add" : "R", "sub" : "R", "slt" : "R", "srl" : "R", "or" : "R", "and" : "R", "addi" : "I", "lw" : "R", "jalr" : "I", "sw" : "S", "beq" : "B", "blt" : "B", "bne" : "B", "jal" : "J"}

def read_file():
    file = open("file_name.txt", "r")
    temp = file.readlines()
    file.close()
    
    instruction_list = []
    for i in temp:
        type = i.split(" ")[0]
        if type in type_of_inst:
            instruction_list.append([i.strip(), type_of_inst[type]])

    return instruction_list


print(read_file())