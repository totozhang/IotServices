from kamene.all import *
from kamene.layers.inet import IP, UDP

# IP Layer
# Actually it makes no sense to change the source ip addr, since there's NAT.
srcip = "11.11.111.111"
dstip = "47.95.194.185"
iplayer = IP(src=srcip, dst=dstip)

# UDP Layer
srcport = random.randint(1024, 65535)
dstport = [9999]
udplayer = UDP(sport=srcport, dport=dstport)

# APP Layer data
position = ["DL", "SY", "BJ", "SH", "TK"]
district = ["AA", "BB", "CC", "DD", "EE"]
identify = ["00", "01", "02", "03", "04"]
data_min = 10
data_max = 40

# Send 5 times
for i in range(0, 5):
    prefix = position[random.randint(0, len(position) - 1)] + \
             district[random.randint(0, len(district) - 1)] + \
             identify[random.randint(0, len(identify) - 1)]
    surfix = str(random.randint(data_min, data_max))
    message = prefix + ":" + surfix
    send(iplayer / udplayer / message)
