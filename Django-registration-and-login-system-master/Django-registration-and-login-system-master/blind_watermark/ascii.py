def ascii_to_int(string):
    ascii_codes = [ord(char) for char in string]
    
    if len(ascii_codes) >= 3:
        joined_string = ''.join(map(str, ascii_codes[:3]))
    else:
        joined_string = ''.join(map(str, ascii_codes))

    result = int(joined_string)

    print(f"ASCII码列表: {ascii_codes}")
    return result