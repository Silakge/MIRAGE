import json
import random

def add_specific_pattern(word):
    """
    Add a specific pattern of symbols: add * after each character,
    and insert & in the middle of the word.
    
    Args:
        word (str): The original word
        
    Returns:
        str: The word after adding symbols
    """
    if not word or word == "No sensitive word detected":
        return word
    
    chars = list(word)
    processed_chars = []
    
    for i, char in enumerate(chars):
        processed_chars.append(char)
        
        # Add * after each character
        if i < len(chars) - 1:
            processed_chars.append('*')
        
        # Insert & in the middle of the word
        if i == len(chars) // 2 - 1:
            processed_chars.append('&')
    
    return ''.join(processed_chars)

def process_sensitive_words(input_file, output_file):
    """
    Process sensitive words by adding a specific pattern of symbols.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for item in data:
            original_word = item['sensitive_word']
            processed_word = add_specific_pattern(original_word)
            item['processed_word'] = processed_word
            
            print(f"Original sensitive word: {original_word}")
            print(f"Processed sensitive word: {processed_word}")
            print("-" * 30)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print(f"Processing complete! Results saved to {output_file}")
                
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
    except Exception as e:
        print(f"Error occurred while processing the file: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "process_ins1.json"
    output_file = "process_ins1.json"
    process_sensitive_words(input_file, output_file)
