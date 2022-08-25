FORWARD = "forward"
BACKWARD = "backward"
HORI = "horizon"
VERT = "vertical"
ORDER = "order"
V_SORT = "v_sort"

class relationship:
    __DIRECTION = [FORWARD, BACKWARD]
    __ELEMENTS  = [HORI, VERT, ORDER]

    # initialization
    def __init__(self,myname:str) -> None:
        self.__myname = myname
        self.__link = {}
        for direction in self.__DIRECTION:
            self.__link[direction] = {}
            for element in self.__ELEMENTS:
                self.__link[direction][element] = {}
    
    def __str__(self) -> str:
        txt  = "type: " + self.__class__.__name__ + '\n'
        txt += "myname: " + self.__myname + '\n'
        for direction in self.__DIRECTION:
            txt += direction + '\n'
            for element in self.__ELEMENTS:
                if any(self.__link[direction][element]):
                    txt += element + ": " + ", ".join(self.get_linkkeys(element)) + '\n'

        return txt

    # add elements
    def add_link(self, direction: str, element: str, key: str, item) -> None:
        self.__link[direction][element][key] = item
    
    # get members
    def get_myname(self) -> str:
        return self.__myname
    
    def get_link(self, direction: str = None, element: str = None) -> dict:
        if direction is None:
            return self.__link
        elif element is None:
            return self.__link[direction]
        else:
            return self.__link[direction][element]
    
    def get_linkall(self) -> dict:
        return self.__link
    
    def get_linkkeys(self, direction: str) -> list:
        return self.__link[direction].keys()
    
    def get_waykeys(self) -> list:
        return self.__link.keys()

# counter = 0

class horizon:
    @classmethod
    def add_horizon(cls, forward: relationship, backward: relationship) -> None:
        forward.add_link(BACKWARD, HORI, backward.get_myname(), backward)
        backward.add_link(FORWARD, HORI,  forward.get_myname(),  forward)


    def __get_elmtlength(self, direction: str, ins: relationship) -> int:
        return len(ins.get_link(direction, HORI))

    @classmethod
    def link_horizon(cls, rel: relationship, d_link: dict, d_name: dict) -> None:
        for elmt in d_name[rel.get_myname()]:
            if elmt not in d_link:
                d_link[elmt] = relationship(elmt)
            cls.add_horizon(forward=d_link[elmt], backward=rel)
            if elmt not in d_name or len(d_name[elmt]) == cls.__get_elmtlength(cls, FORWARD, d_link[elmt]):
                continue
            else:
                cls.link_horizon(d_link[elmt], d_link, d_name)

class vertical:
    @classmethod
    def search_vertical(cls, rel: relationship, d_vertical:dict, direction: str, increment: int, mode: int = 1, depth: int = 0) -> None:
        d_link = rel.get_link(direction, HORI)
        for key in d_link:
            if key in d_vertical:
                if abs(d_vertical[key]) * mode < abs(depth) * mode:
                    d_vertical[key] = depth
                continue
            else:
                d_vertical[key] = depth
            cls.search_vertical(d_link[key], d_vertical, direction, increment, mode, depth + increment)

    @classmethod
    def sort_vertical(cls, rel: relationship, d_target: dict, direction: str, desc: bool = False) -> None:
        ordered = sorted(d_target.items(), key=lambda i: i[1], reverse=desc)
        for i in range(len(ordered)):
            ordered[i] = ordered[i][0]
        rel.add_link(direction, ORDER, V_SORT, ordered)

    @classmethod
    def get_vertical(cls, rel: relationship, mode: int = -1, depth: int = 0) -> None:
        cls.search_vertical(rel, rel.get_link(FORWARD, VERT), FORWARD, -1, mode, depth - 1)
        cls.search_vertical(rel, rel.get_link(BACKWARD, VERT), BACKWARD, 1, mode, depth + 1)
        cls.sort_vertical(rel, rel.get_link(FORWARD, VERT), FORWARD, desc=True)
        cls.sort_vertical(rel, rel.get_link(BACKWARD, VERT), BACKWARD)

if __name__ == "__main__":
    from readxlsx import readxlsx
    FILENAME = "jobconnection.xlsx"
    linkval = readxlsx(FILENAME, 0)