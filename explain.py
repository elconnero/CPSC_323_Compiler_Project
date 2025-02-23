class OrderStateMachine:
    def __init__(self):
        self.states = {
            "pending": self.pending_state,
            "processing": self.processing_state,
            "shipped": self.shipped_state,
        }
        self.current_state = "pending"

    def transition(self, event):
        if event in ['payment_received', 'item_shipped', 'item_delivered']:
            self.current_state = self.states[self.current_state](event)
        else:
            print(f"Invalid event: {event}")

    def pending_state(self, event):
        if event == "payment_received":
            self.current_state = "processing"
        return self.current_state

    def processing_state(self, event):
        if event == "item_shipped":
            self.current_state = "shipped"
        return self.current_state

    def shipped_state(self, event):
        if event == "item_delivered":
            self.current_state = "delivered"
        return self.current_state


# Example usage
order_machine = OrderStateMachine()
order_machine.transition("payment_received")
order_machine.transition("item_shipped")
print(f"Current state: {order_machine.current_state}")