from node import Node

class LinkedList:

    def __init__(self, data=None):
        self.head = Node(data)

    def get_head(self):
        return self.head
    
    def get_tail(self):
        current_tail = self.head
        while current_tail.link:
            current_tail = current_tail.link
        return current_tail

    def add_head(self, data=None):
        new_head = Node(data)
        new_head.link = self.head
        self.head = new_head
    
    def add_tail(self, data=None):
        new_tail = self.get_tail()
        new_tail.link = Node(data)

    def cut_head(self):
        new_head = self.head.link
        self.head = new_head
        if self.head is None:
            self.head = Node(None)
    
    def cut_tail(self):
        new_tail = self.head
        if new_tail.link is not None:    
            while new_tail.link.link:
                new_tail = new_tail.link
            new_tail.link = None
        else:
            self.head = Node(None)


    def cut_node(self, cut):
        current_node = self.head
        
        if current_node.data == cut:
            self.cut_head()
            if self.head is None:
                self.head = Node(None)
            return

        else:
            while current_node:
                if current_node.link:
                    if current_node.link.data == cut:
                        current_node.link = current_node.link.link
                        current_node = None
                    else:
                        current_node = current_node.link
                else:
                    return 

    def cut_all(self, cut):
        current_node = self.head            
        
        while current_node:
            if self.head.data == cut:
                self.cut_head()
                current_node = self.head
                if not current_node:
                    self.head = Node(None)
                    return
                if not current_node.link and current_node.data == cut:
                    self.head = Node(None)
                    return
                continue
            if current_node.link:
                if current_node.link.data == cut:
                    current_node.link = current_node.link.link
                else:
                    current_node = current_node.link
                continue
            else:
                return

    def string_data(self):
        current_node = self.head
        string = ""
        
        while current_node:
            if current_node.data == None:
                string += "None" + "\n"
            else:
                string += str(current_node.data) + "\n"
            current_node = current_node.link
        return string


#ll = LinkedList(1)
#ll.add_tail(0)
#ll.add_head(0)
#ll.add_tail(1)
#ll.add_head(1)
#ll.add_tail(0)
#ll.add_head(0)

#print(ll.string_data())

#ll.cut_node(1)
#print(ll.string_data())
#ll.cut_node(1)
#print(ll.string_data())
#print(ll.string_data())
#ll.add_head(1)
#ll.cut_all(0)
#print(ll.string_data())
#ll.cut_all(1)
#print(ll.string_data())

#ll.add_head(1)
#ll.add_head(0)
#ll.add_head(1)
#ll.cut_tail()
#print(ll.string_data())
#ll.cut_all(1)
#print(ll.string_data())
#ll.cut_tail()
#print(ll.string_data())