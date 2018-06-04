#!/usr/bin/python3

# secp256k1
a = 0; b = 7
prime = 2**256 - 2**32 -977
gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
G = (gx, gy)
order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
<<<<<<< HEAD
          
from FiniteFields import modInv

def pointDouble(P):
  if P[1] == 0 or P[0] is None:
    return (None, None)
  lam = ((3*P[0]*P[0]+a) * modInv(2*P[1], prime)) % prime
  x = (lam*lam-2*P[0]) % prime
  y = (lam*(P[0]-x)-P[1]) % prime
  return (x, y)

def pointAdd(P, Q):
  if Q[0] is None:
    return P
  if P[0] is None:
    return Q
  if Q[0] == P[0]:
    if Q[1] == P[1]:
      return pointDouble(P)
    else:
      return (None, None)
  lam = ((Q[1]-P[1]) * modInv(Q[0]-P[0], prime)) % prime
  x = (lam*lam-P[0]-Q[0]) % prime
  y = (lam*(P[0]-x)-P[1]) % prime
  return (x, y)

# double & add recursive
def pointMultiplyRecursive(n, P):
  n = n % order
  if n == 0 or P[0] is None:
    return (None, None)
  if n == 1:
    return P
  if n % 2 == 1: # addition when n is odd
    return pointAdd(P, pointMultiplyRecursive(n - 1, P))
  else:          # doubling when n is even
    return pointMultiplyRecursive(n//2, pointDouble(P))

# double & add
def pointMultiply(n, P):
  n = n % order
  result = (None, None) # initializing result to (None,None)
  temp = P              # temp variable to store doubled values
  while n>0 :
    if n & 1:
      result = pointAdd(result,temp) # adding when lsb of n is 1
    temp = pointDouble(temp) # doubling
    n = n>>1            # shift bits of factor
  return result
=======

from EllipticCurve import EllipticCurve, pointAdd, pointDouble, pointMultiply, modInv
ec = EllipticCurve(a, b, prime, G, order)

def main():
  ec.checkPoint(G)
  print(ec.G)
  print(pointAdd(ec.G, ec.G, ec))
  print(pointDouble(ec.G, ec))
  print(pointMultiply(2, ec.G, ec))
  print(pointMultiply(ec.order, ec.G, ec))
  print(pointMultiply(ec.order+1, ec.G, ec))
  print(pointMultiply(ec.order+2, ec.G, ec))

if __name__ == "__main__":
  # execute only if run as a script
  main()
>>>>>>> master
