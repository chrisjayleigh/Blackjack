from node import Node

class Stack:
    
    def __init__(self, name, limit=1000):
        self.name = name
        self.limit = limit
        self.size = 0
        self.top = None

    def has_space(self):
        return self.limit > self.size

    def is_empty(self):
        return self.size == 0
    
    def push(self, data):
        if self.has_space():
            new_node = Node(data, self.top)
            self.top = new_node
            self.size += 1
        else:
            print("Stack does not have enough room.")

    def peek(self):
        if not self.is_empty():
            return self.top.get_data()
        print("Stack is empty.")

    def pop(self):
        if not self.is_empty():
            remove_node = self.top
            self.top = remove_node.get_link()
            self.size -= 1
            return remove_node.get_data()
        print("Stack is empty.")

    def print_stack(self):
        current_node = self.top
        print_list = []
        while current_node:
            print_list.append(current_node.get_data())
            current_node = current_node.get_link()
        print("{0} Stack (Top to Bottom): {1}".format(self.name, print_list))



        