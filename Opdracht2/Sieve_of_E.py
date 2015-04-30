import time
import sys

T1 = time.perf_counter()

def lijst(n):
    lijst1=list(range(2,n+1))
    for i in lijst1:
        for j in lijst1:
            if j%i == 0 and i != j:
                lijst1.remove(j)
    return lijst1

T2 = time.perf_counter()

n=int(sys.argv[1])

out=open(sys.argv[2], 'w')
for i in lijst(n):
    out.write(str(i)+'\n')
out.close()

aantal=len(lijst(n))

print('Found '+str(aantal)+' prime numbers smaller than '+str(n)+' in '+str(T2-T1)+' sec.')