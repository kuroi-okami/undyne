# #####################################################################################################################
# Project UNDYNE - DEMO 1: Motors go spin... Beholdeth.
# #####################################################################################################################

from motordriver import motordriver
import time

md = motordriver()
print("Welcome to the Undyne Motor Demo")
print("Commencing steps through 100, 50, -50 and -100 demand levels")
print(":D")
md.initialise()
md.setdemand([100, 100, 100, 100])
time.sleep(5)
md.setdemand([50, 50, 50, 50])
time.sleep(5)
md.setdemand([-50, -50, -50, -50])
time.sleep(5)
md.setdemand([-100, -100, -100, -100])
time.sleep(5)
md.deactivate()
print("Show's over folks... Hopefully it worked as planned...")






















