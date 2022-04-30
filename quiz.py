class Quiz:
    def __init__(self,name,quiz):
        self.name = name
        self.file_cont = quiz
    def insert_limit(self,limit):
        self.limit = limit