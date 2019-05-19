from nltk.corpus import semcor
from nltk.tree import Tree
from nltk.corpus.reader.wordnet import Lemma
from nltk.corpus.reader.wordnet import Synset

from nltk.corpus import wordnet
import copy
import nltk


sent = 'I went to the bank to deposit money' #raw_input()
target_word = 'bank' 				#raw_input()

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


# Context words
context_words = copy.copy(words)
context_words.remove(target_word)
print "Context words : ", context_words


synsets = wordnet.synsets(target_word)				# Synsets of target word
no_of_senses = len(synsets)

tagged_chunks = semcor.tagged_chunks(tag='both')		# SemCor


# Calculating prior probability of each sense and conditional prob (individual feature probability) :-
prior_prob = {}
feature_prob = {}

count = {}
synset_count = {}
feature_count = {}

count_target = 0

for synset in synsets:
	prior_prob[synset] = 0
	count[synset] = 0
	synset_count[synset] = 0
	
window_size = 10
			

for i in range(0, len(tagged_chunks)):
	if tagged_chunks[i].height() == 3 and isinstance(tagged_chunks[i].label(), nltk.corpus.reader.wordnet.Lemma):
		
		synset = tagged_chunks[i].label().synset()
		
		if tagged_chunks[i].leaves()[0] == target_word:
			count_target += 1
			
			if synset in synsets:
				count[synset] += 1
				
		if synset in synsets:
			synset_count[synset] += 1
		
			# Taking 'window size' words forward to current word and incrementing the count for that word's feature count
			cnt = 0
			j = 1
			while cnt != window_size:
				if tagged_chunks[i+j].height() == 3 and isinstance(tagged_chunks[i+j].label(), nltk.corpus.reader.wordnet.Lemma) and tagged_chunks[i+j].leaves()[0].lower() not in stopwords:
					try:
						feature_count[(tagged_chunks[i+j].leaves()[0].lower(), synset)] += 1
					except:
						feature_count[(tagged_chunks[i+j].leaves()[0].lower(), synset)] = 1
					
					cnt += 1
				j += 1
			
			# Taking 'window size' words backward to current word and incrementing the count for that word's feature count
			cnt = 0
			j = 1
			while cnt != window_size:
				if tagged_chunks[i-j].height() == 3 and isinstance(tagged_chunks[i-j].label(), nltk.corpus.reader.wordnet.Lemma) and tagged_chunks[i-j].leaves()[0].lower() not in stopwords:
					try:
						feature_count[(tagged_chunks[i-j].leaves()[0].lower(), synset)] += 1
					except:
						feature_count[(tagged_chunks[i-j].leaves()[0].lower(), synset)] = 1
					
					cnt += 1
				j += 1
									
			'''if (chunk_tree.leaves()[0], synset) in feature_count:
				feature_count[(chunk_tree.leaves()[0], synset)] += 1
			
			else:
				feature_count[(chunk_tree.leaves()[0], synset)] = 1'''


print '\nPrior probabilties :-'
print count_target
print '\n', count

for synset in synsets:			
	prior_prob[synset] = (count[synset] + 1) / float(count_target + no_of_senses)		# To handle zero frequency problem

print '\n', prior_prob


print '\nIndividual feature probabilities :-'
print synset_count
print '\n', feature_count

for key in feature_count:
	(w, synset) = key
	feature_prob[key] = feature_count[key] / float(synset_count[synset])

print '\n', feature_prob


# Disambiguation :-
scores = {}

for synset in synsets:
	score = prior_prob[synset]
		
	for word in context_words:
		try:
			score *= feature_prob[(word, synset)]
		except:
			score *= 0.0001
	
	scores[synset] = score
	
print '\n', 'Scores :\n', scores

max_score = max(scores.values())

synset = ""

for k in scores:
	if scores[k] == max_score:
		synset = k
		break
		
print "\nCorrect sense = ", synset, " - ", synset.definition()
