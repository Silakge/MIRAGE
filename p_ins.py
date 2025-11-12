from openai import OpenAI
from config import API_BASE_URL, DEFAULT_MODEL, API_KEY
import json

def analyze_sensitive_words(sentence):
    """
    Analyze sensitive words in a sentence.
    
    Args:
        sentence (str): The sentence to analyze.
        
    Returns:
        str: The most sensitive word extracted from the sentence.
    """
    try:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY
        )

        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a security research assistant specialized in sensitive information detection. Extract only the most sensitive word from the given sentence."},
                {"role": "user", "content": f"I'm going to conduct security research now. First, I need to analyze and extract the most sensitive word in the sentence: {sentence}\n\nInstruction: Output only the single most sensitive word or phrase, nothing else."}
            ],
            temperature=0.1,
            max_tokens=20  # Limit the output length
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error occurred during API interaction: {e}")
        return None

def replace_sensitive_word(sentence, sensitive_word):
    """
    Replace the sensitive word with a placeholder string.
    
    Args:
        sentence (str): The original sentence.
        sensitive_word (str): The sensitive word to replace.
        
    Returns:
        str: The processed sentence.
    """
    if sensitive_word and sensitive_word in sentence:
        return sentence.replace(sensitive_word, "Spiuytrov1")
    return sentence

def process_sentences_from_file(file_path, output_file):
    """
    Read sentences from a file, analyze and replace sensitive words, then save results.
    
    Args:
        file_path (str): Path to the input file.
        output_file (str): Path to the output JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sentences = file.readlines()
        
        processed_data = []
        
        for index, sentence in enumerate(sentences, 1):
            original_sentence = sentence.strip()
            if not original_sentence:  # Skip empty lines
                continue
                
            print(f"Processing sentence {index}: {original_sentence}")
            
            # Analyze the sensitive word
            sensitive_word = analyze_sensitive_words(original_sentence)
            print(f"Extracted sensitive word: {sensitive_word}")
            
            # Validate if the sensitive word exists in the original sentence
            if sensitive_word and sensitive_word not in original_sentence:
                print(f"Warning: The sensitive word '{sensitive_word}' was not found in the original sentence.")
                sensitive_word = None
            
            # Replace the sensitive word
            processed_sentence = replace_sensitive_word(original_sentence, sensitive_word)
            print(f"Processed sentence: {processed_sentence}")
            
            # Build JSON data
            sentence_data = {
                "index": index,
                "original_sentence": original_sentence,
                "processed_sentence": processed_sentence,
                "sensitive_word": sensitive_word if sensitive_word else "No sensitive word detected"
            }
            
            processed_data.append(sentence_data)
            print("-" * 50)
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=2)
        
        print(f"Processing complete! Results saved to {output_file}")
        
        # Save a human-readable text version
        text_output_file = output_file.replace('.json', '_readable.txt')
        with open(text_output_file, 'w', encoding='utf-8') as file:
            for data in processed_data:
                file.write(f"Index: {data['index']}\n")
                file.write(f"Original sentence: {data['original_sentence']}\n")
                file.write(f"Sensitive word: {data['sensitive_word']}\n")
                file.write(f"Processed sentence: {data['processed_sentence']}\n")
                file.write("-" * 50 + "\n")
        
        print(f"Readable format saved to {text_output_file}")
                
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error occurred while processing the file: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "dataset.txt"  # Input file path
    output_file = "process_ins1.json"  # Output JSON file path
    process_sentences_from_file(input_file, output_file)
