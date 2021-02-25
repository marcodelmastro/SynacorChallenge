# Synacor Challenge

https://challenge.synacor.com

## Notes on progress

* Virtual machine implementation was relatively simple, self test at beginning helped quite a lot the debugging
* A text adventure!

* Grues are dangerous, they live in the darkness. I need light to proceed.

* After the ladder: west, north, south, north to find the oil can

* Ruins:
> You stand in the massive central hall of these ruins.  The walls are crumbling, and vegetation has clearly taken over.  Rooms are attached in all directions.  There is a strange monument in the center of the hall with circular slots and unusual symbols.  It reads:
_ + _ * _^2 + _^3 - _ = 399

* Coins
  * Red coin (2 dots)
  * Concanve coin (7 dots)
  * Corroded coin (triangle on one side)
  * Blue coin (9 dots)
  * Shiny coin (pentagon on one side)

* Coin puzzle solution: (9, 2, 5, 7, 3) blue, red, shiny, concave, corroded (see Jupyter notebook: easy to brute-force using `itertools` permutations)

* Hacked the VM to read a prepackaged list of instructions to quick reach teleporter

* To change teleporter behaviour I need to find the right value to set to register 7 before issuing the `use teleporter` command (see `strangebook.txt`)

* Hacked the interface to print and modify the register accprting custom commands

* Register 7 is usually set to 0, if changed to any other number and then `use teleporter` issued the code gets into a very intensive (and probably inefficient) calculation:

> A strange, electronic voice is projected into your mind:
>  "Unusual setting detected!  Starting confirmation process!  Estimated time to completion: 1 billion years."

* Printing out loop instructions and register changes after the above message, I notice a loop of some sort happening after instruction at memory 5489, that trigger repeating instructions that begins at memory addredd 6027:
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

* To proceed further I need a more serious disassembler (and more free time)! Stop for now...


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
