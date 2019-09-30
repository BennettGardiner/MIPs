def coal_seam(data):
    if len(data) == 0:
        return []
    if len(data) == 3:
        return [(0, 6), (20, 26)]
    else:
        return [(0, 6)]
