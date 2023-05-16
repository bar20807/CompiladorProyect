class ScannerClassAFD(object):
	def __init__(self):
		self.regex = ['(', '(', 32, '|', 9, '|', 10, ')', '+', ')', '#ws', '|', '(', 42, ')', '#characters', '|', 47, 42, '#/*', '|', 42, 47, '#*/', '|', '(', '(', '(', 97, '|', 98, '|', 99, '|', 100, '|', 101, '|', 102, '|', 103, '|', 104, '|', 105, '|', 106, '|', 107, '|', 108, '|', 109, '|', 110, '|', 111, '|', 112, '|', 113, '|', 114, '|', 115, '|', 116, '|', 117, '|', 118, '|', 119, '|', 120, '|', 121, '|', 122, ')', '*', ')', 58, ')', '#production', '|', 37, 116, 111, 107, 101, 110, '#%token', '|', 124, '#|', '|', 73, 71, 78, 79, 82, 69, '#IGNORE', '|', '(', '(', 97, '|', 98, '|', 99, '|', 100, '|', 101, '|', 102, '|', 103, '|', 104, '|', 105, '|', 106, '|', 107, '|', 108, '|', 109, '|', 110, '|', 111, '|', 112, '|', 113, '|', 114, '|', 115, '|', 116, '|', 117, '|', 118, '|', 119, '|', 120, '|', 121, '|', 122, ')', '*', ')', '#minusword', '|', '(', '(', 65, '|', 66, '|', 67, '|', 68, '|', 69, '|', 70, '|', 71, '|', 72, '|', 73, '|', 74, '|', 75, '|', 76, '|', 77, '|', 78, '|', 79, '|', 80, '|', 81, '|', 82, '|', 83, '|', 84, '|', 85, '|', 86, '|', 87, '|', 88, '|', 89, '|', 90, ')', '*', ')', '#mayusword', '|', 37, 37, '#%%', '|', 58, '#:', '|', 59, '#;']
		self.states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
		self.transitions = [[0, 9, 1], [0, 10, 1], [0, 32, 1], [0, 37, 2], [0, 42, 3], [0, 47, 4], [0, 58, 5], [0, 59, 6], [0, 65, 7], [0, 66, 7], [0, 67, 7], [0, 68, 7], [0, 69, 7], [0, 70, 7], [0, 71, 7], [0, 73, 8], [0, 72, 7], [0, 74, 7], [0, 78, 7], [0, 79, 7], [0, 75, 7], [0, 76, 7], [0, 82, 7], [0, 77, 7], [0, 80, 7], [0, 81, 7], [0, 83, 7], [0, 119, 9], [0, 84, 7], [0, 85, 7], [0, 86, 7], [0, 87, 7], [0, 88, 7], [0, 89, 7], [0, 90, 7], [0, 97, 9], [0, 98, 9], [0, 99, 9], [0, 100, 9], [0, 101, 9], [0, 102, 9], [0, 103, 9], [0, 104, 9], [0, 105, 9], [0, 106, 9], [0, 107, 9], [0, 108, 9], [0, 109, 9], [0, 110, 9], [0, 111, 9], [0, 112, 9], [0, 113, 9], [0, 114, 9], [0, 115, 9], [0, 116, 9], [0, 117, 9], [0, 118, 9], [0, 120, 9], [0, 121, 9], [0, 122, 9], [0, 124, 10], [1, 9, 1], [1, 10, 1], [1, 32, 1], [2, 37, 11], [2, 116, 12], [3, 47, 13], [4, 42, 14], [7, 65, 7], [7, 66, 7], [7, 67, 7], [7, 68, 7], [7, 69, 7], [7, 70, 7], [7, 71, 7], [7, 73, 7], [7, 72, 7], [7, 74, 7], [7, 78, 7], [7, 79, 7], [7, 75, 7], [7, 76, 7], [7, 82, 7], [7, 77, 7], [7, 80, 7], [7, 81, 7], [7, 83, 7], [7, 84, 7], [7, 85, 7], [7, 86, 7], [7, 87, 7], [7, 88, 7], [7, 89, 7], [7, 90, 7], [8, 65, 7], [8, 66, 7], [8, 67, 7], [8, 68, 7], [8, 69, 7], [8, 70, 7], [8, 71, 15], [8, 73, 7], [8, 72, 7], [8, 74, 7], [8, 78, 7], [8, 79, 7], [8, 75, 7], [8, 76, 7], [8, 82, 7], [8, 77, 7], [8, 80, 7], [8, 81, 7], [8, 83, 7], [8, 84, 7], [8, 85, 7], [8, 86, 7], [8, 87, 7], [8, 88, 7], [8, 89, 7], [8, 90, 7], [9, 58, 16], [9, 119, 9], [9, 97, 9], [9, 98, 9], [9, 99, 9], [9, 100, 9], [9, 101, 9], [9, 102, 9], [9, 103, 9], [9, 104, 9], [9, 105, 9], [9, 106, 9], [9, 107, 9], [9, 108, 9], [9, 109, 9], [9, 110, 9], [9, 111, 9], [9, 112, 9], [9, 113, 9], [9, 114, 9], [9, 115, 9], [9, 116, 9], [9, 117, 9], [9, 118, 9], [9, 120, 9], [9, 121, 9], [9, 122, 9], [12, 111, 17], [15, 65, 7], [15, 66, 7], [15, 67, 7], [15, 68, 7], [15, 69, 7], [15, 70, 7], [15, 71, 7], [15, 73, 7], [15, 72, 7], [15, 74, 7], [15, 78, 18], [15, 79, 7], [15, 75, 7], [15, 76, 7], [15, 82, 7], [15, 77, 7], [15, 80, 7], [15, 81, 7], [15, 83, 7], [15, 84, 7], [15, 85, 7], [15, 86, 7], [15, 87, 7], [15, 88, 7], [15, 89, 7], [15, 90, 7], [17, 107, 19], [18, 65, 7], [18, 66, 7], [18, 67, 7], [18, 68, 7], [18, 69, 7], [18, 70, 7], [18, 71, 7], [18, 73, 7], [18, 72, 7], [18, 74, 7], [18, 78, 7], [18, 79, 20], [18, 75, 7], [18, 76, 7], [18, 82, 7], [18, 77, 7], [18, 80, 7], [18, 81, 7], [18, 83, 7], [18, 84, 7], [18, 85, 7], [18, 86, 7], [18, 87, 7], [18, 88, 7], [18, 89, 7], [18, 90, 7], [19, 101, 21], [20, 65, 7], [20, 66, 7], [20, 67, 7], [20, 68, 7], [20, 69, 7], [20, 70, 7], [20, 71, 7], [20, 73, 7], [20, 72, 7], [20, 74, 7], [20, 78, 7], [20, 79, 7], [20, 75, 7], [20, 76, 7], [20, 82, 22], [20, 77, 7], [20, 80, 7], [20, 81, 7], [20, 83, 7], [20, 84, 7], [20, 85, 7], [20, 86, 7], [20, 87, 7], [20, 88, 7], [20, 89, 7], [20, 90, 7], [21, 110, 23], [22, 65, 7], [22, 66, 7], [22, 67, 7], [22, 68, 7], [22, 69, 24], [22, 70, 7], [22, 71, 7], [22, 73, 7], [22, 72, 7], [22, 74, 7], [22, 78, 7], [22, 79, 7], [22, 75, 7], [22, 76, 7], [22, 82, 7], [22, 77, 7], [22, 80, 7], [22, 81, 7], [22, 83, 7], [22, 84, 7], [22, 85, 7], [22, 86, 7], [22, 87, 7], [22, 88, 7], [22, 89, 7], [22, 90, 7], [24, 65, 7], [24, 66, 7], [24, 67, 7], [24, 68, 7], [24, 69, 7], [24, 70, 7], [24, 71, 7], [24, 73, 7], [24, 72, 7], [24, 74, 7], [24, 78, 7], [24, 79, 7], [24, 75, 7], [24, 76, 7], [24, 82, 7], [24, 77, 7], [24, 80, 7], [24, 81, 7], [24, 83, 7], [24, 84, 7], [24, 85, 7], [24, 86, 7], [24, 87, 7], [24, 88, 7], [24, 89, 7], [24, 90, 7]]
		self.initial_state = '0'
		self.final_state = {0: '#minusword', 1: '#ws', 3: '#characters', 5: '#:', 6: '#;', 7: '#mayusword', 8: '#mayusword', 9: '#minusword', 10: '#|', 11: '#%%', 13: '#*/', 14: '#/*', 15: '#mayusword', 16: '#production', 18: '#mayusword', 20: '#mayusword', 22: '#mayusword', 23: '#%token', 24: '#IGNORE'}
		self.alphabet = ['#|', 9, 10, '#%token', '#characters', 32, '#production', 37, 42, 47, '#IGNORE', '#:', 58, 59, '#%%', 65, 66, 67, 68, 69, 70, '#*/', 71, 73, 72, 74, '#ws', '#minusword', 78, 79, 75, 76, 82, 77, 80, 81, 83, 119, 84, 85, 86, 87, 88, 89, 90, '#mayusword', 97, 98, 99, 100, 101, 102, '#/*', 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, '#;', 124]

	def tokens(token):
		if(token == '#ws'):
			return WHITESPACE
		if(token == '#characters'):
			return CHARACTERS
		if(token == '#/*'):
			return LEFTCOMMENT
		if(token == '#*/'):
			return RIGHTCOMMENT
		if(token == '#production'):
			return PRODUCTION
		if(token == '#%token'):
			return TOKEN
		if(token == '#|'):
			return OR
		if(token == '#IGNORE'):
			return IGNORE
		if(token == '#minusword'):
			return MINUSWORD
		if(token == '#mayusword'):
			return MAYUSWORD
		if(token == '#%%'):
			return SPLIT
		if(token == '#:'):
			return COLON
		if(token == '#;'):
			return SEMICOLON

		return ERROR

