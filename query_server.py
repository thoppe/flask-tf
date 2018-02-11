from flasktf import caller

model = caller()
print model('z', x=[1,2,3], y=[0,1,2])
# Returns {"z": 8.0}
