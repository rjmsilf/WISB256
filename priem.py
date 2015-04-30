def pr(getal):
    for i in range(2,getal):
        if getal%i == 0:
            return False
    return getal


print(pr(191))