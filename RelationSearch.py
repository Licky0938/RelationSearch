from inspect import getfile
from turtle import back


class relationship:
    # initialization
    def __init__(self,myname:str) -> None:
        self.__myname = myname
        self.__forward  = {}    # name:instance dictionary
        self.__backward = {}    # name:instance dictionary
        self.__link = {"forward": {}, "backward": {}}
    
    def __str__(self) -> str:
        return self.__myname  #, self.depth, self.__fname, 
    
    # add instance
    def add_forward(self, key: str, ins: object) -> None:
        if key not in self.__forward:
            self.__forward[key] = ins
    
    def add_backward(self, key:str, ins: object) -> None:
        if key not in self.__backward:
            self.__backward[key] = ins
    
    def add_link(self, direction: str, key: str, ins: object) -> None:
        self.__link[direction][key] = ins
    
    # get members
    def get_myname(self) -> str:
        return self.__myname

    def get_forward(self) -> dict:
        return self.__forward
    
    def get_backward(self) -> dict:
        return self.__backward
    
    def get_link(self, direction: str) -> dict:
        return self.__link[direction]
    
    def get_linkall(self) -> dict:
        return self.__link

    def get_forkeys(self) -> list:
        return self.__forward.keys()
    
    def get_backkeys(self) -> list:
        return self.__backward.keys()
    
    def get_keys(self, direction: str) -> list:
        return self.__link[direction].keys()
    
    def get_waykeys(self) -> list:
        return self.__link.keys()

# counter = 0

def add_links(forward: relationship, backward: relationship) -> None:
#     forward.add_backward(backward.get_myname(), backward)
#     backward.add_forward(forward.get_myname(), forward)
    forward.add_link("backward", backward.get_myname(), backward)
    backward.add_link("forward",  forward.get_myname(),  forward)

def get_flength(ins: relationship) -> int:
    return len(ins.get_forkeys())

def get_elmtlength(direction: str, ins: relationship) -> int:
    return len(ins.get_link(direction))

def link_forward(rel: relationship, d_link: dict, d_name: dict) -> None:
    for elmt in d_name[rel.get_myname()]:
        if elmt not in d_link:
            d_link[elmt] = relationship(elmt)
        add_links(forward=d_link[elmt], backward=rel)
        # print("me:", rel.get_myname(), "for:", d_link[elmt].get_myname())
        if elmt not in d_name or len(d_name[elmt]) == get_elmtlength("forward", d_link[elmt]):
            continue
        else:
            link_forward(d_link[elmt], d_link, d_name)

def get_flink(rel: relationship, d_depth: dict, depth: int) -> None:
    d_fwd = rel.get_forward()
    for key in d_fwd.keys():
        if key in d_depth:
            if d_depth[key] > depth:
                d_depth[key] = depth
        else:
            d_depth[key] = depth
        get_flink(d_fwd[key], d_depth, depth - 1)

def get_relation(direction: str, rel: relationship, d_depth: dict, depth: int, mode: int = 1) -> None:
    d_link = rel.get_link(direction)
    for key in d_link.keys():
        if key in d_depth:
            if abs(d_depth[key]) * mode < abs(depth) * mode:
                d_depth[key] = depth
            continue
        else:
            d_depth[key] = depth
        get_relation(direction, d_link[key], d_depth, depth, mode)

if __name__ == "__main__":
    from readxlsx import readxlsx
    FILENAME = "jobconnection.xlsx"
    linkval = readxlsx(FILENAME, "Sheet1")
    dict_link = linkval.get_link(s_col=1, e_col=2)
    dict_master = {}
    for key in dict_link.keys():
        dict_master[key] = relationship(key)

    for key in sorted(dict_link.keys(), reverse=True):
        # counter = 0
        link_forward(dict_master[key], dict_master, dict_link)
        print("[System]", key, "linked")

    for key in sorted(dict_master.keys()):
        print(dict_master[key].get_myname(), list(dict_master[key].get_forkeys()), list(dict_master[key].get_backkeys()))