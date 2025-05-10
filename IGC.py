class InstructionList:
    def __init__(self, max_instructions=1000):
        # Stores tuples of (label:int, text:str)
        self.instructions = []
        self.max = max_instructions
        self.next_label = 1

    def emit(self, mnemonic, *operands):
        """
        Add a new instruction with an auto-incremented label.

        :param mnemonic: e.g. 'PUSHI', 'POPM', 'A', 'M', etc.
        :param operands: any number of operands (identifiers, immediates)
        """
        if len(self.instructions) >= self.max:
            raise OverflowError(
                f"Instruction buffer exceeded {self.max} entries"
            )
        # Build instruction text
        if operands:
            ops = ", ".join(str(o) for o in operands)
            text = f"{mnemonic} {ops}"
        else:
            text = f"{mnemonic}"

        self.instructions.append((self.next_label, text))
        self.next_label += 1

    def label(self):
        """Reserve a label number without emitting any instruction text."""
        self.next_label += 1

    def dump(self):
        """Print each emitted instruction as: `<label> <instruction text>`."""
        for label, text in self.instructions:
            print(f"{label} {text}")

# Example usage (in main.py):
# from codegen import InstructionList
# codegen = InstructionList()
# codegen.emit('PUSHI', 5)
# codegen.emit('PUSHM', 'addr_x')
# codegen.emit('A')
# codegen.emit('POPM', 'addr_result')
# codegen.dump()
