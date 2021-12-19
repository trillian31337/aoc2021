from termcolor import colored
import re
import sys
import numpy as np
from copy import deepcopy

class BITSpacket():
	def __init__(self,version, typeid, lentype, length):
		self.version = version
		self.typeid = typeid
		self.lentype = lentype
		self.length = length
		self.subpackets = []

	def append_sub(self,packet):
		self.subpackets.append(packet)

def subpackets_val(data):
	valdata = data
	vallist = []
	vallen = 0
	end = False
	while valdata[0] == '1':
		vallist.extend(valdata[1:5])
		valdata = valdata[5:]
		vallen += 5
	# add last value which starts with bit 0
	vallist.extend(valdata[1:5])
	vallen += 5
	val = int(''.join(vallist),2)
	return val,vallen

def subpackets_op(data,lentype,length):
	subpackets = []
	spdata = data
	totsplen = 0
	if lentype == 0:
		splen = length
		while len(spdata) >= 8: 
			packet, packet_length = decode_packet(spdata)
			subpackets.append(packet)
			splen -= packet_length
			spdata = spdata[packet_length:]
		totsplen = length
	else: # lentype == 1
		for i in range(length):
			packet, packet_length = decode_packet(spdata)
			subpackets.append(packet)
			spdata = spdata[packet_length:]
			totsplen += packet_length
	return subpackets, totsplen

# decode one packet
# return packet, packet_length
def decode_packet(data):
	version = int(''.join(data[0:3]),2)
	typeid = int(''.join(data[3:6]),2)
	if typeid != 4:
		lentype = int(''.join(data[6]),2)
	else:
		lentype = -1
	if lentype == 0:
		# 15 bits length, number of bits of subpackets
		length = int(''.join(data[7:22]),2)
	elif lentype == 1:
		# 11 bit length, number of subpackets
		length = int(''.join(data[7:18]),2)
	else:
		length = -1
	packet = BITSpacket(version,typeid,lentype,length)
	print("#########################################")
	print("BITS packet header:")
	print("packet version:",version)
	print("packet type:",typeid)
	print("subpacket lentype:",lentype)
	print("subpacket length:",length)
	if typeid == 4:
		# literal value
		headerlen = 6
		val,length = subpackets_val(data[headerlen:])
		packet.append_sub(val)
	else:
		if lentype == 0:
			headerlen = 22
			subpackets,length = subpackets_op(data[headerlen:headerlen+length],lentype,length)
		elif lentype == 1:
			headerlen = 18
			subpackets,length = subpackets_op(data[headerlen:],lentype,length)
		for sp in subpackets:
			packet.append_sub(sp)
	# calculate packet length
	packet_length = headerlen + length
	
	data = data[packet_length:]

	return packet, packet_length

def version_sum_packet(packet):
	if packet.typeid == 4:
		return packet.version
	else:
		vsum = packet.version
		for sp in packet.subpackets:
			vsum += version_sum_packet(sp)
		return vsum

def version_sum(packets):
	vsum = 0
	for packet in packets:
		vsum += version_sum_packet(packet)
	return vsum

def evaluate_packet(packet):
	if packet.typeid == 4: # literal value
		return packet.subpackets[0]
	elif packet.typeid == 0: # sum
		result = 0
		for sp in packet.subpackets:
			result += evaluate_packet(sp)
	elif packet.typeid == 1: # product
		result = 1
		for sp in packet.subpackets:
			result *= evaluate_packet(sp)
	elif packet.typeid == 2: # minimum
		result = sys.maxsize
		for sp in packet.subpackets:
			result = min(result,evaluate_packet(sp))
	elif packet.typeid == 3: # maximum
		result = 0
		for sp in packet.subpackets:
			result = max(result,evaluate_packet(sp))
	elif packet.typeid == 5: # greater than
		result = (evaluate_packet(packet.subpackets[0])) > (evaluate_packet(packet.subpackets[1]))
		if result == True:
			return 1
		else:
			return 0
	elif packet.typeid == 6: # less than
		result = (evaluate_packet(packet.subpackets[0])) < (evaluate_packet(packet.subpackets[1]))
		if result == True:
			return 1
		else:
			return 0
	elif packet.typeid == 7: # less than
		result = (evaluate_packet(packet.subpackets[0])) == (evaluate_packet(packet.subpackets[1]))
		if result == True:
			return 1
		else:
			return 0
	return result
	

def evaluate(packets):
	result = 0
	for packet in packets:
		result += evaluate_packet(packet)
	return result


### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)
for line in f:
	packets = []
	print("########################################################################")
	print("New transmission:",line.rstrip())
	h_size = len(line.rstrip()) * 4
	bindata = (bin(int(line.rstrip(), 16))[2:] ).zfill(h_size)
	transmissionlen = len(bindata)
	while transmissionlen >= 8:
		packet, packet_length = decode_packet(bindata)
		packets.append(packet)
		transmissionlen -= packet_length
		bindata = bindata[packet_length:]
	versum = version_sum(packets)
	print()
	print("Version sum of all packets:",versum)
	result = evaluate(packets)
	print()
	print("Value of evaluated transmission:",result)
