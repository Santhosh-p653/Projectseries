import os
import urllib.request

DATA_DIR = "data"
FILE_NAME = "AmesHousing.csv"
LOCAL_PATH = os.path.join(DATA_DIR, FILE_NAME)

# Using Inria's official, highly stable scikit-learn training repository URL
URL = "https://raw.githubusercontent.com/INRIA/scikit-learn-mooc/main/datasets/house_prices.csv"

def download_dataset():
    if not os.path.exists(DATA_DIR):
        print(f"Creating directory: '{DATA_DIR}'...")
        os.makedirs(DATA_DIR)
        
    print("Downloading dataset from official Inria source...")
    try:
        req = urllib.request.Request(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(LOCAL_PATH, 'wb') as out_file:
            out_file.write(response.read())
        print(f"\n✅ Success! Dataset saved safely to: {LOCAL_PATH}")
    except Exception as e:
        print(f"\n❌ Failed to download dataset. Error: {e}")

if __name__ == "__main__":
    download_dataset()
