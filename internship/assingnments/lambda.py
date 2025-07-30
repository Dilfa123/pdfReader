add=lambda x,y:x+y
print("sum=",add(4,3))
mul=lambda  a,b:a*b
print("multiplication=",mul(4,3))
power=lambda x,y=2:x**y
print("square=",power(3))
avg=lambda *nums:sum(nums)/len(nums)
print("avg=",avg(4,3))
greet=lambda who="guest":f"hi,{who}"
print(greet())
