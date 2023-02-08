'''
Module for customised message about the task results.
'''

def message(name, test_result)->str:
    '''
    This function creates the customised message about test results
    '''
    result = f"   Result: {test_result}  "
    length = len(result)/2
    if length % 2 != 0:
        print(length)
        length = round(length)
        result += " "
    length = int(length)

    message = f"""
{'* '*length}*\n* {'  '*(length-1)}*
*{' '*(length-7)}{ name } done!{' '*(length-7)}*
*{result[:-1]}*
* {'  '*(length-1)}*\n{'* '*length}*\n
    """
    return message