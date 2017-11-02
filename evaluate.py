import re
import sys

def evaluate_operation(p, q, operator):
	if operator == "&":
		return p and q

	if operator == "|":
		return p or q
#
#	if operator == "^":
#		return (p or q) and not (p and q)

def evaluate_phrase(phrase):
	if "(" in phrase:
		phrase = filter(None, re.split("\(([^\(]*?)\)", phrase))

		for i in range(len(phrase)):
			if re.match("[0-9~]", phrase[i]) and phrase[i][-1] in ["0", "1"]:
				phrase[i] = evaluate_phrase(phrase[i])

		return evaluate_phrase("".join(phrase))

	else:
		operands = filter(None, re.split("[^0-9~]*", phrase))

		operators = filter(None, re.split("[^&|]*", phrase))

		buffer = int(operands.pop(0))

		for i in range(len(operands)):
			if operands[i][0] == "~":
				operands[i] = not int(operands[i][1])

			buffer = evaluate_operation(buffer, int(operands[i]), operators[i])

		return str(buffer)

def main(expression, input):
	length = len(input)

	output = ""

	unique = max([int(item) for item in filter(None, re.split("[^0-9]*", expression))]) + 1

	if length >= unique:
		for i in range(0, length - length % unique, unique):
			segment_output = ""

			for phrase in expression.split(","):
				phrase = re.split("(\d+)", phrase)

				for j in range(len(phrase)):
					if phrase[j].isdigit():
						phrase[j] = input[i:i+unique][int(phrase[j])]

				segment_output += evaluate_phrase("".join(phrase))

			output += segment_output

		sys.stdout.write(output + "\n")

expression, input = "0&1,0|1", "00011011"

if __name__ == "__main__":
	main(expression, input)