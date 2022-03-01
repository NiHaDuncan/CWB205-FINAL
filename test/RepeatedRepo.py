output2 = open('output2','r')
output3 = open('output3','r')
set2 = set()
set3 = set()
for line in output3:
    set3.add(line)
print('Output3 size = ', len(set3))
for line in output2:
    set3.discard(line)

print('Output3 new size = ', len(set3))

output3_uniq = open('output3_uniq','w')
for item in set3:
    output3_uniq.write(item)
