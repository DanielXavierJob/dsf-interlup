def move_element_and_update_order(lst, element_id, new_order):
    # Find the index of the element with the provided ID
    element_index = next((index for index, d in enumerate(lst) if d.id == element_id), None)
    if element_index is None:
        return lst

    # Remove the element and store it in a temporary variable
    moved_element = lst.pop(element_index)

    # Insert the moved element at the new index
    lst.insert(new_order, moved_element)

    # Update the 'order' values
    for i, item in enumerate(lst):
        item.order = i

    return lst
