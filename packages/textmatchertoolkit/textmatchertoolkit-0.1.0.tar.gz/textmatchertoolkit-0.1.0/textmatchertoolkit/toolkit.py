import warnings
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import spacy
from numpy import dot
from numpy.linalg import norm
import re
import collections
from math import log2
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk
import pandas as pd
import string

nltk.download('stopwords')
warnings.filterwarnings("ignore")


class Utility:
    def __init__(self):
      self.nlp=spacy.load('en_core_web_sm')
      self.stopwords = self.nlp.Defaults.stop_words
      self.vectorizer = TfidfVectorizer(stop_words=list(self.stopwords))

    def remove_links(self,text):
      url_pattern = r"http\S+|www\S+"
      return re.sub(url_pattern, "", text)

    def to_lowercase(self,text):
        if isinstance(text, str):
            return text.lower()
        else:
            return text

    def remove_mentions_and_tags(self,text):
        text = re.sub(r'@\S*', '', text)
        return re.sub(r'#\S*', '', text)

    def lemmatize(self,text):
      doc = self.nlp(text)
      lemmatized_text = []
      for token in doc:
        lemmatized_text.append(token.lemma_)
      return ' '.join(lemmatized_text)

    def keep_only_alphabet(self,text):
      return re.sub(r'[^a-z]', ' ', text)

    def reshape_topic_output(self,dictionary):
      output_dict={}
      for i in range(0,9):
        output_dict[dictionary['labels'][i]]=dictionary['scores'][i]
      return collections.OrderedDict(sorted(output_dict.items()))

    def kl_divergence(self,p, q):
      return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))

    def calculate_pos_tagging(self,text):
      return [token.pos_ for token in self.nlp(text)]

    def compute_tfidf_matrix(self,corpus):
      corpus=map(self.remove_links,corpus)
      corpus=map(self.remove_mentions_and_tags,corpus)
      corpus=map(self.to_lowercase,corpus)
      corpus=map(self.keep_only_alphabet,corpus)
      corpus=list(map(self.lemmatize,corpus))
      res=self.vectorizer.fit_transform(corpus)
      feature_names=self.vectorizer.get_feature_names_out()
      return res,feature_names


    def add_row_to_dataframe(self,df, new_data):
      df.loc[len(df.index)] = new_data
      return df



class Matcher():
  def __init__(self):
    self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    self.similarity_model=SentenceTransformer('sentence-transformers/all-distilroberta-v1').to(self.device)
    self.topic_model=pipeline("zero-shot-classification",model="valhalla/distilbart-mnli-12-1",device=0)#device=0
    self.candidate_topic_labels = ["Sports","Technology","Politics","Fashion","Health_Fitness","Travel","Business_Finance","Science_Education","Social_Issues"]
    self.utility=Utility()
    self.paraphrase_model=AutoModelForSequenceClassification.from_pretrained("Prompsit/paraphrase-bert-en").to(self.device)
    self.paraphrase_tokenizer=AutoTokenizer.from_pretrained("Prompsit/paraphrase-bert-en")
    self.entailment_model=pipeline("text-classification",model="geckos/bart-fined-tuned-on-entailment-classification",tokenizer="geckos/bart-fined-tuned-on-entailment-classification",return_all_scores=True,device=0)#device=0
    #self.vectorizer = TfidfVectorizer()
    self.subjectivity_model=pipeline(task="text-classification",model="cffl/bert-base-styleclassification-subjective-neutral",return_all_scores=True,device=0)#device=0

  def compute_similarity(self,text1,text2):
    couple=(text1,text2)
    embeddings = self.similarity_model.encode(couple)
    cos_sim = dot(embeddings[0], embeddings[1])/(norm(embeddings[0])*norm(embeddings[1]))
    return cos_sim

  def compute_topic_coherence(self,sentence1,sentence2):
    t1=self.utility.remove_mentions_and_tags(self.utility.remove_links(sentence1))
    t2=self.utility.remove_mentions_and_tags(self.utility.remove_links(sentence2))
    dist_t1=self.topic_model(t1, self.candidate_topic_labels)
    dist_t2=self.topic_model(t2, self.candidate_topic_labels)
    dist_t1=self.utility.reshape_topic_output(dist_t1)
    dist_t2=self.utility.reshape_topic_output(dist_t2)
    return self.utility.kl_divergence(list(dist_t1.values()),list(dist_t2.values()))

  def compute_paraphrase(self,sentence1,sentence2):
    input = self.paraphrase_tokenizer(sentence1,sentence2,return_tensors='pt').to(self.device)
    logits = self.paraphrase_model(**input).logits
    soft = torch.nn.Softmax(dim=1)
    result=soft(logits).tolist()[0]
    return result[1]

  def compute_entailment(self,sentence1,sentence2):
    desired_score=0
    full_text=" "
    if sentence1.endswith('.'):
      full_text=sentence1+" "+sentence2
    else:
      full_text=sentence1+". "+sentence2
    res=self.entailment_model(full_text)[0]
    for item in res:
      if item['label'] == "entailment":
        desired_score = item['score']
        break
    return desired_score


  def compute_positional_distance(self,sentence1,sentence2):
    return Levenshtein.distance(self.utility.calculate_pos_tagging(sentence1),self.utility.calculate_pos_tagging(sentence2))

  def compute_tfidf_similarity(self,sentence1,sentence2,vectorizer_):
    t1=self.utility.lemmatize(self.utility.keep_only_alphabet(self.utility.to_lowercase(self.utility.remove_mentions_and_tags(self.utility.remove_links(sentence1)))))
    t2=self.utility.lemmatize(self.utility.keep_only_alphabet(self.utility.to_lowercase(self.utility.remove_mentions_and_tags(self.utility.remove_links(sentence2)))))
    t1_vector = vectorizer_.transform([t1]).toarray()
    t2_vector = vectorizer_.transform([t2]).toarray()
    similarity = cosine_similarity(t1_vector, t2_vector)
    return similarity[0][0]

  def compute_subjectivity(self, sentence):
    res=self.subjectivity_model(sentence)
    if res[0][0]['label']=='SUBJECTIVE':
      return res[0][0]['score']
    else:
      return res[0][1]['score']
