import random
import string

def nipuns_password():
    length = random.randint(6, 12)
    p1 = []
    #random digit generated
    p1.append(random.choice(string.digits)) 
    
    #here i add random uppercase alphabet
    p1.append(random.choice(string.ascii_uppercase))  
    
    #here i add random lowercase alphabet
    p1.append(random.choice(string.ascii_lowercase))
    

    for i in range(length - 3):
        p1.append(random.choice(string.ascii_letters + string.digits))
        #now i joined whole password in single string

    return ''.join(p1)

p1 = nipuns_password()
print(p1)

