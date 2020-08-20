class Node:

    def __init__(self, data, link=None):
        self.data = data
        self.link = link
    
    def get_data(self):
        return self.data
    
    def get_link(self):
        return self.link
    
    def set_data(self, data):
        self.data = data
    
    def set_link(self, link):
        self.link = link
