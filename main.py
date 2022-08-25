from readxlsx import readxlsx as rxlx
from RelationSearch import relationship as rels
from RelationSearch import horizon as hrzn
from RelationSearch import vertical as vtcl
from RelationSearch import FORWARD, BACKWARD, HORI, VERT, ORDER, V_SORT

sourcefile = "jobconnection.xlsx"
targetfile = "jobtarget.xlsx"


s_xlx = rxlx(sourcefile, 0)
t_xlx = rxlx(targetfile, 0)
t_lst = t_xlx.get_targetset(1)

# dictionary[ownname] = [jobname0, jobname1, jobname2, ...]
dict_link = s_xlx.get_link(1, 2)
# dictionary[ownname] = rels.relationship(ownname)
dict_master = {}

for key in dict_link:
    dict_master[key] = rels(key)

for key in dict_link:
    hrzn.link_horizon(dict_master[key], dict_master, dict_link)

for elmt in dict_master:
    vtcl.get_vertical(dict_master[elmt])

with open("test.csv", mode="w") as f:
    for key in dict_master:
        f.write(key + ',' + ','.join(dict_master[key].get_link(FORWARD,  ORDER)[V_SORT]) + '\n')
        f.write(      ',' + ','.join(dict_master[key].get_link(BACKWARD, ORDER)[V_SORT]) + '\n')

set_extract = set(dict_master.keys()) - t_lst