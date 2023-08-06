import random
import string

length = 12

while True:
    passw = random.choices(string.ascii_lowercase, k=1) + \
               random.choices(string.ascii_uppercase, k=1) + \
               random.choices(string.digits, k=1) + \
               random.choices(string.ascii_letters + string.digits, k=length-3)
    random.shuffle(passw)
    passw = ''.join(passw)
    
    if (any(c.islower() for c in passw) and
        any(c.isupper() for c in passw) and
        any(c.isdigit() for c in passw)):
        break

print(passw)
