#!/usr/bin/env python3

from collections import deque
import pickle
import time

class VM:
    def __init__(self,filename=""):
        self.mem = [ 0 for i in range(2**15)]
        self.reg = {}
        for n in range(8):
            self.reg[n] = 0
        self.stack = deque()
        if filename !="":
            self.readInput(filename)
        self.i = 0
        self.input = []

    def initialize(self,prog):
        i = 0
        for j in prog:
            self.mem[i] = j
            i+=1
        
    def readInput(self,filename="synacor-challenge/challenge.bin"):
        i = 0
        with open(filename, "rb") as f:
            read = f.read(2)
            while read:
                self.mem[i] = int.from_bytes(read, "little")
                read = f.read(2)
                i+=1 

    def printReg(self):
        print("REG =  ",end="")
        for k in self.reg.keys():
            print("{:1d}: {:5d} | ".format(k,self.reg[k]),end="")
        print()

    def hackTeleporter(self):
        # NOOP to skip call to teleporter verification algorithm
        self.mem[5489] = 21 
        self.mem[5490] = 21 
        #self.reg[0] = 6 # this is not enough, $0 get changed by `use teleporter` before the check $6==6
        # Removing $0==6 check (lines from 5491 to 5494)
        self.mem[5491] = 21
        self.mem[5492] = 21
        self.mem[5493] = 21
        self.mem[5494] = 21
        
    def rov(self,b): # register or value
        if b < 32768:
            return b
        else:
            return self.reg[b%32768]

    def run(self,commands=[]):

        lastcommand = ""
        #timestr = time.strftime("%Y%m%d-%H%M%S")
        #filenameout = "actions_"+timestr+".txt"
        filenameout = "actions.txt"
        
        with open(filenameout,"w") as fout:
        
            while True:
            
                op = self.mem[self.i]%32768

                a  = b  = c  = -1
                if self.i+1<len(self.mem): a = self.mem[self.i+1]
                if self.i+2<len(self.mem): b = self.mem[self.i+2]
                if self.i+3<len(self.mem): c = self.mem[self.i+3]                

                if lastcommand=="use teleporter":
                    print("use teleporter")
                    lastcommand="loop"
                
                #if self.reg[7]!=0:
                #    print("{:5d} | {:2d} {:5d} {:5d} {:5d} || ".format(self.i,op,a,b,c),end="")
                             
                if op==0: # # halt: 0 - stop execution and terminate the program
                    print("GAME OVER")
                    return

                elif op==1: # set: 1 a b - set register <a> to the value of <b>
                    self.reg[a%32768] = self.rov(b)
                    self.i += 3

                elif op==2: # push: 2 a - push <a> onto the stack
                    self.stack.append(self.rov(a))
                    self.i += 2

                elif op==3: # pop: 3 a - remove the top element from the stack and write it into <a>; empty stack = error
                    if len(self.stack):
                        self.reg[a%32768] = self.stack.pop()
                    else:
                        print("ERROR Stack empty")
                    self.i += 2

                elif op==4: # eq: 4 a b c - set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                    if self.rov(b)==self.rov(c):
                        self.reg[a%32768] = 1
                    else:
                        self.reg[a%32768] = 0
                    self.i += 4

                elif op==5: # gt: 5 a b c - set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                    if self.rov(b)>self.rov(c):
                        self.reg[a%32768] = 1
                    else:
                        self.reg[a%32768] = 0
                    self.i += 4

                elif op==6: # jmp: 6 a - jump to <a>
                    self.i = self.rov(a)

                elif op==7: # jt: 7 a b - if <a> is nonzero, jump to <b>
                    if self.rov(a)!=0:
                        self.i = self.rov(b)
                    else:
                        self.i += 3

                elif op==8: # jf: 8 a b - if <a> is zero, jump to <b>
                    if self.rov(a)==0:
                        self.i = self.rov(b)
                    else:
                        self.i += 3

                elif op==9: # add: 9 a b c - assign into <a> the sum of <b> and <c> (modulo 32768)
                    self.reg[a%32768] = (self.rov(b)+self.rov(c))%32768
                    self.i += 4

                elif op==10: # mult: 10 a b c - store into <a> the product of <b> and <c> (modulo 32768)
                    self.reg[a%32768] = (self.rov(b)*self.rov(c))%32768
                    self.i += 4

                elif op==11: # mod: 11 a b c - store into <a> the remainder of <b> divided by <c>
                    self.reg[a%32768] = (self.rov(b)%self.rov(c))%32768
                    self.i += 4

                elif op==12: # and: 12 a b c - stores into <a> the bitwise and of <b> and <c>
                    self.reg[a%32768] = (self.rov(b)&self.rov(c))%32768
                    self.i += 4

                elif op==13: # or: 13 a b c - stores into <a> the bitwise or of <b> and <c>
                    self.reg[a%32768] = (self.rov(b)|self.rov(c))%32768
                    self.i += 4

                elif op==14: # not: 14 a b - stores 15-bit bitwise inverse of <b> in <a>
                    self.reg[a%32768] = (~self.rov(b))%32768
                    self.i += 3

                elif op==15: # rmem: 15 a b - read memory at address <b> and write it to <a>
                    self.reg[a%32768] = self.mem[self.rov(b)]
                    self.i += 3

                elif op==16: # wmem: 16 a b - write the value from <b> into memory at address <a>
                    self.mem[self.rov(a)] = self.rov(b)
                    self.i += 3

                elif op==17: # call: 17 a - write the address of the next instruction to the stack and jump to <a>
                    self.stack.append( self.i+2 ) # "next instruction" is the op after current if no jump
                    self.i = self.rov(a)

                elif op==18: # ret: 18 - remove the top element from the stack and jump to it; empty stack = halt
                    if len(self.stack):
                        self.i = self.stack.pop()
                    else:
                        print("ERROR Stack empty")
                        return

                elif op==19: # out: 19 a - write the character represented by ascii code <a> to the terminal
                    print(chr(self.rov(a)),end="")
                    self.i += 2

                elif op==20: # in: 20 a - read a character from the terminal and write its ascii code to <a>; 
                    # it can be assumed that once input starts, it will continue until a newline is encountered; 
                    # this means that you can safely read whole lines from the keyboard and trust that they will be fully read
                    if not len(self.input):
                        # save status
                        #with open("status.sav", "wb") as f:
                        #    pickle.dump(self.mem,f)
                        #    pickle.dump(self.reg,f)
                        #    pickle.dump(self.stack,f)
                        #    pickle.dump(self.i,f)
                        if len(commands)==0:
                            command = input()
                        else:
                            command = commands.pop(0)
                            print(command)
                        lastcommand = command
                        fout.write(command+"\n")

                        if len(command):
                            if command[0]=='Q':
                                print("GOODBYE")
                                return
                            elif command[0]=="P":
                                print(self.reg)
                            elif command[0]=="T":
                                self.reg[7] = int(command.split(" ")[1])
                                self.hackTeleporter()
                                self.printReg()

                        for c in command:
                            self.input.append(ord(c))
                        self.input.append(ord('\n'))
                    self.reg[a%32768] = self.input.pop(0)
                    self.i += 2

                elif op==21: # noop: 21 - no operation
                    self.i += 1

                if self.i > len(self.mem):
                    return
                
                #if self.reg[7]!=0:
                #    self.printReg()



def main():

    import sys

    vm = VM()
     
    #import os
    #files = os.listdir('.')
    #mem = []
    #if 'status.sav' in files:
    #    print("Welcome to the Synacor Challenge!")
    #    ans = input("Do you want to start from last saved status? [y/n]")
    #    if ans[0]=="Y" or ans[0]=='y':
    #        with open("status.sav", "rb") as f:
    #            mem = pickle.load(f)
    #            reg = pickle.load(f)
    #            stack = pickle.load(f)
    #            i = pickle.load(f)
    #    if len(mem):
    #        vm.initialize(mem)
    #        vm.i = i
    #        vm.reg = reg
    #        vm.stack = stack
    #    else:
    
    vm.readInput("synacor-challenge/challenge.bin")

    #with open('moves.txt') as fmoves:
    if (len(sys.argv)>1):
        with open(sys.argv[1], 'r') as fmoves:
            commands = [ c.strip("\n") for c in fmoves.readlines()]
            if (len(commands)):
                print("Synacor Challenge: using moves from {} as pre-recorded actions...".format(sys.argv[1]))
                vm.run(commands)
            else:
                vm.run()
    else:
        vm.run()
        
if __name__ == "__main__":
    main()
