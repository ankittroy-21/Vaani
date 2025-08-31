import nltk

print("--- Starting NLTK Data Download ---")
packages = ['brown', 'punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4','punkt_tab']

for package in packages:
    print(f"Downloading '{package}'...")
    nltk.download(package)

print("\n--- All required NLTK data has been downloaded. ✅ ---")