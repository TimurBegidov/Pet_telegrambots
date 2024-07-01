
n=4
count=1
k=5
read=5

def dec (k):
    def counter(func):
        def wrapper(cn,r):
            read=1*k
            func(cn, r)
            return read
        return wrapper
    return counter

@dec(k)
def counte(cn,r):
    result = 0
    i=0
    for i in range(10):
        result+=cn*r
    print(result)

print(counte(5,5))
