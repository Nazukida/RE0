#尝试python用法，顺便看看我之前那个conda能不能用
def isprime(m, n):
    s = 0
    for num in range(m, n + 1):
        is_prime = True
        for i in range(2, n):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            s += 1
    return s
m = int(input("第一个数"))
n = int(input("第二个数"))

print(f"在{m}和{n}之间有{isprime(m, n)}个素数")
#事实证明不行
#还是得配环境