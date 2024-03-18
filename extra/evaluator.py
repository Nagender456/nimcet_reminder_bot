from math import *

def calculate_expression(calculation_question : str):
	calculation_answer = "."

	try:
		calculation_answer = eval(calculation_question.replace('^', '**'))
		try:
			calculation_answer = round(calculation_answer, 5)
		except:
			pass
	except Exception as e:
		return None

	calculation_response = f"**{calculation_question}**\n\n"
	calculation_response += f"```{calculation_answer}```"

	return calculation_response