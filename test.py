# import regex
import re,time
# Pattern with timeout
pattern = r'^(.*)/(\d+)\.?(\d+)?.?(\d+)?.?(\d+)? CFNetwork'
text = '/0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

compiled_pattern = re.compile(pattern)

start_time = time.time()
print(compiled_pattern.match(text))
end_time = time.time()

print(f"Time taken: {end_time-start_time}")