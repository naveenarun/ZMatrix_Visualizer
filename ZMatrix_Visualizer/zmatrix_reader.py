

from visual import *
import math
import os

atoms = {}
names = {}
count = 0

def listfiles():
    filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
    zfiles = []
    for file_n in filenames:
        if file_n[-5:] == ".zmat":
            zfiles.append(file_n[:-5])
    return zfiles

zfiles = listfiles()
print "\nThese are the .zmat files in this directory:"
for i in range(len(zfiles)):
    print i+1,":",zfiles[i]

a = zfiles[input("Which file do you choose? ")-1] + ".zmat"
read = open(a)

labels_yn = raw_input("Do you want labels? (y/n): ")
if labels_yn == "y":
    labels_yn = True
else:
    labels_yn = False

scene = display(title=a)
scene.autoscale = True
scene.autocenter = True
    
def whichline(varname):
    dummy = open(a)
    count = 0
    for line in dummy:
        count += 1
        if line.split()[0] == varname:
            return str(count)

def findme(name):
    dummy = open(a)
    switch = 0
    for line in dummy:
        if line.strip()[0] == "V":
            switch = 1
        if name in line and switch == 1:
            try:
                return line.split("=")[1].strip()                
            except IndexError:
                process = line.split()
                return process[len(process)-1].strip()

def connect(atoms, i_1, i_2):
    arrow = vector(atoms[i_2][1])-vector(atoms[i_1][1])
    print "here: ", vector
    return cylinder(pos=(vector(atoms[i_1][1])), axis=(arrow), radius=0.1)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def replace(line):
    for i in range(1,len(line)):
        if not is_number(line[i]):
            isneg = False    #check if it's negative
            if line[i][0] == "-":
                isneg = True
                line[i] = line[i][1:]
            if i % 2 == 0:
                line[i] = findme(line[i])
            else:
                line[i] = whichline(line[i])
            if isneg == True:
                line[i] = "-" + line[i]
            if line[i][0:2] == "--":
                line[i] = line[i][2:]
    return line

def process_name(name):
    if name.isalpha():
        return name
    else:
        construct = name[0]
        if name[1].isalpha():
            construct += name[1]
        return construct

for line in read:
    if line.strip() == "":
        continue
    dissect = line.split()
    try:
        if dissect[0][0] == "V":
            break
    except IndexError:
            pass
    dissect = replace(dissect)
    count+=1
    i = str(count)
    names[i] = process_name(dissect[0])
    if len(dissect) == 1:
        atoms[i] = (0.0,0.0,0.0)
    elif len(dissect) == 3:
        atoms[i] = (atoms[dissect[1]][0], atoms[dissect[1]][1], atoms[dissect[1]][2] + float(dissect[2]))
    elif len(dissect) == 5:
        other = dissect[3]
        center = dissect[1]
        otherside = vector(atoms[other]) - vector(atoms[center])
        sidelength = float(dissect[2])
        rotateme = norm(otherside) * sidelength
        rot_angle = math.radians(float(dissect[4]))
        pivot = (0.,1.,0.)
        
        new = rotate(rotateme, rot_angle, pivot)
        new = vector(atoms[center]) + new
        atoms[i] = tuple(new)
    else:
        other = dissect[3]
        center = dissect[1]
        third = dissect[5]
        otherside = vector(atoms[other]) - vector(atoms[center])
        secondside = vector(atoms[third])- vector(atoms[other])
        sidelength = float(dissect[2])
        rotateme = norm(otherside) * sidelength
        rot_angle = math.radians(float(dissect[4]))
        di_angle = -math.radians(float(dissect[6]))
        pivot = cross(otherside,secondside)      

        new = rotate(rotateme, rot_angle, pivot)
        new = rotate(new, di_angle, otherside)
        new = vector(atoms[center]) + new
        atoms[i] = tuple(new)
#    if len(dissect)>1:
#        rod = connect(atoms, dissect[1], i)

print "\n\n"

#xaxis = arrow(pos=(0.,0.,0.), axis=(0.4,0.,0.), opacity=0.6, shaftwidth=0.02, color=color.red)
#yaxis = arrow(pos=(0.,0.,0.), axis=(0.,0.4,0.), opacity=0.6, shaftwidth=0.02, color=color.green)
#zaxis = arrow(pos=(0.,0.,0.), axis=(0.,0.,0.4), opacity=0.6, shaftwidth=0.02, color=color.blue)

def draw(key, atoms, names):
    radii = {"h":(0.37, color.red),
             "o":(0.66, color.blue),
             "c":(0.77, color.yellow),
             "f":(0.64, color.green),
             "n":(0.70, color.magenta)}
    name = names[key].lower()
    if name in radii.keys():
        return sphere(pos=atoms[key], color=radii[name][1], radius = radii[name][0])
    else:
        return sphere(pos=atoms[key], color=color.white, radius = 0.5)

for i in range(len(atoms.keys())):
    key = str(i+1)
    if key == "1":
        colors = color.blue
    else:
        colors = color.red
    print names[key], ":", atoms[key]
    ball = draw(key, atoms, names)
    if labels_yn == True:
        label(pos=atoms[key], text=names[key])
