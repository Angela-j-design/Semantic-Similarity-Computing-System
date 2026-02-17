import math

def norm(vec):
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    numerator = 0
    for word in vec1:
        if word in vec2:
            numerator += vec1[word] * vec2[word]

    mag1 = 0
    mag2 = 0
    for v in vec1.values():
        mag1 += v * v
    for v in vec2.values():
        mag2 += v * v

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return numerator / math.sqrt(mag1 * mag2)

def build_semantic_descriptors(sentences):
    dic = {}
    for sentence in sentences:
        for w in sentence:
            if w not in dic:
                dic[w] = {}
            for other_word in sentence:
                if other_word != w:
                    dic[w][other_word] = dic[w].get(other_word, 0) + 1
    return dic

def build_semantic_descriptors_from_files(filenames):
    text = ""
    for filename in filenames:
        with open(filename, "r", encoding="latin1") as f:
            text += f.read() + " "

    text = text.lower()
    text = text.replace("!", ".").replace("?", ".")
    sentences = text.split(".")

    processed_sentences = []
    punctuation_to_remove = [",", "-", "--", ":", ";"]

    for sentence in sentences:
        for punct in punctuation_to_remove:
            sentence = sentence.replace(punct, " ")
        words = sentence.split()
        if words:
            processed_sentences.append(words)

    return build_semantic_descriptors(processed_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]

    max_similarity = -1
    best_choice = choices[0]

    for choice in choices:
        if choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word],
                                       semantic_descriptors[choice])
        else:
            similarity = -1

        if similarity > max_similarity:
            max_similarity = similarity
            best_choice = choice

    return best_choice
