class RV32i:
    def __init__(self,R,I,S,B,J,U,Regiseter,file):
        self.R=R
        self.I=I
        self.S=S
        self.B=B
        self.J=J
        self.U=U
        self.Regiseter=Regiseter
        self.file=file
    def main(self,file):
        with open(self.file,"w") as f:
            def R(self,R,Regiseter,file):
                Ri=["add s2,s3,s4"]#self.R 
                f3={"add":["000","0000000"],"sub":["000","0100000"],"slt":["010","0000000"],"sltu":["011","0000000"],"xor":["100","0000000"],"srl":["101","0000000"],"or":["110","0000000"],"and":["111","0000000"],"sra":["101","0100000"]}
                opcode="0110011"
                for i in Ri:
                    for j in f3:
                        if i.split()[0]==f3[3]:
                            rd=Regiseter[i.split()[0].split(",")[0]]
                            rs1=Regiseter[i.split()[0].split(",")[1]]
                            rs2=Regiseter[i.split()[0].split(",")[2]]
                            print(f"{f3[j][1]}{rs2}{rs1}{f3[j][0]}{rd}{opcode}")
                            f.write(f"{f3[j][1]}{rs2}{rs1}{f3[j][0]}{rd}{opcode}")
            def I(self,I,Regiseter,file):
                Ii=self.I

            def S(self,S,Regiseter,file):
                Si=self.S

            def B(self,B,Regiseter,file):
                Bi=self.B

            def J(self,J,Regiseter,file):
                Ji=self.J

            def U(self,U,Regiseter,file):
                Ui=self.U

Inst=RV32i(["add s2,s3,s4","sub s2,s2,s2"],["add s2,s3,s4"],["add s2,s3,s4"],["add s2,s3,s4"],["add s2,s3,s4"],["add s2,s3,s4"],{"zero": "00000", "ra":"00001", "sp": "00010", "gp": "00011", "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "fp": "01000", "s1": "01001", "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111"},"output.txt")
