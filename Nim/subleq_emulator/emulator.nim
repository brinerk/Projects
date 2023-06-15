import os
import strutils

let f = readFile(paramStr(1))

var programCounter = 0

#enter file to memory
var mem = f.split({' ','\n'})
var memInt = newSeq[int](0)

#clean up empty entries (space at end)
for i in 0..<mem.len:
  if mem[i] == "":
    mem.del(i)

#fill out mem
while mem.len < 255:
  mem.add("00")

for i in 0..<mem.len:
  memInt.add(fromHex[int](mem[i]))

#make sure program is under 255 bits
if mem.len > 255:
  echo "Error: Mem Overflow"
  quit(QuitFailure)

#memA = memA - memB IF memA <= 0 goto memC
#echo memInt

while programCounter <= 252:
  #echo ">", memInt[programCounter]
  if memInt[programCounter+1] == 254:
    memInt[memInt[programCounter]] = parseInt(readLine(stdin))
  if memInt[programCounter] == 254:
    #echo (memInt[programCounter] - memInt[memInt[programCounter+1]])
    echo ">", (memInt[memInt[programCounter+1]])
    programCounter += 3
    continue
  if memInt[programCounter] == 255:
    break
  memInt[memInt[programCounter]] = memInt[memInt[programCounter]] - memInt[memInt[programCounter+1]]
  if memInt[memInt[programCounter]] <= 0:
    programCounter = memInt[programCounter+2]
    continue
  #echo memInt
  programCounter += 3 

#echo memInt

#[
echo mem.len
echo memInt
echo programCounter
]#
