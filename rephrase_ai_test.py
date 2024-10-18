import pytest
from rephrase_ai import RephraseAI

def test_chat():
    chat = RephraseAI(
        ckpt_dir= "llama-2-7b-chat/", 
        tokenizer_path= "tokenizer.model",
        temperature = 0.6, 
        top_p = 0.9, 
        max_seq_len = 512,
        max_batch_size = 4,
        max_gen_len = None
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
    test_chat()

pytest.main()    
