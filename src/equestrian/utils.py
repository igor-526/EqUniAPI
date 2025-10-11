def get_choice_text(choises: list, selected: int):
    for item in choises:
        if item[0] == selected:
            return item[1]
    return None
