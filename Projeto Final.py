#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
PATH = './camara'
docs = []
files = os.listdir(PATH)
for f in files:
    with open(PATH + '/' + f, 'r', encoding='utf-8') as file:
        text = ' '.join(file.read().split('-')[2:])
        docs.append(text)


# In[2]:


import re
from functools import reduce

def process_doc(doc):
    paragraphs = doc.split('\n      ')
    paragraphs[0] = ' '.join(paragraphs[0].split('\n')[1:])
    paragraphs = [re.sub('\s+', ' ', par) for par in paragraphs]
    paragraphs = [re.sub('^\s+', '', par) for par in paragraphs]
    return paragraphs

processed_docs = reduce(lambda x, y: x + y, [process_doc(doc) for doc in docs], [])


# In[3]:


print(len(processed_docs))


# In[4]:


from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()
tokenizer.fit_on_texts(processed_docs)
total_words = len(tokenizer.word_index) + 1


# In[5]:


max_sequence_len = 16

sequences = []
for line in docs:
	token_list = tokenizer.texts_to_sequences([line])[0]
	for i in range(2, len(token_list)):
		n_gram_sequence = token_list[:i+1]
		sequences.append(n_gram_sequence)


# In[6]:


print(len(sequences))


# In[7]:


from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

sequences = pad_sequences(sequences, maxlen=max_sequence_len+1, padding='pre')

X = sequences[:, :-1]
labels = sequences[:, -1]
y = to_categorical(labels, num_classes=total_words)


# In[8]:


# from sklearn.model_selection import train_test_split

# X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.9)
def shuffle(matrix, target, test_proportion):
    ratio = int(matrix.shape[0]/test_proportion) #should be int
    X_train = matrix[ratio:,:]
    X_test =  matrix[:ratio,:]
    Y_train = target[ratio:,:]
    Y_test =  target[:ratio,:]
    return X_train, X_test, Y_train, Y_test

X_train, X_test, y_train, y_test = shuffle(X, y, 6)


# In[9]:


from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

model = Sequential()
model.add(Embedding(total_words, 256, input_length=max_sequence_len))
model.add(Bidirectional(LSTM(128)))
model.add(Dense(total_words, activation='softmax'))

optimizer = Adam(lr=0.01)

model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
print(model.summary())


# In[ ]:


history = model.fit(X_train, y_train, epochs=50, batch_size=1, 
                    validation_data=(X_test, y_test))


# In[ ]:


seed_text = "O PT"
next_words = 100

index_to_word = {index: word for word, index in tokenizer.word_index.items()}

T = 0.9

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')

    probas = model.predict(token_list, verbose=0)
    probas = np.array(probas[0][1:])
    probas = probas ** (1.0 / T)
    probas /= np.sum(probas)
    predicted = np.random.choice(range(1,total_words), p=probas)
    # predicted = model.predict_classes(token_list, verbose=0)[0]
    
    seed_text += " " + (index_to_word[predicted] if predicted != 0 else '')
print(seed_text)


# In[ ]:




