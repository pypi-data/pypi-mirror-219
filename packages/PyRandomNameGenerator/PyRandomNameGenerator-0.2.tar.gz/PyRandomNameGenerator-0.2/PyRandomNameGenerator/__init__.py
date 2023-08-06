import random

def generateRandomName():
    first_name = ['John', 'Jane', 'Michael', 'Emily','David','Joe','Albert','Elon']
    last_name = ['Smith', 'Johnson', 'Williams', 'Brown', 'Warner', 'Steaven', 'Mark', 'Mohib']
    
    first = random.choice(first_name)
    last = random.choice(last_name)
    
    return f"{first} {last}"
