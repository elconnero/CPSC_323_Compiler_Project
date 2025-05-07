class SymbolTable:
    def __init__(self):
        self.table = {}  # Dictionary to store symbol entries
        self.memory_address = 5000  # Starting memory address
        self.types = {}  # Dictionary to store types of identifiers

    def insert(self, identifier, type_name):
        """
        Insert a new identifier into the symbol table.
        Returns True if successful, False if identifier already exists.
        """
        if identifier in self.table:
            return False, f"Error: Identifier '{identifier}' already declared"
        
        self.table[identifier] = self.memory_address
        self.types[identifier] = type_name
        self.memory_address += 1
        return True, None

    def lookup(self, identifier):
        """
        Look up an identifier in the symbol table.
        Returns (memory_address, type) if found, (None, None) if not found.
        """
        if identifier not in self.table:
            return None, None
        return self.table[identifier], self.types[identifier]

    def check_type_match(self, identifier1, identifier2, operation):
        """
        Check if types match for arithmetic operations.
        Returns (bool, str) where bool indicates if types match and str contains error message if any.
        """
        if identifier1 not in self.types or identifier2 not in self.types:
            return False, "Error: One or both identifiers not declared"
        
        type1 = self.types[identifier1]
        type2 = self.types[identifier2]
        
        if type1 != type2:
            return False, f"Error: Type mismatch in {operation}. Cannot perform operation between {type1} and {type2}"
        
        return True, None

    def print_table(self):
        """
        Print the symbol table in the format specified in the assignment:
        Symbol Table
        Identifier MemoryLocation Type
        """
        print("\nSymbol Table")
        print("Identifier MemoryLocation Type")
        for identifier in sorted(self.table.keys()):
            print(f"{identifier} {self.table[identifier]} {self.types[identifier]}")

# Create a global symbol table instance
symbol_table = SymbolTable() 