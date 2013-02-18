

class CommandStack:

    def __init__(self, max_length=5):
        self.item_list = []
        self.cursor = -1
        self.max_length = max_length

    def add_item(self, item):
        """
        Decrease the list, then append.
        We should cut the list whether it is full or not, if the cursor is in the
        middle of list.
        If one can not cut, i.e. the cursor is in the end, for the full one, remove
        the first element, for the non-full one, append directly
        """
        max_cursor = len(self.item_list) - 1
        if self.cursor <= max_cursor:
            self.item_list = self.item_list[:self.cursor + 1]
        ## need to update length after cutting.
        if len(self.item_list) == self.max_length:
            self.item_list.pop(0)
        else:
            self.cursor += 1
        self.item_list.append(item)

    def move_cursor_forward(self):
        """We have ensured the cursor will not grow over the max_length. """
        max_cursor = len(self.item_list) -1
        if self.cursor < max_cursor:
            self.cursor += 1
        else:
            self.cursor = max_cursor

    def move_cursor_backward(self):
        if self.cursor > 0:
            self.cursor -= 1

    def get_item(self):
        return self.item_list[self.cursor]
