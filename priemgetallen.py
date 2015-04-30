def pr(getal):
    n=2
    while n<getal:
        if getal%n == 0:
            if getal > 2:
            return
        n=n+1
    if getal > 2:
        print(str(getal) +' is een priem!')
    return

def givepriem(k):
    for char in range(k):
        print(pr(k))