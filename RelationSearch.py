class relationship:
    # initialization
    def __init__(self,myname:str) -> None:
        self.__myname = myname
        self.__forward  = {}    # name:instance dictionary
        self.__backward = {}    # name:instance dictionary
    
    def __str__(self) -> str:
        return self.__myname  #, self.depth, self.__fname, 
    
    # add instance
    def add_forward(self, key: str, ins: object) -> None:
        if key not in self.__forward:
            self.__forward[key] = ins
    
    def add_backward(self, key:str, ins: object) -> None:
        if key not in self.__backward:
            self.__backward[key] = ins
    
    # get members
    def get_myname(self) -> str:
        return self.__myname

    def get_forward(self) -> dict:
        return self.__forward
    
    def get_backward(self) -> dict:
        return self.__backward
    
    def get_forkeys(self) -> list:
        return self.__forward.keys()
    
    def get_backkeys(self) -> list:
        return self.__backward.keys()

# counter = 0

def add_links(forward: relationship, backward: relationship) -> None:
    forward.add_backward(backward.get_myname(), backward)
    backward.add_forward(forward.get_myname(), forward)

def get_flength(ins: relationship) -> int:
    return len(ins.get_forkeys())

def link_forward(rel: relationship, d_link: dict, d_name: dict) -> None:
    # global counter
    for elmt in d_name[rel.get_myname()]:
        # counter += 1
        if elmt not in d_link:
            # print("in not")
            d_link[elmt] = relationship(elmt)
        add_links(forward=d_link[elmt], backward=rel)
        # print("me:", rel.get_myname(), "for:", d_link[elmt].get_myname())
        if elmt not in d_name or len(d_name[elmt]) == get_flength(d_link[elmt]):
            # print("already exist")
            continue
        else:
            link_forward(d_link[elmt], d_link, d_name)

            
        

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