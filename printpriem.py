def pr(getal):
    for i in range(2,getal):
        if getal%i == 0:
            return False
    return True

def pr2(getal2,getal3):
    for i in range(getal2,getal3):
        if pr(i) == True:
            print(i)
    return

pr2(3,3000)