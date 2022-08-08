from readxlsx import readxlsx as rxlx
import RelationSearch as rels

sourcefile = "jobconnection.xlsx"
targetfile = "jobtarget.xlsx"

t_xlx = rxlx(targetfile, "Sheet1")
s_xlx = rxlx(sourcefile, "Sheet1")
t_lst = t_xlx.get_targetlist(1)

dict_link = s_xlx.get_link(1, 2, t_lst)
dict_master = {}

for key in dict_link:
    dict_master[key] = rels.relationship(key)
    # print(key)
a = dict_master["I"]
a.add_link("forward", "J", dict_master["J"])

# for key in sorted(dict_link.keys()):
#     rels.link_forward(dict_master[key], dict_master, dict_link)

# set_other = set(dict_master.keys()) - set(t_lst)
# for key in dict_master:
#     d = {}
#     rels.get_flink(dict_master[key], d, -1)
#     print(dict_master[key], d)

# for key in sorted(dict_master.keys()):
#     print(dict_master[key].get_myname(), list(dict_master[key].get_forkeys()), list(dict_master[key].get_backkeys()))
