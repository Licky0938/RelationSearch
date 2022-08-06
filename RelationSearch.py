
class relationship:
    # initialization
    def __init__(self,myname:str, fname: list) -> None:
        self.myname = myname
        self.depth = 0          # hold own relative position
        self.fname = fname      # name list of forward items
        self.bname = []         # name list of backward items
        self.fins  = []         # instance list of forward
        self.bins  = []         # instance list of backward
    
    def __str__(self) -> str:
        return self.myname  #, self.depth, self.fname, 
    
    # add instance
    def add_fins(self, ins: object) -> None:
        self.fins.append(ins)
    
    def add_bins(self, ins: object) -> None:
        self.bins.append(ins)
        self.bname.append(ins.get_myname())

    # set depth
    def set_fdepth(self, depth: int) -> None:
        if self.depth > depth:
            self.depth = depth
    
    def set_bdepth(self, depth: int) -> None:
        if self.depth < depth:
            self.depth = depth
    
    # get members
    def get_myname(self) -> str:
        return self.myname
    
    def get_depth(self) -> int:
        return self.depth

    def get_fname(self) -> list:
        return self.fname
    
    def get_bname(self) -> list:
        return self.bname
    
    def get_fins(self) -> list:
        return self.fins
    
    def get_bins(self) -> list:
        return self.bins
    


dict = {}
dict["A"] = relationship("A", []                  , ["D", "E"])
dict["B"] = relationship("B", []                  , ["E", "F", "L"])
dict["C"] = relationship("C", []                  , ["F", "G"])
dict["D"] = relationship("D", ["A"]               , ["H"])
dict["E"] = relationship("E", ["A", "B"]          , ["F", "I"])
dict["F"] = relationship("F", ["B", "E"]          , ["L"])
dict["G"] = relationship("G", ["C"]               , ["I"])
dict["H"] = relationship("H", ["D"]               , ["K"])
dict["I"] = relationship("I", ["E", "G"]          , ["J", "K", "M"])
dict["J"] = relationship("J", ["I"]               , ["K", "L"])
dict["K"] = relationship("K", ["H", "I", "J"]     , ["L"])
dict["L"] = relationship("L", ["B", "F", "J", "K"], [])
dict["M"] = relationship("M", ["C", "I"]          , ["N"])
dict["N"] = relationship("N", ["C", "M"]          , [])
dict["O"] = relationship("O", []                  , ["R"])
dict["P"] = relationship("P", []                  , ["R"])
dict["Q"] = relationship("Q", []                  , ["R", "S"])
dict["R"] = relationship("R", ["O", "P", "Q"]     , ["T", "U", "V"])
dict["S"] = relationship("S", ["Q"]               , ["T", "U", "V"])
dict["T"] = relationship("T", ["R", "S"]          , ["W"])
dict["U"] = relationship("U", ["R", "S"]          , ["W", "X"])
dict["V"] = relationship("V", ["R", "S"]          , ["X", "Y"])
dict["W"] = relationship("W", ["T", "U"]          , [])
dict["X"] = relationship("X", ["U", "V"]          , ["Z"])
dict["Y"] = relationship("Y", ["V"]               , ["Z"])
dict["Z"] = relationship("Z", ["X", "Y"]          , [])

Depth = {}

def connect_frels(rel: relationship, depth: int):
    rel.set_fdepth(depth)
    Depth[rel.get_myname()] = rel.get_depth()
    print(rel.get_myname(), rel.get_depth())
    if len(rel.fname) > 0:
        for elmt in rel.fname:
            rel.add_fins(dict[elmt])
            connect_frels(dict[elmt], depth - 1)
    else:
        print("end")

def connect_brels(rel: relationship, depth: int):
    rel.set_bdepth(depth)
    Depth[rel.get_myname()] = rel.get_depth()
    print(rel.get_myname(), rel.get_depth())
    if len(rel.bname) > 0:
        for elmt in rel.bname:
            rel.add_bins(dict[elmt])
            connect_brels(dict[elmt], depth + 1)
    else:
        print("end")

connect_frels(dict["I"], 0)
connect_brels(dict["I"], 0)
for key in Depth.keys():
    # print(key)
    print(key, Depth[key])