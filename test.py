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

# @app.route('/regex_injection', methods=['GET', 'POST'])
# def regex_injection():
# message = None
# if request.method == 'POST':
#     string = request.form.get('string')
#     if string:
#         queue = Queue()
#         p = Process(target=search, args=(string, queue))
#         p.start()
#         p.join(2)  # Wait for 1 second
#         if p.is_alive():
#             p.terminate()
#             p.join()
#             response = make_response(render_template('timeout.html', message='500 Internal Server Error'), 500)
#         else:
#             result = queue.get()
#             if result:
#                 response = make_response(render_template('timeout.html', message='200 OK'), 200)
#             else:
#                 response = make_response(render_template('timeout.html', message='400 Bad Request'), 400)
#         return response
# return render_template('timeout.html', message=message)
