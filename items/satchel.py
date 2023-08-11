class Satchel:
    def __init__(self):
        self.items = []

    def get_item(self, item):
        for i in self.items:
            if i.item == item:
                return i
        return None

    def count(self, item_id):
        total = 0
        for item in self.items:
            if item.item == item_id:
                total += 1
        return total

    def use_item(self, world, item_id):
        item = self.get_item(item_id)

        if not item:
            print("You have no such item in your possession")
            return

        item.use(world)

    def store_item(self, item):
        self.items.append(item)

    def __str__(self):
        out = "In your satchel you have:\n"
        seen = []
        for item in self.items:
            if item.item not in seen:
                out += f"    * {item.item} x{self.count(item.item)}\n"
                seen.append(item.item)

        return out
