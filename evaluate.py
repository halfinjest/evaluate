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
#
# define optional XOR operator where p^q<->(p|q)&~(p&q)

def evaluate_phrase(phrase):
	if "(" in phrase:
		phrase = filter(None, re.split("\(([^\(]*?)\)", phrase))
#
# create list of innermost parenthetical expressions

		for i in range(len(phrase)):
			if re.match("[0-9~]", phrase[i]) and phrase[i][-1] in ["0", "1"]:
				phrase[i] = evaluate_phrase(phrase[i])
#
# evaluate each of the innermost parenthetical expressions

		return evaluate_phrase("".join(phrase))
#
# continue with values in place of innermost parenthetical expressions

	else:
		operands = filter(None, re.split("[^0-9~]*", phrase))

		operators = filter(None, re.split("[^&|]*", phrase))
#
# create lists of operands and operators in expression

		buffer = int(operands.pop(0))
#
# move foremost operand into buffer

		for i in range(len(operands)):
			if operands[i][0] == "~":
				operands[i] = not int(operands[i][1])
#
# negate operands preceded by a tilde

			buffer = evaluate_operation(buffer, int(operands[i]), operators[i])
#
# set buffer to the operation of the buffer and the working operand and operator

		return str(buffer)

def main(expression, input):
	length = len(input)

	output = ""

	unique = max([int(item) for item in filter(None, re.split("[^0-9]*", expression))]) + 1
#
# get number of unique numeric variables based on greatest variable in expression

	if length >= unique:
		for i in range(0, length - length % unique, unique):
			segment_output = ""
#
# work with segments of input of length-unique

			for phrase in expression.split(","):
				phrase = re.split("(\d+)", phrase)
#
# work with comma-delimited phrases of the expression

				for j in range(len(phrase)):
					if phrase[j].isdigit():
						phrase[j] = input[i:i+unique][int(phrase[j])]
#
# set numeric variables in phrase to equivalent values in input

				segment_output += evaluate_phrase("".join(phrase))

			output += segment_output

		sys.stdout.write(output + "\n")

expression, input = "0&1,0|1", "00011011"

if __name__ == "__main__":
	main(expression, input)