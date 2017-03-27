import RAKE

default_stopwords_file = "/home/sindhu/upwork/code_assist_python/src/stopwords/SmartStoplist.txt"
class KeywordsExtractor:
	def __init__(self, stopwords_file = default_stopwords_file):
		if not stopwords_file:
			stopwords_file = default_stopwords_file
		self.Rake = RAKE.Rake(stopwords_file)

	def get_keywords(self, text_str):
		kws = self.Rake.run(text_str)
		#TODO: value sorting? 
		return [x[0] for x in kws]
