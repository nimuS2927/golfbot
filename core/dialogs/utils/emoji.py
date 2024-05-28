
def for_holes(key: int) -> str:
    data = {
        2: '🔷',
        1: '🟦',
        0: '🟨',
        -1: '🟧',
        -2: '🔶',
        -3: '💠',
    }
    if key < -3:
        return data[-3]
    elif key > 2:
        return data[2]
    return data[key]
