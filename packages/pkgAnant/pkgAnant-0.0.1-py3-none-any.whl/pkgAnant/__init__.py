import random
import string

def generate_pass():

    # using random for range
    len=random.randint(6, 12)

    # using string to generate characters
    lower=string.ascii_lowercase
    upper=string.ascii_uppercase
    num=string.digits

    # to select at least one lower, one upper, one number
    password=random.choice(lower)+random.choice(upper)+random.choice(num)

    # filling password with remaining length
    password+=''.join(random.choices(lower+upper+num,k=len-3))

    # shuffling the password by creating a list
    password_list=list(password)
    random.shuffle(password_list)
    password=''.join(password_list)
    return password

# password=generate_pass()
# print(password)