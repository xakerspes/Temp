y1=2020
y2=2020
m1=1
m2=3
M=[]
for i in range(y1*12+m1,y2*12+1+m2):
    if i%12==0: year = i // 12;  month = 12
    else:       year = i // 12;  month = i % 12
    print('{}/{:02d}'.format(year,month))
    z=b[b.str.contains('{}/{:02d}'.format(year,month))]
    if len(z): M.append(z)
