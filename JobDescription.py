# app.py
import spacy
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Load SpaCy's pre-trained model
nlp = spacy.load("en_core_web_sm")

# Predefined lists for categorizing skills
technical_skills = ['python', 'sql', 'aws', 'django', 'tensorflow', 'java', 'html', 'css', 'javascript', 'r', 'node.js']
soft_skills = ['communication', 'leadership', 'teamwork', 'problem-solving', 'creativity', 'adaptability', 'time management', 'collaboration']
certifications = ['pmp', 'aws certified', 'certified scrum master', 'google analytics', 'data science certification', 'project management certification']

def extract_keywords(job_description):
    """
    Extracts important keywords (nouns & proper nouns) from a job description.
    Filters out stopwords and common terms.
    """
    doc = nlp(job_description)
    keywords = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]
    keyword_frequency = Counter(keywords)
    return keyword_frequency.most_common()

def categorize_keywords(keywords):
    """
    Categorizes keywords into Technical Skills, Soft Skills, and Certifications.
    """
    categorized = {
        'Technical Skills': [],
        'Soft Skills': [],
        'Certifications': []
    }
    
    for keyword, _ in keywords:
        if keyword in technical_skills:
            categorized['Technical Skills'].append(keyword.capitalize())
        elif keyword in soft_skills:
            categorized['Soft Skills'].append(keyword.capitalize())
        elif keyword in certifications:
            categorized['Certifications'].append(keyword.capitalize())
    
    return categorized

def generate_wordcloud(keywords):
    """
    Generates a word cloud from the extracted keywords.
    """
    word_freq = dict(keywords)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return plt

def display_resume_tips():
    """
    Displays tips for users on how to incorporate keywords into different sections of their resume.
    """
    st.write("""
    ### How to Add Keywords to Your Resume:
    - **Skills Section**: Add technical skills like programming languages, tools, and frameworks (e.g., Python, AWS, Django).
    - **Experience Section**: Mention your experience with the relevant technologies, projects, and tools.
    - **Certifications Section**: Add any certifications that you hold (e.g., PMP, AWS Certified).
    - **Summary Section**: Highlight your top skills and expertise in a brief professional summary.
    """)

def main():
    # Set page config for dark/light mode toggle
    st.set_page_config(page_title="Job Description Keywords Extractor", layout="wide")

    st.title("Job Description Keywords Extractor")
    st.write("""
    Enter a job description below to extract key skills and terms.
    This tool will help you identify the important keywords to add to your resume.
    """)

    # Dark mode toggle
    theme = st.sidebar.radio("Choose theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown('<style>body{background-color:#2e2e2e;color:white;}</style>', unsafe_allow_html=True)

    # File uploader for multiple job descriptions
    uploaded_file = st.file_uploader("Upload Job Description(s)", type=["txt", "docx"], accept_multiple_files=True)

    if uploaded_file:
        for file in uploaded_file:
            job_description = file.read().decode("utf-8")  # Read file content as text
            st.subheader(f"Job Description: {file.name}")

            # Extract keywords from the job description
            keywords = extract_keywords(job_description)

            # Display the most common keywords
            st.write("### Extracted Keywords")
            for keyword, frequency in keywords:
                st.write(f"- {keyword.capitalize()} (Frequency: {frequency})")

            # Categorize the keywords into Technical, Soft Skills, and Certifications
            categorized_keywords = categorize_keywords(keywords)
            st.write("### Categorized Keywords")
            for category, skills in categorized_keywords.items():
                st.write(f"**{category}:** {', '.join(skills) if skills else 'None'}")

            # Generate and display word cloud
            st.write("### Word Cloud of Keywords")
            generate_wordcloud(keywords)
            st.pyplot()

            # Provide resume tips
            display_resume_tips()

    else:
        st.write("Please upload a job description file to extract keywords.")

# Run the app
if __name__ == "__main__":
    main()
