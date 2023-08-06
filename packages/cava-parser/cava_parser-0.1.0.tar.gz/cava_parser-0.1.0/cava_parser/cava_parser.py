from transformers import pipeline

class matcher():
  def __init__(self):
    self.topic_model=pipeline("zero-shot-classification",model="valhalla/distilbart-mnli-12-1")#device=0
    self.candidate_topic_labels=candidate_labels = ["Sports","Technology","Politics","Fashion","Health_Fitness","Travel","Business_Finance","Science_Education","Social_Issues"]

  def compute_topic_coherence(self,sentence1):
    return self.topic_model(sentence1, self.candidate_topic_labels)
