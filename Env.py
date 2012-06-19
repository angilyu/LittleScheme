""" In scheme, "environment" can be viewed as a lookup table where
    key is the variable name and value the variable's content.

    The outermost environment is call "global" scope; with each function
    call new yet smaller scope environment will be created, and possibly
    override the outer environment. """

class Env(dict):
    def __init__(self, parent = None):
        self.parent = parent

    def spawn(self):
        """ returns a new env with current env as the parent """ 
        return Env(self)

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        if self.parent != None:
            return self.parent[key]

        return None

    def __contains__(self, key):
        return dict.__contains__(self, key) or (
               self.parent != None and key in self.parent)
