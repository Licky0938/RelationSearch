FORWARD = "forward"
BACKWARD = "backward"

class relationship:
    # initialization
    def __init__(self,myname:str) -> None:
        self.__myname = myname
        self.__link = {FORWARD: {}, BACKWARD: {}}
    
    def __str__(self) -> str:
        txt  = "type: " + self.__class__.__name__ + '\n'
        txt += "myname: " + self.__myname + '\n'
        for key in [FORWARD, BACKWARD]:
            if any(self.__link[key]):
                txt += key + ": " + ", ".join(self.get_linkkeys(key)) + '\n'

        return txt
    
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
        forward.add_link(BACKWARD, backward.get_myname(), backward)
        backward.add_link(FORWARD,  forward.get_myname(),  forward)


    def __get_elmtlength(self, direction: str, ins: relationship) -> int:
        return len(ins.get_link(direction))

    @classmethod
    def link_forward(cls, rel: relationship, d_link: dict, d_name: dict) -> None:
        for elmt in d_name[rel.get_myname()]:
            if elmt not in d_link:
                d_link[elmt] = relationship(elmt)
            cls.add_links(forward=d_link[elmt], backward=rel)
            # print("me:", rel.get_myname(), "for:", d_link[elmt].get_myname())
            if elmt not in d_name or len(d_name[elmt]) == cls.__get_elmtlength(cls, FORWARD, d_link[elmt]):
                continue
            else:
                cls.link_forward(d_link[elmt], d_link, d_name)

class search:
    # initialization
    def __init__(self) -> None:
        self.__hierarchy = {}
    
    @classmethod
    def search_relation(cls, rel: relationship, d_result:dict, direction: str, increment: int, mode: int = 1, depth: int = 0) -> None:
        name = rel.get_myname()
        if name in d_result:
            if abs(d_result[name]) * mode < abs(depth) * mode:
                d_result[name] = depth
        else:
            d_result[name] = depth
            d_link = rel.get_link(direction)
            for key in d_link.keys():
                cls.search_relation(d_link[key], d_result, direction, increment, mode, depth + increment)

    @classmethod
    def sort_depth(cls, rel: relationship, d_target: dict) -> list:
        ordered = sorted(d_target.items(), key=lambda i: i[1])
        for i in range(len(ordered)):
            ordered[i] = ordered[i][0]
        print(ordered)

    @classmethod
    def get_relation(cls, rel: relationship, mode: int = -1, depth: int = 0) -> dict:
        d_result = {FORWARD: {}, BACKWARD: {}}
        cls.search_relation(rel, d_result[FORWARD], FORWARD, -1, mode, depth)
        cls.search_relation(rel, d_result[BACKWARD], BACKWARD, 1, mode, depth)
        cls.sort_depth(rel, d_result[FORWARD])
        # cls.sort_depth(rel, d_result[BACKWARD])
        return d_result

if __name__ == "__main__":
    from readxlsx import readxlsx
    # FILENAME = "jobconnection.xlsx"
    # linkval = readxlsx(FILENAME, "Sheet1")
    # dict_link = linkval.get_link(s_col=1, e_col=2)
    # dict_master = {}
    # for key in dict_link.keys():
    #     dict_master[key] = relationship(key)

    # for key in sorted(dict_link.keys(), reverse=True):
    #     # counter = 0
    #     link_forward(dict_master[key], dict_master, dict_link)
    #     print("[System]", key, "linked")

    # for key in sorted(dict_master.keys()):
    #     print(dict_master[key].get_myname(), list(dict_master[key].get_forkeys()), list(dict_master[key].get_backkeys()))