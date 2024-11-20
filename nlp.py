from re import search, Match

from transformers import pipeline
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

from const import MODEL_NAME

class NLP:
	__pegasus_tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME)
	__pegasus_model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME)
	__TENSORS = "pt"
	__DELIMS: list[str] = [".", "?", "!"]
	__text: str = None
	__prev_idx: int = 0
	__matches: list[Match[str]] = []

	def init(self) -> None:
		pass

	def __find_all_urls(self) -> None:
		'''
		# Description:
		If there is a URL in the text they must be found so when the next
		sentence is gotten it won't cut off a URL
		'''
		pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		found: Match[str] = search(pattern, self.__text)

		while found != None:
			self.__matches.append(found)
			found = search(pattern, self.__text)

	def __get_next_sentences(self) -> list[int]:
		'''
		# Description:
		Find the next (at most) 3 sentences

		# Returns:
		A list of indexes that are where the sentences are
		'''
		indexes = [self.__text.find(self.__DELIMS[0], self.__prev_idx)] # delim = "."
		indexes.append(self.__text.find(self.__DELIMS[1], self.__prev_idx)) # delim = "?"
		indexes.append(self.__text.find(self.__DELIMS[2], self.__prev_idx)) # delim = "!"

		for match_ in self.__matches: # indexes should not stop at URLs
			match_: Match[str]

			if indexes[0] > -1:
				if((indexes[0] >= match_.start()) and (indexes[0] < match_.end())):
					indexes[0] = self.__text.find(self.__DELIMS[0], match_.end())

			if indexes[1] > -1:
				if((indexes[1] >= match_.start()) and (indexes[1] < match_.end())):
					indexes[1] = self.__text.find(self.__DELIMS[1], match_.end())

		indexes.sort()
		indexes.remove(-1)
		indexes.remove(-1)
		indexes.remove(-1)

		self.__prev_idx += indexes[-1] + 1
		return indexes

	def simple_summary(self) -> str:
		prev_idx: int = -1
		paragraph = ""
		cnt = 0
		entire_summary = ""
		ii = 0
		self.__find_all_urls()
		indexes: list[int] = self.__get_next_sentences()
		size = len(indexes)

		while len(indexes) > 0:
			idx = indexes.pop()
			paragraph += text[prev_idx+1, idx]

			if cnt == 4:
				tokens = self.__pegasus_tokenizer(paragraph, truncation=True, padding="longest", return_tensors=self.__TENSORS)

				encoded_summary = self.__pegasus_model.generate(**tokens)
				decoded_summary: str = self.__pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)

				summarizer = pipeline("summarization", model=MODEL_NAME, tokenizer=self.__pegasus_tokenizer, framework=self.__TENSORS)
				entire_summary += summarizer(paragraph, min_length=30, max_length=150)
				
				cnt = 0
				ii = 0
				paragraph = ""
			else:
				ii += 1
				cnt += 1

				if ii == size-1:
					indexes = self.__get_next_sentences()
					size = len(indexes)

		return entire_summary

	@property
	def text(self, text: str) -> None:
		self.__text = text
