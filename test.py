import os
import re
# get the number of files for the copy_count property
a = 0
n = 1

listrange = '['+str(a)+'-'+str(n)+']'
name = "Mangalist"+listrange

path, dirs, files = os.walk("logs/info").next()
file_count = len([csv for csv in files if csv.find(name) != -1])
print file_count

test = "string"
print test.replace("!","").replace("i","")


