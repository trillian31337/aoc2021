import sys
import re

class cuboid():
	def __init__(self,state,x1,x2,y1,y2,z1,z2):
		self.state = state
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.z1 = z1
		self.z2 = z2
		self.count = len(range(x1,x2+1))*len(range(y1,y2+1))*len(range(z1,z2+1))

# count number of on cubes in list of nonoverlapping cuboids
def count_on(cuboidlist):
	count = 0 
	for c in cuboidlist:	
		if c.state == 'on':
			count += c.count
	return count

def count_on_initregion(cuboidlist,initregion):
	count = 0 
	for c in cuboidlist:	
		coverlap = overlap(c,initregion)
		if coverlap != None:
			count += coverlap.count
	return count
	

# combine a new cuboid with the list of previous cuboids to create a list of non-overlapping on cuboids
def combine(cuboids,ncuboid):
	newcuboids = []
	for c in cuboids:
		clist = splitcuboid(c,ncuboid)
		newcuboids.extend(clist)
	# add the new cuboid to the list if it is an on cuboid
	# don't add the second cuboid if it is an off cuboid
	if  ncuboid.state == 'on':
		newcuboids.append(ncuboid)
	return newcuboids	

# split the first cuboid into non-overlapping cuboids (with the second cuboid)
def splitcuboid(cuboid1,cuboid2):

	cuboid3 = overlap(cuboid1,cuboid2)
	# nonoverlapping, return the first cuboid unmodified
	if cuboid3 == None:
		return [cuboid1]
	
	newcuboids = []
	# handles two cases:
	# 1. overlap two on cuboids
	# 2. overlap an on cuboid with an off cuboid
	# for both cases: split the first cuboid into non-overlapping cuboids
	splitx1 = max(cuboid1.x1,cuboid3.x1)
	splitx2 = min(cuboid1.x2,cuboid3.x2)
	splity1 = max(cuboid1.y1,cuboid3.y1)
	splity2 = min(cuboid1.y2,cuboid3.y2)
	splitz1 = max(cuboid1.z1,cuboid3.z1)
	splitz2 = min(cuboid1.z2,cuboid3.z2)
	# there can be one or two ranges for new cuboids in each dimension (up to 6 new cuboids)
	if cuboid1.x1 != splitx1:
		# new cuboid, slice in beginning of x range
		newcuboids.append(cuboid(cuboid1.state,cuboid1.x1,splitx1-1,cuboid1.y1,cuboid1.y2,cuboid1.z1,cuboid1.z2))
	if cuboid1.x2 != splitx2:
		# new cuboid, slice in end of x range
		newcuboids.append(cuboid(cuboid1.state,splitx2+1,cuboid1.x2,cuboid1.y1,cuboid1.y2,cuboid1.z1,cuboid1.z2))
	if cuboid1.y1 != splity1:
		# new cuboid, slice in beginning of y range
		newcuboids.append(cuboid(cuboid1.state,splitx1,splitx2,cuboid1.y1,splity1-1,cuboid1.z1,cuboid1.z2))
	if cuboid1.y2 != splity2:
		# new cuboid, slice in end of y range
		newcuboids.append(cuboid(cuboid1.state,splitx1,splitx2,splity2+1,cuboid1.y2,cuboid1.z1,cuboid1.z2))
	if cuboid1.z1 != splitz1:
		# new cuboid, slice in beginning of z range
		newcuboids.append(cuboid(cuboid1.state,splitx1,splitx2,splity1,splity2,cuboid1.z1,splitz1-1))
	if cuboid1.z2 != splitz2:
		# new cuboid, slice in beginning of z range
		newcuboids.append(cuboid(cuboid1.state,splitx1,splitx2,splity1,splity2,splitz2+1,cuboid1.z2))
	#print("New non-overlapping cuboids:")
	#for c in newcuboids:
	#	prettyprint_cuboid(c)

	return newcuboids

def overlap(cuboid1,cuboid2):
	# part of xrange matching, part of yrange matching part of zrange matching
	if cuboid1.state == 'off' or cuboid2.state == 'off':
		state = 'off'
	else:
		state = 'on'
	x1 = max(cuboid1.x1,cuboid2.x1)
	x2 = min(cuboid1.x2,cuboid2.x2)
	y1 = max(cuboid1.y1,cuboid2.y1)
	y2 = min(cuboid1.y2,cuboid2.y2)
	z1 = max(cuboid1.z1,cuboid2.z1)
	z2 = min(cuboid1.z2,cuboid2.z2)

	# if any of the ranges does not contain any values -> no overlap
	if x1 > x2 or y1 > y2 or z1 > z2:
		return None

	cuboid3 = cuboid(state,x1,x2,y1,y2,z1,z2)
	return cuboid3


def prettyprint_cuboid(cuboid):
	print("Cube:", cuboid.state)
	print(cuboid.x1,"..",cuboid.x2,",",cuboid.y1,"..",cuboid.y2,",",cuboid.z1,"..",cuboid.z2)
	print()

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
elif len(sys.argv) > 1 and sys.argv[1] == "test2":
	fname = 'input_test2'
elif len(sys.argv) > 1 and sys.argv[1] == "test3":
	fname = 'input_test3'
else:
   fname = 'input'

initregion = cuboid('off',-50,50,-50,50,-50,50)

f = open(fname)
pattern = re.compile(r'(on|off) x=(-*\d+)\.\.(-*\d+),y=(-*\d+)\.\.(-*\d+),z=(-*\d+)\.\.(-*\d+)')
cuboids = []
for i,line in enumerate(f):
	m = pattern.match(line)
	if m == None:
		print("Not matching")
	cuboids.append(cuboid(m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)),int(m.group(7))))

newcuboids = [cuboids[0]]
for i,c in enumerate(cuboids):
	newcuboids = combine(newcuboids,c)

count = count_on(newcuboids)
print("Total count after",i+1,"reboot instructions", count)

countinit = count_on_initregion(newcuboids,initregion)
print("Count of on cubes in init region:",countinit)



