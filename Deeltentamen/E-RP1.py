iets=input()
a=iets.split()

def reken(n):
    print(a)
    for i in range(0,n):
        print(i)
        if ord(a[i])==42:
            antwoord=int(a[i-2])*int(a[i-1])
            a[i]=str(antwoord)
            print(a[i])
            del(a[(i-2):i])
            return a
        elif ord(a[i])==43:
            antwoord1=int(a[i-2])+int(a[i-1])
            a[i]=antwoord1
            del(a[(i-2):i])
            return a
        elif ord(a[i])==45:
            antwoord2=int(a[i-2])-int(a[i-1])
            a[i]=str(antwoord2)
            del(a[(i-2):i])
            return a
        elif ord(a[i])==47:
            antwoord3=int(a[i-2])/int(a[i-1])
            a[i]=str(antwoord3)
            del(a[(i-2):i])
            return a

while len(a)>1:
        reken(len(a))
print(a)

# ik krijg het niet voor elkaar om mijn nieuwe vervangde element in a als string toe te voegen, dus erna staat er 12 i.p.v. '12'