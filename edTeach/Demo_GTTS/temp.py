import json

text = """```json
{
  "q1": "What type of sequence is presented in the paragraph?",
  "q1_a": "Arithmetic sequence",
  "q1_b": "Geometric sequence",
  "q1_c": "Fibonacci sequence",
  "q1_d": "Random sequence",
  "q2": "What is the starting number of the sequence?",
  "q2_a": "0",
  "q2_b": "1",
  "q2_c": "21",
  "q2_d": "30",
  "q3": "What is the common difference between consecutive numbers in the sequence?",
  "q3_a": "1",
  "q3_b": "-1",
  "q3_c": "10",
  "q3_d": "-10",
  "q4": "How many numbers are in the sequence?",
  "q4_a": "29",
  "q4_b": "30",
  "q4_c": "31",
  "q4_d": "32",
  "q5": "What is the last number of the sequence?",
  "q5_a": "1",
  "q5_b": "0",
  "q5_c": "30",
  "q5_d": "29",
  "answers": {
    "q1": "q1_a",
    "q2": "q2_d",
    "q3": "q3_b",
    "q4": "q4_c",
    "q5": "q5_b"
  }
}
```"""

def extract_substring(input_string):
    start_index = input_string.find('{')  # Find the index of the first occurrence of '{'
    if start_index == -1:  # If '{' is not found, return None
        return None
    
    # Reverse the string after the first '{'
    reversed_string = input_string[start_index+1:][::-1]
    
    # Find the index of the first occurrence of '}' in the reversed string
    end_index_reversed = reversed_string.find('}')
    
    if end_index_reversed == -1:  # If '}' is not found after the first '{', return None
        return None
    
    # Calculate the index of '}' in the original string
    end_index = len(input_string) - end_index_reversed - 1
    
    return input_string[start_index+1:end_index]  # Extract the substring between the first '{' and the matching '}'

# Example usage:
input_string = text
substring = extract_substring(input_string)
print(substring)  # Output: "this is the substring"
