# print(3 / 0)

# a = kutuyi

# fileDir = ''
# f = open(fileDir, 'r')  # ← 空字符串不是合法路径，抛出 FileNotFoundError
# f.close()

try:
    fh = open('testfile.txt', 'r')
    s = fh.read()
    fh.close()
    print(s)
except FileNotFoundError:
    print("Error: can't find file")
else:
    print("Read succeeded!")

print("Haha")  # 无论是否异常，这行总会执行（它在 try 结构之外）

def get_number():
    number = float(input("Enter a float number: "))
    return number

i = 0.0
while i != 8.0:
    try:
        i = get_number()
    except ValueError:
        print("Error: invalid input, please enter a float number.")
    else:
        print("You entered:", i)
    print('haha')
print("You entered 8.0, exiting loop.")

class ShortInputException(Exception):
    def __init__(self, length, atleast):
        Exception.__init__(self)      # 调用父类构造函数
        self.length = length          # 保存实际长度
        self.atleast = atleast        # 保存最低要求

    def shortInputExceptionAction(self):
        print('shortInputException can do many operations here')
        print('Your input length %d, but the length should be at least %d'% (self.length, self.atleast))

try:
    s = input('Enter Something: ')
    if len(s) < 3:
        raise ShortInputException(len(s), 3)  # 手动抛出异常
except KeyboardInterrupt:
    print('Why did you do interrupt me?')
except ShortInputException as x:    # x 就是被抛出的那个异常对象
    x.shortInputExceptionAction()   # 调用异常对象的方法
else:
    print('No exception was raised.')
    
def KelvinToFahrenheit(Temperature):
    try:
        assert Temperature >= 0
        return (Temperature - 273) * 1.8 + 32
    except AssertionError:
        print('So cold, temperature below zero')
        return None
print(KelvinToFahrenheit(273))    # → 32.0 ✓
print(int(KelvinToFahrenheit(505.78)))  # → 451 ✓
print(KelvinToFahrenheit(-5))     # → None