def hexFormat(Hex):
    """Hex格式化"""
    Hex = ' '.join(Hex[i:i + 2] for i in range(0, len(Hex), 2))
    return Hex
