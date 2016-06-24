from itertools import izip


with open('./IP', 'r') as IP, \
    open('./Port', 'r') as Port, \
    open('./Type', 'r') as Type, \
    open('./ip_pools.txt', 'a') as ip_pools:
        for line1, line2, line3 in izip(IP, Port, Type):
            key = line3.strip().lower()
            if key.startswith('http'):
                value = line3.strip().lower() + '://' \
                        + line1.strip() + ':' + line2.strip()

                format_url = {key:value}
                ip_pools.write(str(format_url) + '\n')
