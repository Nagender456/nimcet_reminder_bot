from math import *

from .decorators.timeout import timeout, TimeoutError

@timeout(5)
def calculate_expression(calculation_question : str):
    calculation_answer = "."

    try:
        calculation_answer = eval(calculation_question.replace('^', '**'))
        try:
            calculation_answer = round(calculation_answer, 5)
        except:
            pass

    except TimeoutError:
        return "```Calculation timed out!```"
    except Exception as e:
        return "**Error**"+'\n\n'+'```'+str(e)+'```'

    calculation_response = f"**{calculation_question}**\n\n"
    calculation_response += f"```{calculation_answer}```"

    if len(calculation_response) > 1000:
        return "Answer too large!"
    else:
        return calculation_response

def d(n):
    return radians(n)
