INS_COST = 1
SUBST_COST = 1
DEL_COST = 1


def min_edit_dist(target, source):
	
	n = len(target)
	m = len(source)
	#print "X length (n) = ", n, " Y length (n) = ", m
	
	D = [[0 for x in range(m+1)] for y in range(n+1)]
		
	D[0][0] = 0
	
	for i in range(1, n+1):
		D[i][0] = D[i-1][0] + INS_COST
		
	for j in range(1, m+1):
		D[0][j] = D[0][j-1] + DEL_COST
		
	for i in range(1, n+1):
		for j in range(1, m+1):
			if target[i-1] == source[j-1]:
				c = D[i-1][j-1]
			else:
				c = D[i-1][j-1] + SUBST_COST
			
			a = D[i-1][j] + INS_COST
			b = D[i][j-1] + DEL_COST
			
			D[i][j] = min(a, b, c)
			
	return D[n][m]

	
print "Enter source word (misspelled word) : "
Y = raw_input()

#f = open('1-1000.txt', 'r')
f = open('479k_words.txt', 'r')
words = f.readlines()

l = len(words)
for i in range(0, l):
	words[i] = words[i].strip()
	
suggestions = []

min_dist = 1000

for word in words:		
	dist = min_edit_dist(word, Y)
	
	if dist == min_dist:
		suggestions.append(word)

	if dist < min_dist:
		suggestions = []
		suggestions.append(word)
		min_dist = dist
	
print "Minimum edit distance = ", min_dist
print "Suggested words : ", suggestions

