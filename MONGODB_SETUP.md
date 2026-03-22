# MongoDB Setup Instructions

## Prerequisites

1. **Install MongoDB**
   - Download from: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (Cloud): https://www.mongodb.com/cloud/atlas

2. **For Local MongoDB:**
   - Install MongoDB Community Edition
   - Start the MongoDB service:
     ```
     mongod
     ```
   - Default connection string: `mongodb://localhost:27017/`

3. **For MongoDB Atlas (Cloud):**
   - Create a cluster at https://www.mongodb.com/cloud/atlas
   - Get your connection string from the cluster
   - Update `backend/db.py` with your connection string:
     ```python
     client = MongoClient("YOUR_CONNECTION_STRING_HERE")
     ```

## Setup Steps

1. **Insert sample facts into database:**
   ```
   python backend/insert_data.py
   ```

2. **Run the fact-checker:**
   ```
   python backend/main.py
   ```

## How It Works

- **db.py** - Connects to MongoDB and manages the database connection
- **insert_data.py** - Inserts sample facts into the database (run this once)
- **similarity.py** - Now fetches facts from MongoDB instead of static list
- **main.py** - Interactive interface (unchanged)

## Expected Output

After inserting data, when you run `main.py`:
```
Enter news: india capital is delhi
Result: true
Confidence: 0.9876
```

Your system is now connected to a real database! 🚀
