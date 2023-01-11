import requests
import time

w0 = open("test.txt", "a")

for i in range(0,10):
    time.sleep(0.25)
    w0.write("(str(data))")
    w0.write('\n')
    print(i)