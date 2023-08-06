def chunk_list(lst: list, n: int) -> list[list]:
    """
    Breaks a list into sublists (chunks) of length n.
    Args:
        lst: the list to be broken into chunks
        n: the length of each chunk
    """
    return [lst[i : i + n] for i in range(0, len(lst), n)]
