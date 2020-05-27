#!/usr/bin/env python

# Imports
import z3

# Initialisation
s = z3.Solver()
serial = []
for i in range(13):
    serial.append(z3.BitVec("serial_{}".format(i), 32))    
running_sum = [3]
    
# Constraints
for digit in serial:
    s.add(z3.And(digit>48, digit<=57))

for i in range((len(serial)-1)):
    current_sum = z3.BitVec("sum_{}".format(i), 32)
    s.add(current_sum==running_sum[-1]+((2*running_sum[-1])^(serial[i]-48)))
    running_sum.append(current_sum)
    
s.add(serial[-1]==(running_sum[-1]%10+48))

# Constraint solving
if s.check() == z3.sat:
    m = s.model()
    inp = []
    for digit in serial:
    	inp.append(m[digit].as_long())
    print("".join([chr(x) for x in inp]))
else:
	print("Set of constraints unsatisfiable!")
