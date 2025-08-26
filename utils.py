def split_to_sublists(items: list, chunk_size: int = 2):
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]