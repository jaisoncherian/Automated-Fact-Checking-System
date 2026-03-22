from db import collection

# Insert sample data into MongoDB with diverse facts
data = [
    {"claim": "india capital is new delhi", "label": "true"},
    {"claim": "earth is flat", "label": "false"},
    {"claim": "sun rises in the east", "label": "true"},
    {"claim": "humans can breathe in space without equipment", "label": "false"},
    {"claim": "water boils at 100 degrees celsius", "label": "true"},
    {"claim": "covid 19 can be cured by drinking hot water", "label": "false"},
    {"claim": "the moon is a planet", "label": "false"},
    {"claim": "the earth revolves around the sun", "label": "true"},
    {"claim": "vaccines cause autism", "label": "false"},
    {"claim": "light travels faster than sound", "label": "true"},
    
    {"claim": "humans have three hearts", "label": "false"},
    {"claim": "the human body has 206 bones", "label": "true"},
    {"claim": "plants need sunlight to grow", "label": "true"},
    {"claim": "gold is heavier than silver", "label": "true"},
    {"claim": "the great wall of china is visible from space", "label": "false"},
    
    {"claim": "fish can live without water", "label": "false"},
    {"claim": "electricity flows through conductors", "label": "true"},
    {"claim": "the brain is the largest organ in the human body", "label": "false"},
    {"claim": "the heart pumps blood throughout the body", "label": "true"},
    {"claim": "sound travels in vacuum", "label": "false"},
    
    {"claim": "india is in asia", "label": "true"},
    {"claim": "the pacific ocean is the largest ocean", "label": "true"},
    {"claim": "mount everest is the tallest mountain", "label": "true"},
    {"claim": "the nile is the longest river", "label": "true"},
    {"claim": "a day has 30 hours", "label": "false"},
    
    {"claim": "the sun is a star", "label": "true"},
    {"claim": "earth has two moons", "label": "false"},
    {"claim": "gravity pulls objects toward the earth", "label": "true"},
    {"claim": "fire is cold", "label": "false"},
    {"claim": "oxygen is necessary for human survival", "label": "true"},
    
    {"claim": "dogs can fly naturally", "label": "false"},
    {"claim": "birds can fly", "label": "true"},
    {"claim": "penguins can fly", "label": "false"},
    {"claim": "whales are mammals", "label": "true"},
    {"claim": "sharks are mammals", "label": "false"},
    
    {"claim": "python is a programming language", "label": "true"},
    {"claim": "java is used only for web development", "label": "false"},
    {"claim": "html is a programming language", "label": "false"},
    {"claim": "css is used for styling web pages", "label": "true"},
    {"claim": "ai stands for artificial intelligence", "label": "true"},
    
    {"claim": "blockchain is a type of database", "label": "true"},
    {"claim": "internet works without servers", "label": "false"},
    {"claim": "cloud computing stores data online", "label": "true"},
    {"claim": "wifi works without electricity", "label": "false"},
    {"claim": "binary uses only 0 and 1", "label": "true"},
    
    {"claim": "the speed of light is constant", "label": "true"},
    {"claim": "time travel to the past is proven possible", "label": "false"},
    {"claim": "atoms are the smallest unit of matter", "label": "true"},
    {"claim": "humans can live without sleep", "label": "false"},
    {"claim": "the earth is the center of the universe", "label": "false"}
]

# Clear existing data
collection.delete_many({})

# Insert new data
result = collection.insert_many(data)
print(f"✓ Inserted {len(result.inserted_ids)} facts into MongoDB")
print("✅ Fact database initialized with threshold-based logic!")
print("\nThreshold Logic:")
print("  └─ Score >= 0.75: Returns TRUE/FALSE (confident)")
print("  └─ Score 0.50-0.75: Returns SUSPICIOUS (uncertain)")
print("  └─ Score < 0.50: Returns UNKNOWN (no match)")
