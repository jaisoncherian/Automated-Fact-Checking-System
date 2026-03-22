from similarity import check_fact

test_inputs = [
    "india capital is delhi",
    "earth is round",
    "drinking hot water cures covid"
]

for text in test_inputs:
    result, score = check_fact(text)
    print(f"Input: {text}")
    print(f"Result: {result}")
    print(f"Confidence: {score:.4f}")
    print("---")
