import numpy as np

class sphere:
    color = (91, 93, 223) 
    radius = 1
    center = (0, -1, 5)

class light:
    pos = (-1, 3, 3)
    intensity = .8

#create some spheres
sphere0 = sphere()
sphere1 = sphere()
sphere2 = sphere()

sphere1.color = (225,238,238)
sphere1.radius = 1.5
sphere1.center = (1, 1, 6)

sphere2.color = (90,180,180)
sphere2.radius = 5000
sphere2.center = (5001, 0, 0)

spheres = [sphere0, sphere1]

#set canvas size and camera position
Cw = 800
Ch = 800
cam = (0, 0, 0)

#setup up ppm for writing
f = open("ray.ppm","w")
magic = "P3\n{} {}\n255\n".format(Cw,Ch)
f.write(magic)

#change of scale from world units to pixels
def CanvasToViewport(x, y):
    return(x*1/Cw, y*1/Ch, 1)

#function for sphere intersects
def IntersectSphere(O, D, sphere):
    r = sphere.radius
    #ray from center to origin, sub two tuples with map and lambda
    CO = tuple(map(lambda i, j: i - j, O, sphere.center))
    
    #set up quadratic
    a = np.dot(D,D)
    b = 2*np.dot(CO, D)
    c = np.dot(CO, CO) - r*r

    discrim = b*b - 4*a*c

    #make sure discriminant is real
    if discrim < 0:
        return 1000, 1000

    #solve quadratic and return both intersects
    t1 = (-b + np.sqrt(discrim))/(2*a)
    t2 = (-b - np.sqrt(discrim))/(2*a)
    return t1, t2

def TraceRay(O, D, t_min, t_max):

    #set closest intersect to t_max
    closest_t = 1000
    #default to no sphere
    closest_sphere = False
    #check intersects
    for i in spheres:
        t1, t2 = IntersectSphere(O, D, i)
    #if intersect is within bounds, set closest sphere
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = i
    #..
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = i

    #print debugging
    #print(closest_sphere, closest_t)
    #print(t1, t2, t_min, t_max)

    #if no sphere return background color
    if closest_sphere == False:
        #return (135, 206, 235)
        return (0, 0, 0)

    temp = (0,0,0)
    P = (O[0] + closest_t * D[0], O[1] + closest_t * D[1], O[2] + closest_t * D[2])
    N = tuple(map(lambda i, j: i - j, P, closest_sphere.center))
    N = N / np.sqrt(N[0]**2+N[1]**2+N[2]**2)
    temp = (closest_sphere.color[0] * ComputeLighting(P, N), closest_sphere.color[1] * ComputeLighting(P, N), closest_sphere.color[2] * ComputeLighting(P, N))
    return temp 

def ComputeLighting(P, N):
    i = 0.
    L = tuple(map(lambda i, j: i - j, light.pos, P))
    n_dot_l = np.dot(N, L)
    if n_dot_l > 0:
        i += light.intensity * n_dot_l/(np.sqrt(N[0]**2+N[1]**2+N[2]**2) * np.sqrt(L[0]**2+L[1]**2+L[2]**2))
    return i

#main func
for x in range(round(-Cw/2),round(Cw/2)):
    for y in range(round(-Ch/2),round(Ch/2)):
        D = CanvasToViewport(x, y)
        color = TraceRay(cam, D, 1, 1000)
        #write colors, index tuple
        f.write("{} {} {}".format(round(color[0]), round(color[1]), round(color[2])))
        f.write("   ")
    f.write("\n")

f.close()
