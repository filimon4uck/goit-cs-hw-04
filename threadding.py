import os
import threading


def search_in_file(file_path, keywords, results, lock):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()
        found = {
            word: text.count(word.lower()) for word in keywords if word.lower() in text
        }

        with lock:
            results[file_path] = found


def main():
    folder = "files"
    keywords = ["Python", "thread", "class"]

    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".txt")]

    results = {}
    lock = threading.Lock()
    threads = []

    for file_path in files:
        t = threading.Thread(
            target=search_in_file, args=(file_path, keywords, results, lock)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Results:")
    for file, res in results.items():
        print(f"{file}: {res}")


if __name__ == "__main__":
    main()
