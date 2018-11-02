#!usr/bin/python3
#pythonTipProblems.py
#Problem1:a+b
"""
a,b=1,2
print a+b
#Problem2:sort
L=[4,2,1,0]
L.sort()
#Problem3:reverse string
a = 'xydz'
b = ""
for i in range(len(a)-1, -1, -1):
    b += a[i];
print(b)
a = 'xydz'
b = list(a)
b.reverse()
print(''.join(b))
a = 'xydz'
print(a[::-1])
#Problem4:print out keys of dict
a={1:1,2:2,3:3}
b = list(a.keys())
b.sort()
print(','.join(str(x) for x in b))
#Problem5:odd position charactor in string
a=‘xyzwd’
for i in range(0,len(a),2):
    b += a[i]
print(b)
#Problem6:prime number in 100
def isPrime(n):
    for i in range(2,n,1):
        if n%i == 0:
            return False
    return True

primeNumber = []
for i in range(2,100):
    if isPrime(i):
        primeNumber.append(i)
print(" ".join(str(x) for x in primeNumber))

def sushu(n):
    sushu_list = [2,3,5,7]
    a = []
    b = list(range(2, n))
    for i in b:
        for j in sushu_list:
            if i != j and i % j == 0:
                break
        else:
            a.append(str(i))
    print(' '.join(a))
sushu(100)
#Problem7:area of rectangle
def getValue(a, b):
    area = a*b
    rd = (a+b)*2
    return [str(area), str(rd)]
a=3
b=4
print(' '.join(getValue(a,b)))
print("{} {}".format(a*b,2*(a+b)))

#Problem8:中位数
L=[1,0,2,3,4]
L.sort()
size = len(L);
if size%2 == 0:
    print((L[size//2-1]+L[size//2])/2.0)
else:
    print(L[size//2])

#Problem11:相乘结尾0的个数
L=[2,8,10,50,3,25]
def getNumOffactor(num, factor):
    count = 0
    while num%factor==0:
        count +=1
        num = num//factor
    return count

num_2,num_5=0,0
for i in L:
    num_2 += getNumOffactor(i, 2)
    num_5 += getNumOffactor(i, 5)
print(min(num_2,num_5))
#Problem12:相乘结尾奇偶性
L=[2,8,1,5,3,25]
it = map(lambda x:x%2, L)
count_0,count_1=0,0
for i in it:
    if i==0:
        count_0+=1
    else:
        count_1+=1
if count_0>count_1:
    print(0)
else:
    print(1)

#Problem13:二进制表达下1的个数
a = -55
b = bin(a)
print(b)
count = b.count('1')
print(count)

#Problem14:输出python之禅
import this
print(this.s)
"""
#Problem15:大写字母转小写
a='a#$$#%dfaFajfdkFDSA234.ja.'
print(a.lower())
