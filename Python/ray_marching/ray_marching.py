import math

#Constants
w = 800 #width
h = 800 #height
MAX_DIST = 1000
HIT_DIST = .01
MAX_STEP = 64

#test vectors
cam_pos = [0, 0, -5]
light_pos = [3, -5, 3]

class Sphere:
    radius = 2
    center = [0, 0, 4]

def sub_vec(vector1, vector2):
    vector3 = [0, 0, 0]
    for i in range(0,len(vector1)):
        vector3[i] = vector1[i] - vector2[i]
    return vector3

def add(vector1, vector2):
    vector3 = [0, 0, 0]
    for i in range(0,len(vector1)):
        vector3[i] = vector1[i] + vector2[i]
    return vector3

def dot(vector1, vector2):
    return sum(vector1_i * vector2_i for vector1_i, vector2_i in zip(vector1,vector2))

def mod(vector, scalar):
    return [i % scalar for i in vector]

def scaladd(vector, scalar):
    return [scalar + i for i in vector]

def scalmul(vector, scalar):
    return [scalar * i for i in vector]

def length(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def canvas_to_view(x, y):
    return [x/w, y/h, 1]

def Sphere_SDF(point, center, radius):
    Sphere_dist = length(sub_vec(point, center)) - radius
    return Sphere_dist

def mapper(point):
    disp = math.sin(2.0 * point[0]) * math.sin(3.0 * point[1]) * math.sin(2.0* point[2])*.3
    #disp = 0 
    rend = Sphere_SDF(point, Sphere.center, Sphere.radius)
    return (rend + disp) 

def calc_normal(point):
    epsilon = .001
    grad_x = mapper([point[0] + epsilon, 0, 0]) - mapper([point[0] - epsilon, 0, 0])
    grad_y = mapper([0, point[1] + epsilon, 0]) - mapper([0, point[1] - epsilon, 0])
    grad_z = mapper([0, 0, point[2] + epsilon]) - mapper([0, 0, point[2] - epsilon])
    normal = [grad_x, grad_y, grad_z]
    normal2 = [0, 0, 0]
    for x in range(0,len(normal)):
        normal2[x] = normal[x]/length(normal)
    return normal2 


def march(origin, direction):
    dist_traveled = 0
    current_pos = [0, 0, 0]

    for i in range(0,MAX_STEP):
        for j in range(0,3):
            current_pos[j] = origin[j] + dist_traveled * direction[j]
        dist_to_closest = mapper(current_pos)

        if dist_to_closest < HIT_DIST:
            normal = calc_normal(current_pos)

            light_dir = sub_vec(current_pos, light_pos)

            for y in range(0,3):
                light_dir[y] = light_dir[y]/length(light_dir)

            diffuse = max(0,dot(normal, light_dir))
            ret = [180, 15, 180]
            ret[0] = round(ret[0] * diffuse)
            ret[1] = round(ret[1] * diffuse)
            ret[2] = round(ret[2] * diffuse)

            return ret

        if dist_traveled > MAX_DIST:
            break
        dist_traveled += dist_to_closest

    return [0, 0, 0]

#test vector funcs
#print(length(vector1))
#print(sub(vector1, vector2))

#create and write data to ppm image
with open("march.ppm","w") as f:
    f.write("P3\n{} {}\n255\n".format(w,h))

    for x in range(round(-w/2), round(w/2)):
        for y in range(round(-h/2), round(h/2)):
            rd = canvas_to_view(x, y)
            color = march(cam_pos, rd)
            f.write("{} {} {}   ".format(color[0], color[1], color[2]))
        f.write("\n")
