import math
h = 6.626068 * (10**-34) #joules/sec
c = 2.997925 * (10**8) #m/s
K = 1.38066 * (10**-23) #joules/degree
lambda_ = 10**-5 # meters
C1 = 2*h*c*c*(lambda_)**-5 #Watts / 
C2 = (h*c)/(lambda_*K)
I = 9.8 / (10**-6) # divide by 1 * 10^-6 to convert the mum to meters to be compatible with K1

print(C1) #1191042919.6552804 W m^-3 sr^-1
print(C2) #1438.7651491967606 K

T = C2/math.log((C1/I) + 1)

print(T) #299.21931528251974

