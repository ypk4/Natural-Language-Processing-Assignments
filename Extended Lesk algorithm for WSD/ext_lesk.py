import nltk
from nltk.corpus import wordnet
import copy

#print "Enter sentence : "
sent = 'I went to bank to withdraw money' #raw_input()

#print "Enter target word : "
target_word = 'bank' #raw_input()

sent_words = sent.split()

if target_word not in sent_words:
	print "Error : Target word is not in the sentence"
	exit()


# Building stopword list :-
f = open('stopword', 'r')
stopwords = f.readlines()

for i in range(0, len(stopwords)):
	stopwords[i] = stopwords[i].strip()

# Removing stopwords :-
words = copy.copy(sent_words)

for w in sent_words:
	for sw in stopwords:
		if w.lower() == sw:
			words.remove(w)
			break
			
print 'After stopword removal : ', words

#index = words.index(target_word)
#print "Index of target word = ", index

context_words = copy.copy(words)
context_words.remove(target_word)
print "Context words : ", context_words


# Extended Lesk WSD :-

synsets = wordnet.synsets(target_word)

scores = []

# Building gloss of all senses of that context word
print "\nBuilding glosses of all senses of context words ...\n"
cw_glosses = {}

for context_word in context_words:
	cw_synsets = wordnet.synsets(context_word)
	print len(cw_synsets), "Synsets for context word :- ", context_word
	cw_gloss = ""
		
	for cw_synset in cw_synsets:
		cw_gloss = cw_gloss + " " + cw_synset.definition()
		
	print '\n', cw_gloss, '\n'
	
	cw_gloss = cw_gloss.split()
	
	# Removing stopwords :-
	cw_gloss_copy = copy.copy(cw_gloss)

	for w in cw_gloss:
		for sw in stopwords:
			if w.lower() == sw:
				cw_gloss_copy.remove(w)
				break
	
	cw_glosses[context_word] = set(cw_gloss_copy)
	
print "Glosses of context words :- ", cw_glosses

	
# WSD	
for synset in synsets:
	score = 0
	synset_gloss = synset.definition()
	synset_gloss = set(synset_gloss.split())
	
	hyponyms = synset.hyponyms()
	
	hypernyms = synset.hypernyms()
	
	# Removing stopwords in synset_gloss :-
	synset_gloss_copy = copy.copy(synset_gloss)

	for w in synset_gloss:
		for sw in stopwords:
			if w.lower() == sw:
				synset_gloss_copy.remove(w)
				break

	# WSD :-		
	for context_word in context_words:
		# Overlap with gloss
		intersec = cw_glosses[context_word].intersection(synset_gloss_copy)
		score += len(intersec)		
		
		# Hyponyms
		for hyponym in hyponyms:
			hypo_gloss = hyponym.definition()
			hypo_gloss = set(hypo_gloss.split())
			
			# Removing stopwords in hypo_gloss :-
			hypo_gloss_copy = copy.copy(hypo_gloss)

			for w in hypo_gloss:
				for sw in stopwords:
					if w.lower() == sw:
						hypo_gloss_copy.remove(w)
						break
			
			# Overlap with hyponym
			intersec = cw_glosses[context_word].intersection(hypo_gloss_copy)
			score += len(intersec)		
		
		# Hypernyms
		for hypernym in hypernyms:
			hyper_gloss = hypernym.definition()
			hyper_gloss = set(hyper_gloss.split())
			
			# Removing stopwords in hyper_gloss :-
			hyper_gloss_copy = copy.copy(hyper_gloss)

			for w in hyper_gloss:
				for sw in stopwords:
					if w.lower() == sw:
						hyper_gloss_copy.remove(w)
						break
			
			# Overlap with hypernym
			intersec = cw_glosses[context_word].intersection(hyper_gloss_copy)
			score += len(intersec)		
								
	scores.append(score)
	
print "\nScores :- ", scores
	
max_index = scores.index(max(scores))

print "\nThe relevant sense for target word is ", synsets[max_index], '-', synsets[max_index].definition()

