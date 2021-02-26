# Synacor Challenge

https://challenge.synacor.com

## Notes on progress

### VM Implementation and text adventure

* Virtual machine implementation was relatively simple, self test at beginning helped quite a lot the debugging

* A text adventure!

* Grues are dangerous, they live in the darkness. I need light to proceed.

* After the ladder: west, north, south, north to find the oil can

* Ruins:
> You stand in the massive central hall of these ruins.  The walls are crumbling, and vegetation has clearly taken over.  Rooms are attached in all directions.  There is a strange monument in the center of the hall with circular slots and unusual symbols.  It reads:
_ + _ * _^2 + _^3 - _ = 399

* Coins
  * Red coin (2 dots)
  * Concave coin (7 dots)
  * Corroded coin (triangle on one side)
  * Blue coin (9 dots)
  * Shiny coin (pentagon on one side)

* Coin puzzle solution: (9, 2, 5, 7, 3) blue, red, shiny, concave, corroded (see Jupyter notebook: easy to brute-force using `itertools` permutations)

* Hacked the VM to read a prepackaged list of instructions to quick reach teleporter

* To change teleporter behaviour I need to find the right value to set to register 7 before issuing the `use teleporter` command (see `strangebook.txt`)

### Teleporter puzzle

* Hacked the interface to print and modify the register accepting custom commands

* Register 7 is usually set to 0, if changed to any other number and then `use teleporter` issued the code gets into a very intensive (and probably inefficient) calculation:

> A strange, electronic voice is projected into your mind:
>  "Unusual setting detected!  Starting confirmation process!  Estimated time to completion: 1 billion years."

* Printing out loop instructions and register changes after the above message, I notice a loop of some sort happening after instruction at memory 5489, that trigger repeating instructions that begins at memory address 6027:
> 6027 |  7 32768  6035     9 || REG =  0:     4 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6035 |  7 32769  6048     9 || REG =  0:     4 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6048 |  2 32768     9 32769 || REG =  0:     4 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6050 |  9 32769 32769 32767 || REG =  0:     4 | 1:     0 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6054 | 17  6027     1 32769 || REG =  0:     4 | 1:     0 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  

* The loop sometimes gets bigger involving instructions 18:
> 6027 |  7 32768  6035     9 || REG =  0:     0 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6030 |  9 32768 32769     1 || REG =  0:     2 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6034 | 18     7 32769  6048 || REG =  0:     2 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6047 | 18     2 32768     9 || REG =  0:     2 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6056 |  1 32769 32768     3 || REG =  0:     2 | 1:     2 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6059 |  3 32768     9 32768 || REG =  0:     1 | 1:     2 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6061 |  9 32768 32768 32767 || REG =  0:     0 | 1:     2 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 6065 | 17  6027    18    11 || REG =  0:     0 | 1:     2 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  

* Just before the routine starting at line 6017 gets called, these are the instructions:
> 5483 |  1 32768     4     1 || REG =  0:     4 | 1:  5445 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 5486 |  1 32769     1    17 || REG =  0:     4 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  
> 5489 | 17  6027     4 32769 || REG =  0:     4 | 1:     1 | 2:     3 | 3:    10 | 4:   101 | 5:     0 | 6:     0 | 7:     1 |  

  The first two (opcode 1) set registers 0 to 4 and register 1 to 0. The third (opcode 17) call instructions (function) starting al line 6027. 

* To proceed further I would need a more serious disassembler (and more free time) to decode what the instructions starting at line 6027 do! 

* Implemented a disassebler, saving program in `program.txt`. Noted that part of the memory does not correposnd to architecture opcodes, these must be values storing the sentences used by the text adventure engine: saving them as `VALUE` instructions.

* Here a more readable version of what happens before the loop:

>  5483 | SET $0 4  
>  5486 | SET $1 1  
>  5489 | CALL 6027  
>  5491 | EQ $1 $0 6  
>  5495 | JF $1 5579  

* As already discovered before, line 5482 sets $0 to 4 and $1 to 1, then call function at line 6027. 

* Whatever the function does (or would do, given the almost infinite execution rime!) then line 5941 sets $1 to 1 if the content of $0 is equal to 6, otherwise to 0. If $1 is set tyo 1, then line 5495 would jump to instruction at line 5579, that I guess is what would trigger the alternative behaviour of the teleporter. So, I need to find out what the function at line 6027 does and how it would set $0 to 6, given the initial value $0(4) and $1(1), and an unknown value of $7 I need to set.

* I suspect that, even assuming I can figure out what line 6027 do, it would still take quite some time even if I properly set $7. I would probably need to set $0 to 6, $7 to whatever value would lead to get $0 to be equal to 6, and bypass the call at line 5489 (e.g. replace it with a `NOOP` opcode). 

* I could imagine to simply bypass instruction at line 5489 and set $0 to 6, but I won't know what $7 should be. I guess this can generate some problem, given that the strange book text warns that:
> The second destination, however, is predicted to require a very specific energy level in the eighth register.  The teleporter must take great care to confirm that this energy level is exactly correct before teleporting its user!  If it is even slightly off, the user would (probably) arrive at the correct location, but would briefly experience anomalies in the fabric of reality itself.

* I implemented the hack to skip the call to routine 6027 and I can indeed jump, but as expected I get a new error:
> A strange, electronic voice is projected into your mind:  
>  "Miscalibration detected!  Aborting teleportation!"  
> Nothing else seems to happen.  
So I indeed need to compute a proper (_calibrated!_) value for $7... :-(

## Codes

- Code 1: iwAXllQmiZDv (it was in the instructions!)
- Code 2: XstgJSxeHSHA (first simple run of the VM)
- Code 3: IhBRSqeTnzgw (after self test)
- Code 4: XEBwBmFKDmLA (using tablet)
- Code 5: yZWfuTMfgZkV (chiseled on the wall of one of the passageways where the can is found)
- Code 6: gbwPqnSdSlUV (after having used the teleporter, found after solving the coin puzzles)


## ChangeLog

* 2021-02-24: 
  * Implemented basic virtual machine and status saving mechanism. 
  * Added saving of VM status and command list to track/repeat progress.
  * Found first 6 codes

* 2021-02-25:
  * More output to try to figure out what the teleporter checking algorithm does.
  
* 2021-02-26:
  * Implemented disassembler to scrutinize program
  * Studying the program...
  * Hack to bypass call to routine 6027
