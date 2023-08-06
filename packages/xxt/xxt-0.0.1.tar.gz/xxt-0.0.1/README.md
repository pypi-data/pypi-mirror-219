# XXT

XXT is a multi-purpose library

## Uses

> - Wait function
> - Clear function
> - Functions to get time and date
> - Classes for numbers and random choices

## Installation

```
pip install xxt
```

## Code Example

```py
import xxt

ten = xxt.Number(10) #make a number object
print(ten) # print the traits of ten

r = xxt.Random() #make a random choice object
print(r.integer(1, 10)) #print random number between 1 and 10

xxt.clear() #clear the console/terminal
xxt.wait(1) #waits one second

print(xxt.gettime, "on" xxt.getdate) #prints (the time) on (the date) in format - day, month, year
```
