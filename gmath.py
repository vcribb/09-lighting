import math
from display import *

  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect):

    color = [0, 0, 0]
    normalize(normal)
    normalize(view)
    normalize(light[0])

    amb = calculate_ambient(ambient, areflect)
    dif = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)

    for num in range(3):
        color[num] = amb[num] + dif[num] + spec[num]
    return limit_color(color)

def calculate_ambient(alight, areflect):
    color = [0, 0, 0]
    for num in range(3):
        color[num] = alight[num] * areflect[num]
    return limit_color(color)

def calculate_diffuse(light, dreflect, normal):
    color = [0, 0, 0]
    for num in range(3):
        color[num] = light[1][num] * dreflect[num] * dot_product(light[0], normal)
    return limit_color(color)

def calculate_specular(light, sreflect, view, normal):
    color = [0, 0, 0]
    obj = [0, 0, 0]
    temp = 2 * dot_product(light[0], normal)
    for num in range(3):
        obj[num] = normal[num] * temp - light[0][num]
    temp2 = (dot_product(obj, view))
    if temp2 < 0:
        temp2 = 0
    temp2 = pow(temp2, SPECULAR_EXP)
    for num in range(3):
        color[num] = light[1][num] * sreflect[num] * temp2
    return limit_color(color)

def limit_color(color):
    for num in range(3):
        color[num] = int(color[num])
        if color[num] < 0:
            color[num] = 0
        elif color[num] > 255:
            color[num] = 255
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude
    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
