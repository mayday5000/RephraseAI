from typing import Any, Dict, List, Optional, Iterable
import fire, re
from llama.generation import Llama, Dialog, ChatPrediction

class RephraseAI:
    def __init__(
              self, 
              ckpt_dir: str, 
              tokenizer_path: str,
              temperature: float, 
              top_p: float, 
              max_seq_len: int,
              max_batch_size: int,
              max_gen_len: int,
              ):
        self.ckpt_dir = ckpt_dir
        self.tokenizer_path = tokenizer_path
        self.temperature = temperature
        self.top_p = top_p
        self.max_seq_len = max_seq_len
        self.max_batch_size = max_batch_size
        self.max_gen_len = max_gen_len

        self.generator = Llama.build(
            ckpt_dir=self.ckpt_dir,
            tokenizer_path=self.tokenizer_path,
            max_seq_len=self.max_seq_len,
            max_batch_size=self.max_batch_size,
        )

    def chat_completion(self, dialogs :List[Dialog]) -> List[ChatPrediction]:
        return self.generator.chat_completion(
            [dialogs],  # type: ignore
            max_gen_len=self.max_gen_len,
            temperature=self.temperature,
            top_p=self.top_p,
        )

    def parse_synonyms(self, dialogs :List[Dialog], results :List[ChatPrediction]) -> Dict[str, List[str]]:
        message :str = ""
        synonyms :Dict[str, List[str]] = {}

        for dialog, result in zip(dialogs, results):
            message = message + f"{result['generation']['content']}\n"
            message = message.replace('\"', '')

            fg_next_line = False
            word = ""
            lines = message.lower().split('\n')
            for line in lines:
                if line == '':
                    continue

                splitted=re.split('\d+\\.' ,line)
                if len(splitted) > 1:
                    fg_next_line = False

                if fg_next_line == True:
                    splitted = line.split(' ')
                    if len(splitted) > 1:
                            synonyms_list.append(splitted[1].strip())
                            current_word = {word: synonyms_list}
                            synonyms.update(current_word)
                    else:
                        fg_next_line = False                    
                else:
                    splitted=re.split('\\.|\\:', line)
                    if len(splitted) > 1:
                        splitted = re.split('\\:|\\-', splitted[1])
                        if len(splitted[0]) > 0:
                            word = splitted[0].strip()
                        
                            if len(splitted) > 1:
                                synonyms_list = splitted[1].split(',')
                                current_word = {word: synonyms_list}
                                synonyms.update(current_word)
                                fg_next_line = False
                            else:
                                synonyms_list = []
                                fg_next_line = True

        return synonyms
    
    def parse_rephrase(self, dialogs :List[Dialog], results :List[ChatPrediction]) -> List[str]:
        message :str = ""
        rephrase = ""
        end_of_query = "I hope these suggestions are helpful! Let me know if you have any other questions"
        rephrase_list = []

        for dialog, result in zip(dialogs, results):
            message = message + f"{result['generation']['content']}\n"
            message = message.replace('\"', '')
            lines = message.split('\n')

            line_number = 0
            for line in lines:
                line_number = line_number + 1
                if line_number > 1 and len(line) > 2:
                    rephrase = line.replace('\"', '')
                    idx = rephrase.find(". ")
                    if idx >= 0:
                        rephrase = rephrase[idx+2:]
                    idx = rephrase.find("* ")
                    if idx >= 0:
                        rephrase = rephrase[idx+2:]
                    idx = rephrase.find("- ")
                    if idx >= 0:
                        rephrase = rephrase[idx+2:]                        

                    if rephrase[-1] != '.':
                        rephrase = rephrase + '.'

                    if rephrase.find(end_of_query) < 0:
                        rephrase_list.append(rephrase)
                else:
                    if len(rephrase_list) > 0:
                        break

        return rephrase_list

    def get_phrases_with_synonyms(self, phrase :str, max_synonyms_per_word: int = 3) -> List[str]:
        dialogs = []

        phrase = phrase.lower()
        message = "Given the following phrase give me some synonyms of each word. The phrase is: " + "\""+ phrase +"\""
        dialogs.append({"role": "user", "content": message})

        response = self.chat_completion(dialogs)
        synonyms = self.parse_synonyms(dialogs, response)

        new_phrases = []
        for key in synonyms.keys():
            synonym_count = 0
            for value in synonyms[key]:
                if synonym_count == max_synonyms_per_word:
                    break
                new_phrases.append(phrase.replace(key, value.strip()))
                synonym_count = synonym_count + 1

        return new_phrases
    
    def get_rephrases(self, phrase :str, max_synonyms_per_word: int = 3) -> Iterable[str]:
        rephrase = ""
        input_phrases = []

        phrase = phrase.replace('\"', '').replace('\n', '').replace('\t', '').replace('\'', '')
        if len(phrase) < 3:
            return "Error: There is no text in this sentence."
        
        input_phrases = self.get_phrases_with_synonyms(phrase=phrase, max_synonyms_per_word=max_synonyms_per_word)

        if len(input_phrases) == 0:
            input_phrases.append(phrase)

        for input_phrase in input_phrases:
            dialogs = []
            message = "Could you rephrase the following phrase: " + "\""+ input_phrase +"\""
            dialogs.append({"role": "user", "content": message})

            response = self.chat_completion(dialogs)
            rephrase_list = self.parse_rephrase(dialogs, response)
            for rephrase in rephrase_list:        
                yield rephrase

def main(
    ckpt_dir: Optional[str] = "llama-2-7b-chat/", 
    tokenizer_path: Optional[str] = "tokenizer.model",
    temperature: Optional[float] = 0.6, 
    top_p: Optional[float] = 0.9, 
    max_seq_len: Optional[int] = 512,
    max_batch_size: Optional[int] = 4,
    max_gen_len: Optional[int] = None,
):
    chat = RephraseAI(
        ckpt_dir=ckpt_dir, 
        tokenizer_path=tokenizer_path, 
        temperature=temperature,
        top_p=top_p,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
        max_gen_len=max_gen_len
        )

    max_synonyms_per_word = 1
    while True:
        print("\nType 'exit' or 'quit' to exit.\n")
        prompt = input("\n🦙 Enter an english phrase: ")
        if prompt.lower() == "exit" or prompt.lower() == "quit":
            break
        for phrase in chat.get_rephrases(prompt, max_synonyms_per_word):
            print("\n💬 [Rephrase] ------------> ", phrase)  
 
if __name__ == "__main__":
    fire.Fire(main)
