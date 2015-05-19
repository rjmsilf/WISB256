aantal=input()
tellen=0
for i in range(0,int(aantal)):
    hek=input()
    for j in hek:
        if ord(j)==35:
            tellen=tellen+1
L=int(tellen)*5
print('Om de hekjes in dit weiland te verven heb je '+str(L)+' liter verf nodig')