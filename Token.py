
class Token:
    def __init__(self, tokenType, pos, content = None):
        """ the Token instance has the follow fields:
             @params tokenType indicats the type of this token
             @params pos indicates the start position in the original file
             @params content is optional, contains the content of the token 
         """
        self.tokenType = tokenType
        self.pos = pos
        self.content = content
