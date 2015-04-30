def pr(getal):
    n=2
    while n<getal:
        if getal%n == 0:
            return False
        n=n+1
    return True

pr(1000003)
print(pr(1000003))