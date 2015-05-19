aantal=input()
if aantal[0]=='U':
    antwoord=aantal[0:-1]
    a=antwoord.split()
    print(len(a))
else:
    antwoord2='ug '*(int(aantal)-1)+str('ug!')
    antwoord3=antwoord2.upper()[0]+antwoord2[1:]
    print(antwoord3)