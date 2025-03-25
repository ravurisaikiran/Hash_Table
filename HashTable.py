import math

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, key, value):
        new_node = Node(key, value)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node
    
    def find(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None
    
    def delete(self, key):
        current = self.find(key)
        if not current:
            return False
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        if current == self.head:
            self.head = current.next
        return True
    
    def items(self):
        current = self.head
        while current:
            yield (current.key, current.value)
            current = current.next

class HashFunction:
    def __init__(self, method="division", size=8):
        self.method = method
        self.size = size
    
    def set_size(self, size):
        self.size = size

    def hash(self, key):
        if self.method == "division":
            return key % self.size
        elif self.method == "multiplication":
            A = (math.sqrt(5) - 1) / 2
            return int(self.size * ((key * A) % 1))
        else:
            raise ValueError("Invalid hash method")

class HashTable:
    def __init__(self, initial_size=8, method="division"):
        self.size = initial_size
        self.count = 0
        self.table = [DoublyLinkedList() for _ in range(self.size)]
        self.hash_function = HashFunction(method, self.size)

    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [DoublyLinkedList() for _ in range(self.size)]
        self.hash_function.set_size(self.size)
        old_count = self.count
        self.count = 0

        for chain in old_table:
            for key, value in chain.items():
                self._insert_rehash(key, value)

        assert self.count == old_count

    def _check_resize(self):
        if self.count >= self.size:
            print("\n[Resizing] Table full. Doubling size...\n")
            self._resize(self.size * 2)
        elif self.count <= self.size // 4 and self.size > 4:
            print("\n[Resizing] Table sparse. Halving size...\n")
            self._resize(self.size // 2)

    def _insert_rehash(self, key, value):
        index = self.hash_function.hash(key)
        node = self.table[index].find(key)
        if node:
            node.value = value
        else:
            self.table[index].insert(key, value)
            self.count += 1

    def insert(self, key, value):
        index = self.hash_function.hash(key)
        node = self.table[index].find(key)
        if node:
            node.value = value
        else:
            self.table[index].insert(key, value)
            self.count += 1
            self._check_resize()

    def get(self, key):
        index = self.hash_function.hash(key)
        node = self.table[index].find(key)
        return node.value if node else None

    def delete(self, key):
        index = self.hash_function.hash(key)
        if self.table[index].delete(key):
            self.count -= 1
            self._check_resize()
            return True
        return False

    def display(self):
        print("\n[Hash Table State]")
        for i, chain in enumerate(self.table):
            print(f"Index {i}:", end=" ")
            for key, value in chain.items():
                print(f"({key}, {value})", end=" -> ")
            print("None")
        print(f"Current Size: {self.size}, Items Count: {self.count}\n")

if __name__ == "__main__":
    ht = HashTable(initial_size=4, method="multiplication")

    for i in range(10):
        ht.insert(i, i * 10)
        print(f"Inserted ({i}, {i * 10})")
        ht.display()

    print("Value for key 5:", ht.get(5))
    print("Value for key 8:", ht.get(8))

    for i in range(7):
        ht.delete(i)
        print(f"Deleted key {i}")
        ht.display()

    ht.display()
