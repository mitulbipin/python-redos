import regex

# Pattern with timeout
pattern = r'A(B|C+)+D'
text = 'ACCCCCCCCCCCCCCCCCCCABD'

# Calculate an estimated complexity score for the pattern and text
# Here, you can use your own heuristic to determine the complexity
pattern_complexity = len(pattern)
text_length = len(text)

# Set the timeout based on the complexity
timeout = min(1, pattern_complexity * text_length * 0.0001)  # Adjust the multiplier as needed

try:
    # Set timeout for regular expression matching
    match = regex.match(pattern, text, timeout=timeout)
    if match:
        print("Match found:", match.group())
    else:
        print("No match found")
except regex.TimeoutError:
    print("Regex matching timed out")
