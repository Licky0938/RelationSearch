from readxlsx import readxlsx as rxlx
from RelationSearch import relationship as rels
from RelationSearch import horizontal as hztl
from RelationSearch import vertical as vtcl
from RelationSearch import FORWARD, BACKWARD, HZTL, VTCL, ORDER, V_SORT

import time

sourcefile = "jobconnection.xlsx"
targetfile = "jobtarget.xlsx"


xl_source = rxlx(sourcefile)
xl_target = rxlx(targetfile)
s_tname = xl_target.get_targetset(1)

# dictionary[ownname] = [jobname0, jobname1, jobname2, ...]
d_forward = xl_source.get_link(1, 2)
# dictionary[ownname] = rels.relationship(ownname)
d_relship = {}

for key in d_forward:
    d_relship[key] = rels(key)

num = 1
mlen = len(d_forward)
time_begin = time.time()
for key in d_forward:
    time_s = time.time()
    hztl.link_horizon(d_relship[key], d_relship, d_forward)
    print("[System]", "time:", f"{time.time() - time_s: .3f}", "horizontal process:", num, "/", mlen, end='\r')
    num +=1
print("\n[System]", "Horizontal time:", f"{time.time() - time_begin: .3f}")

num = 1
mlen = len(d_relship)
time_begin = time.time()
for elmt in d_relship:
    time_s = time.time()
    vtcl.get_vertical(d_relship[elmt])
    print("[System]", "time:", f"{time.time() - time_s: .3f}", "vretical process:", num, "/", mlen, end='\r')
    num +=1
print("\n[System]", "Vertical time:", f"{time.time() - time_begin: .3f}")

with open("test.csv", mode="w") as f:
    for key in sorted(["XA", "XD"]):
        f.write(key + ',' + ','.join(sorted(d_relship[key].get_link(FORWARD,  ORDER)[V_SORT])) + '\n')
        f.write(      ',' + ','.join(sorted(d_relship[key].get_link(BACKWARD, ORDER)[V_SORT])) + '\n')
print("[System]", "test file is generated")

# set_extract = set(s_tname)
# print(s_tname)
# for key in set(d_relship.keys()) - set_extract:
#     if len(set(d_relship[key].get_link(FORWARD, HZTL).keys()) & s_tname) > 0:
#         set_extract.add(key)
#         print(key)