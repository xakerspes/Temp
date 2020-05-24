with open('file.txt') as file:
    f=file.read()
links =np.genfromtxt('file.txt',dtype='str')

a=np.array(re.findall(r'\/\d+',f)).reshape(-1,3)
b=np.char.add(a[:,0], a[:,1])
c=np.char.add(b,a[:,2])
d=np.char.replace(c, '/', '')

start  = '200801010044'
                        
end    = '200801010136'
start = int(start[:6] +  start[4:6] + start[6:]) 
end   = int(  end[:6] +    end[4:6] +   end[6:])
int(d[0])
for i,j in enumerate(d):
    if  start <= int(d[i]) <= end:
        print(d[i],i)
        print(links[i])
