#!/usr/bin/env python3

# Basically a stripped down version of the VM printin out human-readbale opcodes

class Disassembler:
    def __init__(self,filename=""):
        self.mem = [ 0 for i in range(2**15)]
        if filename !="":
            self.readInput(filename)
        self.i = 0
        self.l = 0
        
    def readInput(self,filename="synacor-challenge/challenge.bin"):
        i = 0
        with open(filename, "rb") as f:
            read = f.read(2)
            while read:
                self.mem[i] = int.from_bytes(read, "little")
                read = f.read(2)
                i+=1
        self.l = i-1 # program lenght
        
    def rov(self,b): # register or value, now as strings
        if b < 32768:
            return str(b)
        else:
            return "$"+str(b%32768)

    def run(self,commands=[]):

        while True:
            
            op = self.mem[self.i]%32768

            a  = b  = c  = -1
            if self.i+1<len(self.mem): a = self.mem[self.i+1]
            if self.i+2<len(self.mem): b = self.mem[self.i+2]
            if self.i+3<len(self.mem): c = self.mem[self.i+3]
                             
            if op==0: # # halt: 0 - stop execution and terminate the program
                print("{:6d} | HALT".format(self.i))
                self.i += 1

            elif op==1: # set: 1 a b - set register <a> to the value of <b>
                print("{:6d} | SET ${:d} {:s}".format(self.i,a%32768,self.rov(b)))
                self.i += 3

            elif op==2: # push: 2 a - push <a> onto the stack
                print("{:6d} | PUSH {:s}".format(self.i,self.rov(a)))
                self.i += 2

            elif op==3: # pop: 3 a - remove the top element from the stack and write it into <a>; empty stack = error
                print("{:6d} | POP ${:d}".format(self.i,a%32768))
                self.i += 2

            elif op==4: # eq: 4 a b c - set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                print("{:6d} | EQ ${:d} {} {}".format(self.i,a%32768,self.rov(b),self.rov(c)))
                self.i += 4

            elif op==5: # gt: 5 a b c - set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                print("{:6d} | GT ${:d} {} {}".format(self.i,a%32768,self.rov(b),self.rov(c)))
                self.i += 4

            elif op==6: # jmp: 6 a - jump to <a>
                print("{:6d} | JMP {:s}".format(self.i,self.rov(a)))
                self.i += 2

            elif op==7: # jt: 7 a b - if <a> is nonzero, jump to <b>
                print("{:6d} | JT {:s}".format(self.i,self.rov(a),self.rov(b)))
                self.i += 3

            elif op==8: # jf: 8 a b - if <a> is zero, jump to <b>
                print("{:6d} | JF {:s} {:s}".format(self.i,self.rov(a),self.rov(b)))
                self.i += 3

            elif op==9: # add: 9 a b c - assign into <a> the sum of <b> and <c> (modulo 32768)
                print("{:6d} | ADD {:s} {:s} {:s}".format(self.i,self.rov(a),self.rov(b),self.rov(c)))
                self.i += 4

            elif op==10: # mult: 10 a b c - store into <a> the product of <b> and <c> (modulo 32768)
                print("{:6d} | MULT {:s} {:s} {:s}".format(self.i,self.rov(a),self.rov(b),self.rov(c)))
                self.i += 4

            elif op==11: # mod: 11 a b c - store into <a> the remainder of <b> divided by <c>
                print("{:6d} | MOD {:s} {:s} {:s}".format(self.i,self.rov(a),self.rov(b),self.rov(c)))
                self.i += 4

            elif op==12: # and: 12 a b c - stores into <a> the bitwise and of <b> and <c>
                print("{:6d} | AND {:s} {:s} {:s}".format(self.i,self.rov(a),self.rov(b),self.rov(c)))
                self.i += 4

            elif op==13: # or: 13 a b c - stores into <a> the bitwise or of <b> and <c>
                print("{:6d} | OR {:s} {:s} {:s}".format(self.i,self.rov(a),self.rov(b),self.rov(c)))
                self.i += 4

            elif op==14: # not: 14 a b - stores 15-bit bitwise inverse of <b> in <a>
                print("{:6d} | NOT {:s} {:s}".format(self.i,self.rov(a),self.rov(b)))
                self.i += 3

            elif op==15: # rmem: 15 a b - read memory at address <b> and write it to <a>
                print("{:6d} | RMEM {:s} {:s}".format(self.i,self.rov(a),self.rov(b)))
                self.i += 3

            elif op==16: # wmem: 16 a b - write the value from <b> into memory at address <a>
                print("{:6d} | WMEM {:s} {:s}".format(self.i,self.rov(a),self.rov(b)))
                self.i += 3

            elif op==17: # call: 17 a - write the address of the next instruction to the stack and jump to <a>
                print("{:6d} | CALL {:s}".format(self.i,self.rov(a)))
                self.i += 2

            elif op==18: # ret: 18 - remove the top element from the stack and jump to it; empty stack = halt
                print("{:6d} | RET".format(self.i))
                self.i += 1

            elif op==19: # out: 19 a - write the character represented by ascii code <a> to the terminal
                print("{:6d} | OUT {:s}".format(self.i,self.rov(a)))
                self.i += 2

            elif op==20: # in: 20 a - read a character from the terminal and write its ascii code to <a>; 
                print("{:6d} | IN {:s}".format(self.i,self.rov(a)))
                self.i += 2

            elif op==21: # noop: 21 - no operation
                print("{:6d} | NOOP".format(self.i))
                self.i += 1

            else:
                #print("{:6d} | INVALID".format(self.i))
                print("{:6d} | VALUE {:d}".format(self.i,op))
                self.i += 1 

            if self.i > self.l:
                return

def main():
    d = Disassembler()
    d.readInput("synacor-challenge/challenge.bin")
    d.run()
        
if __name__ == "__main__":
    main()
