import time
import sys

T1 = time.perf_counter()

def lijst(n):
    lijst1=list(range(0,n))
    lijst1[1]=0
    for i in range(1,n):
        if lijst1[i] != 0:
            for j in range(2*i,n,i):
                lijst1[j]=0
    return lijst1

T2 = time.perf_counter()

n=int(sys.argv[1])

out=open(sys.argv[2], 'w')
a=[]
for i in lijst(n):
    if i != 0:
        out.write(str(i)+'\n')
        a.append(i)
out.close()

aantal=len(a)

print('Found '+str(aantal)+' prime numbers smaller than '+str(n)+' in '+str(T2-T1)+' sec.')