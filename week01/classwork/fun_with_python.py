

class MyClass:
    def __init__(self, my_parameter: int) -> None:
        self.my_parameter = my_parameter

def fun(my_int, my_str, my_obj) -> None:
    print(my_int)
    print(my_str)
    print(my_obj)

my_list = []
#fun("dsfdsa", 10, my_list)

xyz = MyClass(50)
#print(xyz.my_parameter)
#print(id(xyz))

def modify_string(s):
    print(f'inside modify_string: {id(s)}')
    s = "hijklmn"
    print(f'after modified: inside modify_string: {id(s)}')
    
my_string = "abcdefg"
#modify_string(my_string)
#print(f'outside function {id(my_string)}')

def modify_int(i):
    print(f'inside modify_int: {id(i)}')
    i += 10
    print(f'after modified: inside modify_int: {id(i)}')

i = 20
#modify_int(i)
#print(f'outside function {id(i)}')

def modify_list(my_list: list):
    print(f'inside modify_list: {id(my_list)}')
    my_list.append(10)
    print(f'after modified: inside modify_list: {id(my_list)}')

modify_list(my_list)
my_list.append(6)
print(f'outside modify_list: {id(my_list)}')