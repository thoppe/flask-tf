from flasktf import caller

model = caller()

# terms = M.info()
# print M.info(*terms)
output = model('z', x=[1, 2, 3], y=[0, 1, 2])
print output
print type(output)
print output['z']==8

