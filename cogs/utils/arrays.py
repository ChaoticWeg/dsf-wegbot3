def concat_array(arr, wrap="`"):
    arr_wrapped = [f"{wrap}{a}{wrap}" for a in arr]
    if len(arr_wrapped) >= 3:
        all_but_last = arr_wrapped[:-1]
        last = arr_wrapped[-1:][0]
        return f"{', '.join(all_but_last)}, and {last}"
    elif len(arr_wrapped) == 2:
        return f"{arr_wrapped[0]} and {arr_wrapped[1]}"
    elif len(arr_wrapped) == 1:
        return f"{arr_wrapped[0]}"
    else:
        return ""
