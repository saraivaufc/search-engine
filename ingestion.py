import json
import multiprocessing
from threading import Thread

import pandas as pd
from tqdm import tqdm

from image_utils import TextProcessor
from models import Document, Word

THREADS = multiprocessing.cpu_count() * 2

text_processor = TextProcessor()

all_documents = {}
for document in Document.objects.all():
    all_documents[document.hash] = document

all_words = {}
for word in Word.objects.all():
    all_words[word.text] = word


class WorkerThread(Thread):
    def __init__(self, data_frame, position=0):
        Thread.__init__(self)
        self.data_frame = data_frame
        self.position = position

    def run(self):
        for index, row in tqdm(self.data_frame.iterrows(),
                               total=len(self.data_frame),
                               position=self.position):
            data = dict(zip(self.data_frame.columns, row.to_numpy()))

            sentence = json.dumps(data)

            hash = text_processor.hash(sentence)
            words = text_processor.tokenize(sentence)

            if hash not in all_documents:
                all_documents[hash] = Document(hash=hash,
                                               text=sentence,
                                               words=words)

            for word_text in words:
                if word_text not in all_words:
                    all_words[word_text] = Word(text=word_text)

                if all_documents[hash] not in all_words[word_text].documents:
                    all_words[word_text].documents.append(all_documents[hash])


df = pd.read_csv("data_test.csv", sep=",", encoding="ISO-8859-1")

count = len(df)
batch_size = int(count / THREADS)

print("#" * 100)
print("Total documents: ", count)
print("Cores:", THREADS)
print("Batch:", batch_size)
print("#" * 100)

bar_position = 0
threads = []

for x in range(0, THREADS):
    start = x * batch_size
    end = start + batch_size

    thread = WorkerThread(df[start:end], position=bar_position)
    thread.start()
    threads.append(thread)
    bar_position += 1

for thread in threads:
    thread.join()

for hash in list(all_documents.keys()):
    all_documents[hash].save()

for text in list(all_words.keys()):
    all_words[text].save()
