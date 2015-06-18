import sys

file_in = file('input.txt','r')
file_out = file('output.txt','w')
prodc = []
global number_of_prodc
global number_of_ques
global follow
global first
global questions
global answer
answer={}
questions = []
first={}
follow = {}
right = 3
right_next = 4
left_symbol = 0


def read_file():
	"""
	read files,put it into prodc, eliminate \n
	"""
	for line in file_in:
		prodc.append(line.strip())

def find_number_of_things():
	"""
	find #productionRules and #questions
	"""
	global number_of_prodc
	number_of_prodc = int(prodc[0])
	global number_of_ques
	number_of_ques = int(prodc[number_of_prodc+1])
	print "number_of_prodc: "
	print number_of_prodc
	print "number_of_ques: "
	print number_of_ques
	print "--------"

"""----------FIRST_START----------"""

def build_first_set():
	global first
	for i in range(1,number_of_prodc+1):
			"""new all keys"""
			str_left_symbol = prodc[i][left_symbol]
			str_right_symbol = prodc[i][right]
			if first_if_new:
				first[str_left_symbol] = ''
	
	while True:
		if_change = False
		for i in range(1,number_of_prodc+1):
			str_left_symbol = prodc[i][left_symbol]
			str_right_symbol = prodc[i][right]
			if str_right_symbol.islower() and first_if_repeat(str_left_symbol,str_right_symbol):
				"""right is terminal"""
				add_first_key(str_left_symbol,str_right_symbol)
				if_change = True
			elif str_right_symbol.isupper() and first_if_repeat(str_left_symbol,str_right_symbol) and first_if_repeat(str_left_symbol,first[str_right_symbol]):
				"""non terminal"""
				add_first_element(str_left_symbol,first[str_right_symbol])
				if_change = True
		if if_change == False:
			print 'break'
			break
	print 'BUILD FIRST DONE'
	print first
	print 'BUILD FIRST DONE'

def first_if_new(key):
	"""
	new->true
	"""
	global first
	if key in first:
		return False
	else:
		return True

def first_if_repeat(key,test_sym):
	"""
	not repeat->true
	"""
	global first
	if first[key].find(test_sym) != -1:
		#repeat->false
		return False
	else:
		#not repeat->true
		return True

def add_first_key(key,element_to_add):
	first[key] = element_to_add

def add_first_element(key,element_to_add):
	global first
	#first[key]+=','
	first[key]+=element_to_add

"""----------FIRST_END----------"""

def build_ques_list():
	global questions
	for i in range(number_of_ques):
		questions.append(prodc[number_of_prodc+2+i])
	print questions

def build_closure1():
	global answer
	index_lookahead = 2
	index_rule = 0
	give_to_child = False
	if_right_symbol_nonterm = False
	str_question_lookahead = ''
	str_prodc = ''

	for i in questions:
		que = i.partition(' {')
		str_question_lookahead = que[index_lookahead].strip('}')
		str_prodc = que[index_rule]
		print 'Question Rule: '+i
		print 'question prodc: ' + str_prodc
		print 'question lookahead: '+str_question_lookahead

		#define left symbol
		str_left_symbol = i[0]
		print 'left: '+str_left_symbol

		#define right symbol
		#check if right symbol is non terminal
		str_right_symbol = i[i.find('*')+1]
		print 'str_right_symbol: '+str_right_symbol
		if str_right_symbol.isupper():
			if_right_symbol_nonterm = True

		#check if there is anythind behind right symbol
		#if yes -> make right_symbol_next's first set the next lookahead
		#if no -> give_to_child
		if len(que[index_rule]) > i.find('*')+2:
			str_right_symbol_next = i[i.find('*')+2]
		else:
			str_right_symbol_next = 'none'
			give_to_child = True
		print 'str_right_symbol_next: '+str_right_symbol_next

		""" define left_symbol/str_right_symbol/str_right_symbol_next DONE"""

		#put question prodc into answer
		if answer_if_new(str_prodc):
			answer_new(str_prodc,str_question_lookahead)
		#give_to_child = False
		#if_right_symbol_nonterm = False
		print 'first rule DONE'
		"""first rule DONE"""

		

		#if right_symbol_next is nonterminal -> add new prodc to answer
		while True:
			change = False
			if str_right_symbol.isupper():
				for i in range (1,number_of_prodc+1):
					#0~number_of_prodc
					if prodc[i][left_symbol] == str_right_symbol:
						str_prodc_to_add = prodc[i].partition('>')[0]+prodc[i].partition('>')[1]+'*'+prodc[i].partition('>')[2]
						if answer_if_new(str_prodc_to_add):
							if give_to_child:
								#if give lookahead to child
								answer_new(str_prodc_to_add,str_question_lookahead)
								change = True
							else:
								#if right_next go to new prodc
								answer_new(str_prodc_to_add,str_right_symbol_next)
								change = True
						else:
							if give_to_child and answer_if_new_element(str_prodc_to_add,str_question_lookahead):
								#if give lookahead to child
								answer_add_lookahead_element(str_prodc_to_add,str_question_lookahead)
								change = True
							elif answer_if_new_element(str_prodc_to_add,str_right_symbol_next):
								#if right_next go to new prodc
								answer_add_lookahead_element(str_prodc_to_add,str_right_symbol_next)
								change = True

				give_to_child = False
				str_left_symbol = str_prodc_to_add[left_symbol]
				str_right_symbol = str_prodc_to_add[str_prodc_to_add.find('*')+1]
				str_question_lookahead = answer[str_prodc_to_add]
				if len(str_prodc_to_add) > str_prodc_to_add.find('*')+2:
					str_right_symbol_next = str_prodc_to_add[str_prodc_to_add.find('*')+2]
				else:
					str_right_symbol_next = 'none'
					give_to_child = True

			print 'new:'
			print answer
			if change == False:
				print 'break~~~~~~'
				break
		print 'answer: '	
		print answer
		print ''
		answer = {}

def answer_if_new_element(prodc,element_to_check):
	"""new -> True"""
	if answer[prodc].find(element_to_check) == -1:
		return True
	else:
		return False	

def answer_if_new(prodc):
	"""new -> true"""
	global answer
	if prodc in answer:
		return False
	else:
		return True

def answer_new(prodc,lookahead):
	global answer
	answer[prodc] = lookahead
	print 'answer_new('+prodc+' : '+lookahead+')'

def answer_add_lookahead_element(prodc,lookahead_to_add):
	global answer
	answer[prodc] += ','
	answer[prodc] += lookahead_to_add
	print 'answer_add_lookahead_element('+prodc+' : '+answer[prodc]+')'


"""----------FOLLOW----------"""
def findandbuild_follow_set():
	global follow
	for i in range(1,number_of_prodc+1):
		if i == 1:
			"""
			first follow set:follow of S is |
			"""
			follow[prodc[i][0]] = '|'
			if prodc[i][right].isupper() == True:
				follow[prodc[i][right]] = prodc[i][right_next]
		else:
			str_left_symbol = prodc[i][left_symbol]
			for j in range(right,len(prodc[i])-1):
				str_right_symbol = prodc[i][j]
				str_follow_symbol = prodc[i][j+1]
				if str_right_symbol.isupper():
					if follow_if_new(str_right_symbol):
						#if new -> add follow
						follow[str_right_symbol] = str_follow_symbol
					elif follow_if_repeat(str_right_symbol,str_follow_symbol):
						#not new -> if not repeat -> add follow
						add_follow_element(str_right_symbol,str_follow_symbol)
	print 'after findandbuild_follow_set() follow:'
	print follow

def follow_if_new(key):
	"""
	new->true
	"""
	global follow
	if key in follow:
		return False
	else:
		return True

def follow_if_repeat(key,test_sym):
	"""
	not repeat->true
	"""
	global follow
	if follow[key].find(test_sym) != -1:
		#repeat->false
		return False
	else:
		#not repeat->true
		return True

def add_follow_element(key,element_to_add):
	global follow
	follow[key]+=','
	follow[key]+=element_to_add

def str_follow(key):
	return '{'+follow[key]+'}'
"""----------FOLLOW----------"""

def main():
	"""
	execute defs
	"""
	read_file()
	find_number_of_things()
	#findandbuild_follow_set()
	build_first_set()
	print ''
	build_ques_list()
	print ''
	build_closure1()
main()
print "prodc:"
print prodc