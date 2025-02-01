import streamlit as st
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import pos_tag
from nltk.tokenize.treebank import TreebankWordDetokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
import re

# Download stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load the spaCy English model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# Custom stopwords to filter out more irrelevant words
CUSTOM_STOPWORDS = set(stopwords.words('english')).union({
    'to', 'of', 'and', 'the', 'in', 'for', 'on', 'with', 'a', 'that', 'by', 'or', 'an', 'as', 'at', 'it', 'this', 'be', 'which'
})

# Function to extract keywords using NLTK and spaCy
def extract_keywords_nltk_spacy(job_description):
    # Tokenize the job description
    word_tokens = word_tokenize(job_description.lower())
    
    # Remove punctuation and non-alphabetic tokens
    word_tokens = [word for word in word_tokens if word.isalpha()]
    
    # Remove stopwords
    filtered_words = [word for word in word_tokens if word not in CUSTOM_STOPWORDS]
    
    # POS tagging
    tagged_words = pos_tag(filtered_words)
    
    # Extract keywords - focus on nouns and adjectives
    keywords = [word for word, pos in tagged_words if pos in ['NN', 'NNS', 'NNP', 'JJ', 'JJS']]
    
    # Use spaCy for Named Entity Recognition (NER) to extract entities like company names, positions, etc.
    doc = nlp(' '.join(filtered_words))
    ner_keywords = [ent.text.lower() for ent in doc.ents]
    
    # Combine NER keywords and POS-tagged keywords
    combined_keywords = keywords + ner_keywords
    
    # Frequency Distribution of the keywords
    freq_dist = FreqDist(combined_keywords)
    
    # Filter out low frequency words, with a higher threshold
    min_freq = 3  # Set a minimum frequency threshold
    filtered_keywords = [word for word, freq in freq_dist.items() if freq >= min_freq]
    
    return filtered_keywords, freq_dist

# Streamlit App Layout
def main():
    st.title("Job Description Keyword Extractor")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your Job Description (PDF)", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        job_description = extract_pdf_text(uploaded_file)
        st.text_area("Job Description", job_description, height=300)
        
        # Extract relevant keywords from the job description
        if job_description:
            keywords, freq_dist = extract_keywords_nltk_spacy(job_description)
            
            # Show the extracted keywords
            st.write("### Extracted Keywords:")
            st.write(keywords)
            
            # Show WordCloud based on frequency distribution
            st.write("### Word Cloud of Extracted Keywords:")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dist)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.pyplot(plt)
            
            # Display frequency distribution as a bar chart
            st.write("### Frequency Distribution of Keywords:")
            st.bar_chart(freq_dist)

if __name__ == '__main__':
    main()
