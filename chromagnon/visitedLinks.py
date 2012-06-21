import md5
import struct
import sys

f = open("/home/jrb/.config/chromium/Default/Visited Links", 'rB')
print "Magic: 0x%08x"%struct.unpack('I', f.read(4))[0]
print "Version: %d"%struct.unpack('I', f.read(4))[0]
length = struct.unpack('I', f.read(4))[0]
print "Length: %d"%length
print "Used Items: %d"%struct.unpack('I', f.read(4))[0]

salt = ""
for dummy in range(8):
    salt += struct.unpack('c', f.read(1))[0]

url = sys.argv[1]

fingerprint = md5.new()
fingerprint.update(salt)
fingerprint.update(url)
digest = fingerprint.hexdigest()

# Inverting the result
# Why Chrome MD5 computation gives a reverse digest ?
fingerprint = 0
for i in range(0, 16, 2):
    fingerprint += int(digest[i:i+2], 16) << (i/2)*8
key = fingerprint % length

# The hash table uses open addressing
# See chrome/common/visitedlink_common.* for details
f.seek(key*8 + 24, 0)
while True:
    finger = struct.unpack('L', f.read(8))[0]
#print "0x%08x: 0x%016x"%((f.tell()-24)/8-1, finger)
    if finger == 0:
        print "Not Found"
        break
    if finger == fingerprint:
        print "Found"
        break
    if f.tell() >= length*8 + 24:
        f.seek(24)
    if f.tell() == key*8 + 24:
        print "Not Found"
        break
f.close()
