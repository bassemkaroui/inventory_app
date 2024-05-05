class ItemNotFound(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

class ItemAlreadyExists(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id