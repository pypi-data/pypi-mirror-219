import random
import array

max_length = 12

numerals = ['0','1','2','3','4','5','6','7','8','9']
lowerCaps = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upperChars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


type(numerals)
combinedChars = numerals + lowerCaps + upperChars

# print(combinedChars)

passLength = random.randint(6,12)
# print(passLength)

def custom_choice(combinedChars):
    idx = random.randint(0,len(combinedChars)-1)
    return combinedChars[idx]


password = ""
for _ in range(passLength):
    password += custom_choice(combinedChars)

#print(password)

gen_password = list(password)
random.shuffle(gen_password)

def generatePass():
    print(''.join(gen_password))

