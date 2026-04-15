def generate_id(items):
    return max([existing_item.id for existing_item in items], default=0) + 1
