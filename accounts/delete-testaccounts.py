#delete numbered accounts using gam. be careful here."

import os

for i in range (1,14):
    st="teststudent%s@students.kiron.ngo" % i
    ex="./src/gam.py delete user %s" % st
    os.system(ex)
