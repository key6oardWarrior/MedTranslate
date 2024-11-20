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

	def init(self) -> None:
		pass

	def find_all_urls(self) -> None:
		pass

	def __get_next_sentences(self) -> list[int]:
		indexes = [self.__text.find(self.__DELIMS[0], self.__prev_idx)]
		indexes.append(self.__text.find(self.__DELIMS[1], self.__prev_idx))
		indexes.append(self.__text.find(self.__DELIMS[2], self.__prev_idx))

		indexes.sort()
		indexes.remove(-1)
		indexes.remove(-1)
		indexes.remove(-1)

		self.__prev_idx += indexes[-1] + 1

	def simple_summary(self, text: str) -> str:
		self.__text = text
		prev_idx: int = -1
		indexes = self.__get_next_sentences()
		paragraph = ""
		cnt = 0
		entire_summary = ""
		ii = 0

		while len(indexes) > 0:
			idx = indexes[ii]
			paragraph += text[prev_idx+1, idx]

			if cnt == 4:
				tokens = self.__pegasus_tokenizer(paragraph, truncation=True, padding="longest", return_tensors=self.__TENSORS)

				encoded_summary = self.__pegasus_model.generate(**tokens)
				decoded_summary: str = self.__pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)

				summarizer = pipeline("summarization", model=MODEL_NAME, tokenizer=self.__pegasus_tokenizer, framework=self.__TENSORS)
				entire_summary += summarizer(paragraph, min_length=30, max_length=150)
				cnt = 0
				paragraph = ""
			else:
				cnt += 1

		return entire_summary
				