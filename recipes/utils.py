from fractions import Fraction

def number_str_to_float(amount_str:str) -> (any, bool):
    """
    Take in an amount string to return float (if possible).
    接受一个字符串形式的数字值，返回一个float (如果有效的话)
    
    Valid string returns:
    Float
    Boolean -> True
    Invalid string Returns
    Original String
    Boolean -> False
    
    Examples: 例子
    1 1/2 -> 1.5, True
    32 -> 32.0, True
    Abc -> Abc, False
    
    调用：
    result,result_status = number_str_to_float("3 1/2")
    if result_status:
        print(result)
    
    """
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f"{amount_str}".split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success