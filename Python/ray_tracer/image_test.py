f = open("image.ppm","w")
x = 800 
y = 600 
z = 255
magic_string = "P3\n{} {}\n255\n".format(x,y) 
f.write(magic_string)
for i in range(0,x):
    for j in range(0,y):
        f.write("{:0>3} {:0>3} {:0>3}".format(round(j*(255/600)),round(i*(255/600)),z))
        f.write("   ")
    f.write("\n")
f.close()
