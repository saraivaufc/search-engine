from tqdm import tqdm

from image_utils import TextProcessor
from models import Document, Word

text_processor = TextProcessor()

while True:
    query_text = input("Search:")

    query_hash = text_processor.hash(query_text)
    query_words = text_processor.tokenize(query_text)

    print("Words:", query_words)

    query_document = Document(hash=query_hash,
                              text=query_text,
                              words=query_words)

    documents = []
    for word_text in query_document.words:
        word = Word.objects(text=word_text).first()
        if not word:
            print("Word {word} not found!".format(word=word_text))
            continue

        print("[{word}] - {count} documents found.".format(
            word=word_text, count=len(word.documents)))

        documents.extend(word.documents)

    documents = set(documents)

    top_documents = []
    for document in tqdm(documents, total=len(documents)):
        sim_document_query = text_processor.calc_sim(document,
                                                     query_document)
        if sim_document_query > 0:
            top_documents.append([sim_document_query, document.text])

    top_documents = sorted(top_documents, reverse=True)[:10]
    for index, document in enumerate(top_documents):
        print(index, ":", document[1][:1000], "Similarity: ", document[0],
              "\n")
