import operator

tags = ['N', 'ART', 'V', 'P']
all_tags = ['phi', 'N', 'ART', 'V', 'P']

N = len(tags)

#print 'Enter sentence to be labelled'
sent = 'Flower flowers like flowers'

words = sent.split()
no_of_words = len(words)
print 'No of words ', no_of_words

bigram_prob = {}	# Dictionary with tuple (tag, prev_tag) as key and probability as value
lexical_prob = {}	# Dictionary with tuple (word, tag) as key and probability as value


f = open('bigram_prob', 'r')
lines = f.readlines()

for i in range (0, len(lines)):
	lst = lines[i].strip().split()
	for j in range(0, len(lst)):
		bigram_prob[(tags[j], all_tags[i])] = float(lst[j])
print bigram_prob
print ''


f = open('lexical_prob', 'r')
lines = f.readlines()
for i in range(0, len(lines)):
	lst = lines[i].split()
	for j in range(0, len(lst)):
		lexical_prob[(words[j], tags[i])] = float(lst[j])
print lexical_prob


seqscore = [[0 for x in range(no_of_words)] for y in range(N)]
backptr = [[0 for x in range(no_of_words)] for y in range(N)]


 # Initialization step :-
for i in range(0, N):
	seqscore[i][0] = lexical_prob[(words[0], tags[i])] * bigram_prob[(tags[i], 'phi')]
	backptr[i][0] = 0

print '\n', seqscore


# Iteration step :-
for t in range(1, no_of_words):
	for i in range(0, N):
		scores = []
		for j in range(0, N):
			score = seqscore[j][t-1] * bigram_prob[(tags[i], tags[j])]
			#print score, 'one score', bigram_prob[(tags[i], tags[j])], seqscore[j][t-1], j, t-1
			scores.append(score)
			max_index, max_value = max(enumerate(scores), key=operator.itemgetter(1))
			seqscore[i][t] = max_value * lexical_prob[(words[t], tags[i])]
			backptr[i][t] = max_index

print '\n', seqscore


# Sequence identification step :-
c = [0 for x in range(no_of_words)]

max_index = 0
for i in range(1, N):
	if seqscore[i][no_of_words - 1] > seqscore[max_index][no_of_words - 1]:
		max_index = i

c[no_of_words - 1] = max_index

for i in range(no_of_words - 2, -1, -1):
	c[i] = backptr[c[i+1]][i+1]

print c

print words
for i in range(len(c)):
	print tags[c[i]],
