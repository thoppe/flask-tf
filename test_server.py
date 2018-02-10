from flasktf import caller

model = caller()

#terms = M.info()
#print M.info(*terms)
print model('z', x=[1,2,3], y=[0,1,2])
