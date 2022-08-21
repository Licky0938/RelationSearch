from readxlsx import readxlsx as rxlx
from RelationSearch import relationship as rels
from RelationSearch import link
from RelationSearch import search as srch

sourcefile = "jobconnection.xlsx"
targetfile = "jobtarget.xlsx"


s_xlx = rxlx(sourcefile, 0)
t_xlx = rxlx(targetfile, 0)
t_lst = t_xlx.get_targetlist(1)

# dictionary[ownname] = [jobname0, jobname1, jobname2, ...]
dict_link = s_xlx.get_link(1, 2, t_lst)
# dictionary[ownname] = rels.relationship(ownname)
dict_master = {}

for key in dict_link:
    dict_master[key] = rels(key)

for key in dict_link.keys():
    link.link_forward(dict_master[key], dict_master, dict_link)

# for key in sorted(dict_master.keys()):
#     link = dict_master[key].get_linkall()
#     if key in dict_link:
#         print("[origin]", key, set(dict_link[key]))
#     print("[relation]", key, set(link["forward"].keys()), set(link["backward"].keys()))

dict_order = {}
for elmt in dict_master:
    print(elmt)
    dict_order[elmt] = srch.get_relation(dict_master[elmt])

for elmt in sorted(dict_order):
    print(elmt)
    for key in dict_order[elmt]:
        print(key, dict_order[elmt][key])
        break
    break

# set_other = set(dict_master.keys()) - set(t_lst)
# for key in dict_master:
#     d = {}
#     rels.get_flink(dict_master[key], d, -1)
#     print(dict_master[key], d)

# for key in sorted(dict_master.keys()):
#     print(dict_master[key].get_myname(), list(dict_master[key].get_forkeys()), list(dict_master[key].get_backkeys()))
