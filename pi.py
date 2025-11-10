import mpmath

mpmath.mp.dps = 1000  # Set decimal places to 1000
pi_val = str(mpmath.mp.pi)
print(pi_val)
