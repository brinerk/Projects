import strutils
import os

var counter = 0
var pcount = 0
var a = "0"
var b = "0"
var c = "0"

let f = paramStr(1)
var labels = newSeq[string](0)
var addresses = newSeq[string](0)

#first pass for labels and data
for line in lines(f):
  var curLine = line.split({' ',','})
  if curLine[0].startsWith('@'):
    if curLine.len == 3:
      labels.add(curLine[0])
      addresses.add(toHex(pcount*3,2))
    elif curLine[0].startsWith(';'):
      continue
    else:
      labels.add(curLine[0])
      addresses.add(toHex(pcount*3,2))
      continue
  pcount+=1

#second pass
for line in lines(f):
  var curLine = line.split({' ',','})
  #echo curLine
  if curLine[0].startsWith('@'):
    if curLine.len > 1 and curLine[1] == ".data":
      echo toHex(parseInt(curLine[2]),2), " 00 00"
      continue
    else:
      continue
  if curLine[0].startsWith(';'):
    continue
  case curLine[0]:
    of "SUBLEQ":
      for i in 0..<curLine.len:
        for j in 0..<labels.len:
          if curLine[i] == labels[j]:
            #this is awful
            curLine[i] = intToStr(fromHex[int](addresses[j]))
      #echo curLine
      a = toHex(parseInt(curLine[1]),2)
      #this is making it worse
      b = toHex(parseInt(curLine[2]),2)
      c = toHex((counter*3)+3,2)
      if curLine.len == 4:
        echo a," ",b," ",toHex(parseInt(curLine[3]),2)
      else:
        echo a," ",b," ",c
  counter+=1 
