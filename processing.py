import os
from multiprocessing import Process, Queue


def search_in_file(file_path, keywords, queue):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().lower()

        found = {word: text.count(word.lower()) for word in keywords if word in text}
        queue.put((file_path, found))


def main():
    folder = "files"
    keywords = ["Python", "process", "class"]

    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".txt")]

    queue = Queue()
    processes = []

    for file_path in files:
        p = Process(target=search_in_file, args=(file_path, keywords, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    results = {}
    while not queue.empty():
        file_path, data = queue.get()
        results[file_path] = data

    print("Results:")
    for file, res in results.items():
        print(f"{file}: {res}")


if __name__ == "__main__":
    main()
