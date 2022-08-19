class relationship:
    # initialization
    def __init__(self,myname:str) -> None:
        self.__myname = myname
        self.__link = {"forward": {}, "backward": {}}
    
    def __str__(self) -> str:
        return self.__myname  #, self.depth, self.__fname, 
    
    def add_link(self, direction: str, key: str, ins: object) -> None:
        self.__link[direction][key] = ins
    
    # get members
    def get_myname(self) -> str:
        return self.__myname
    
    def get_link(self, direction: str) -> dict:
        return self.__link[direction]
    
    def get_linkall(self) -> dict:
        return self.__link
    
    def get_linkkeys(self, direction: str) -> list:
        return self.__link[direction].keys()
    
    def get_waykeys(self) -> list:
        return self.__link.keys()

# counter = 0

class link:
    @classmethod
    def add_links(cls, forward: relationship, backward: relationship) -> None:
        forward.add_link("backward", backward.get_myname(), backward)
        backward.add_link("forward",  forward.get_myname(),  forward)


    def __get_elmtlength(self, direction: str, ins: relationship) -> int:
        return len(ins.get_link(direction))

    @classmethod
    def link_forward(cls, rel: relationship, d_link: dict, d_name: dict) -> None:
        for elmt in d_name[rel.get_myname()]:
            if elmt not in d_link:
                d_link[elmt] = relationship(elmt)
            cls.add_links(forward=d_link[elmt], backward=rel)
            # print("me:", rel.get_myname(), "for:", d_link[elmt].get_myname())
            if elmt not in d_name or len(d_name[elmt]) == cls.__get_elmtlength(cls, "forward", d_link[elmt]):
                continue
            else:
                cls.link_forward(d_link[elmt], d_link, d_name)

class search:
    # initialization
    def __init__(self) -> None:
        self.__hierarchy = {}
    
    def search_relation(self, direction: str, rel: relationship, mode: int = 1, depth: int = 0) -> None:
        d_link = rel.get_link(direction)
        for key in d_link.keys():
            if key in self.__hierarchy:
                if abs(self.__hierarchy[key]) * mode < abs(depth) * mode:
                    self.__hierarchy[key] = depth
                continue
            else:
                self.__hierarchy[key] = depth
            self.search_relation(direction, d_link[key], mode, depth + 1 if direction == "backward" else depth - 1)


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