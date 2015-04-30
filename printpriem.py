def pr(getal):
    n=2
    while n<getal:
        if getal%n == 0:
            return False
        n=n+1
    return True

def pr2(getal2,getal3):
    for i in range(getal2,getal3):
        if pr(i) == True:
            print(i)
    return

pr2(3,3000)