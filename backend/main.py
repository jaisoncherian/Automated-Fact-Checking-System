from similarity import check_fact

text = input("Enter news: ")

result, score = check_fact(text)

print("Result:", result)
print("Confidence:", score)
