# Synacor Challenge

https://challenge.synacor.com

## Notes

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
* Coin puzzle solution: (9, 2, 5, 7, 3) blue, red, shiny, concave, corroded
* Hacked the VM to read a prepackaged list of instructions
* Hacked the interface to print and modify the register. Register 7 is usually 0, if changed to any other number I get:
> A strange, electronic voice is projected into your mind:
>  "Unusual setting detected!  Starting confirmation process!  Estimated time to completion: 1 billion years."

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
  * Found first 4 codes

