def pr(getal):
    n=2
    while n<(getal/2):
        if getal%n == 0:
            return False
        n=n+1
    return True
priemlijst=[]

def pr2(getal2,getal3):
    while getal2<getal3:
        if pr(getal2) == True:
            priemlijst.append(int(getal2))
            getal2=getal2+1
            pr2(getal2,getal3)
            return
        elif pr(getal2) == False:
            getal2=getal2+1
            pr2(getal2,getal3)
            return
    priemtekst=open('priem'+str(getal3)+'.txt', 'w')
    i=0
    while i<len(priemlijst)-1:
        line=priemlijst[i]
        priemtekst.write('%d \n' %(priemlijst[i]))
        i=i+1
    priemtekst.close()
    return

def pr3(getal4,getal5,getal6):
    import os
    while (getal4+getal5)<getal6:
        #try:
        #import os
        print(getal4+getal5)
        #os.remove('priem'+str(getal4+getal5)+'.txt')
        #except:
        pr2(getal4,getal4+getal5)
        getal4=getal4+getal5
    return

