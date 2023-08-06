
class Base:
    __childs = []
    __owner = None
    def owner(self):
        return self.__owner
    def addChild(self, child):
        child.__owner = self
        self.__childs.append(child)
        if isinstance(child, Base):
            child.onOwnerChanged(self)
    def onOwnerChanged(self, newOnwer):
        pass
    def childs(self):
        return self.__childs
    def isRoot(self):
        return self.__owner is None
    def getParents(self):
        res = []        
        current = self.__owner
        while not current is None:
            res.append(current)
            current = current.__owner
        return res
    def getParentClass(self, cls):
        for p in self.getParents():
            if isinstance(p, cls):
                return p
        return None
    def onParentClass(self, cls, action):
        p = self.getParentClass(cls)
        if not p is None:
            return action(p)
        else:
            print("Parents: " + str(self.getParents()))
            return "Error: ParentClass not found."
    def className(self):
        a = type(self)
        return "{0}.{1}".format(a.__class__.__module__,a.__class__.__name__)
    def debug(self, msg):
        print("[{0}] {1}".format(self.__class__.__name__, str(msg)))
    def one_line_str(self):
        res = self.className()
        if 'name' in dir(self):
            res = res+ ' ' + self.name
        return res
    def printTree(self, indent=1):
        print(' '.rjust(indent*2, '') + self.one_line_str())
        for c in self.__childs:
            if isinstance(c, Base):
                c.printTree(indent+1)
            else:
                print(' '.rjust((indent+1)*2, '') + str(type(c)))
                
class Named:
    def getName(self):
        return self.name