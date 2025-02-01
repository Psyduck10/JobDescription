import nltk
import streamlit as st
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import fitz  # PyMuPDF for extracting text from PDFs

# Download required NLTK datasets
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Predefined lists for categorizing skills
technical_skills = ['python', 'sql', 'aws', 'django', 'tensorflow', 'java', 'html', 'css', 'javascript', 'r', 'node.js']
soft_skills = ['communication', 'leadership', 'teamwork', 'problem-solving', 'creativity', 'adaptability', 'time management', 'collaboration']
certifications = ['pmp', 'aws certified', 'certified scrum master', 'google analytics', 'data science certification', 'project management certification']

def extract_keywords_nltk(job_description):
    """
    Extracts important keywords (nouns & proper nouns) from a job description using NLTK.
    Filters out stopwords and common terms.
    """
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(job_description)

    # POS tagging (identify proper nouns, nouns, and verbs)
    pos_tagged = pos_tag(word_tokens)

    # Filter out stopwords and focus on relevant POS tags (NN for nouns, NNP for proper nouns)
    keywords = [word.lower() for word, tag in pos_tagged if word.lower() not in stop_words and (tag == 'NN' or tag == 'NNP')]
    
    # Count the frequency of each keyword
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

def extract_pdf_text(pdf_file):
    """
    Extract text from the uploaded PDF file using PyMuPDF.
    """
    doc = fitz.open(pdf_file)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

def generate_download_link(text, file_name):
    """
    Generate a download link for the text content.
    """
    # Create the file and encode it to base64
    st.download_button(label=f"Download {file_name}",
                       data=text,
                       file_name=f"{file_name}.txt",
                       mime="text/plain")

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

    # File uploader for multiple job descriptions (PDF or text)
    uploaded_file = st.file_uploader("Upload Job Description(s)", type=["txt", "pdf"], accept_multiple_files=True)

    if uploaded_file:
        for file in uploaded_file:
            job_description = ""
            if file.type == "application/pdf":
                # Extract text from the PDF
                job_description = extract_pdf_text(file)
                st.subheader(f"Job Description from PDF: {file.name}")
            elif file.type == "text/plain":
                # Read the text file directly
                job_description = file.read().decode("utf-8")
                st.subheader(f"Job Description from Text File: {file.name}")

            # Display the job description and option to copy it to clipboard
            st.write("### Job Description:")
            st.text_area("Job Description", job_description, height=200)

            # Button to generate download link for the job description
            generate_download_link(job_description, file.name)

            # Extract keywords from the job description
            keywords = extract_keywords_nltk(job_description)

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

            # Create text for downloading extracted keywords
            extracted_text = "Extracted Keywords:\n"
            for keyword, frequency in keywords:
                extracted_text += f"{keyword.capitalize()} (Frequency: {frequency})\n"

            extracted_text += "\nCategorized Keywords:\n"
            for category, skills in categorized_keywords.items():
                extracted_text += f"{category}: {', '.join(skills) if skills else 'None'}\n"

            # Add "Download Extracted Keywords" button
            generate_download_link(extracted_text, f"Extracted_Keywords_{file.name}")

    else:
        st.write("Please upload a job description file (PDF or Text) to extract keywords.")

# Run the app
if __name__ == "__main__":
    main()
