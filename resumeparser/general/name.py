import re
from nltk.tag import StanfordNERTagger, StanfordPOSTagger
from nltk.tag.stanford import StanfordNERTagger
import subprocess
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import spacy
import csv
from nltk.util import ngrams
from .tblmodels import names_master
from pathlib import Path
import traceback
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------------------------------------------------------


def name_recog(text):

    text = re.sub(r'[\w\.-]+\s{0,1}@\s{0,1}[\w\.-]+\.\w{3}', " ", text)
    text = re.sub(r"[,.();@#?!&$/]+ *", "  ", text)
    result = re.finditer(r"(address)", text.lower())
    for i in result:
        address_text = i.group(1).strip()
        text = text[:i.start()]      
    # print(text[0:i.start()])
    words = word_tokenize(text)
    credentials = ['cv','resume', "engineer", "engineering","curriculam", 'curriculum', 'autocad','curricular','vita','vitae','contact', 'mobile', 'personal','summary','career', 'design','objective','state','university','school', '','institute','proposed','specialist', 'data', 'date', 'education', 'name', 'experience', 'technology', 'certificate', 'power', 'structural', 'icfai','system', "bachelor", 'diploma', 'business', 'gsm', 'management', 'tripura', 'm.tech', 'e-mail', "email", "mail","cell", 'civil', 'transportation']
    # pattern = r'\b(?:' + '|'.join(map(re.escape, credentials)) + r')\b'
    refiltered_words = [word for word in words if word.lower() not in credentials]
    text = ' '.join(refiltered_words)
    # Specify the path to Stanford NER
    # need to provide the path of the package here................................................
    stanford_ner_path = str(BASE_DIR)+"/Stanford-NER-Python-master/stanford-ner-2015-12-09"

    # Specify the path to the Stanford NER model
    model_name = "english.all.3class.distsim.crf.ser.gz"
    input_text = re.sub(r'\n', ' ', text)
    input_text = re.sub(r"[,;@+#?!&$.:/%^\"°-]+ *"," ", input_text)
    print("text is =======", input_text)
    # Read Indian names from the CSV file into a list
    indian_names = []
    # with open('/home/priyanksharma/Downloads/Indian-Male-Names.csv', 'r', encoding='utf-8') as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         # Assuming the name is in the first column of the CSV file
    #         indian_names.append(row[0])

    indian_names=list(names_master.objects.using('table_db').values_list('name',flat=True))

            # time.sleep(1)

    # Input text
    # text = """
    # Jaipur 302019 9166887689 « sharma puneet39gmail com Profile ExperiencedRecruitment Professional with a demonstrated 
    # history of working in the staffing and recruiting industry Ski
    # """

    # Convert text to lowercase
    text = input_text.lower()

    # Tokenize the text into words
    words = word_tokenize(text)

    # Function to generate n-grams
    def generate_ngrams(text, n):
        n_grams = ngrams(text, n)
        return [' '.join(gram) for gram in n_grams]

    # Initialize a set to store found names
    found_names = set()

    # Iterate through different n-gram lengths
    for n in range(1, 4):  # You can adjust the range for different n-gram lengths
        n_grams = generate_ngrams(words, n)
        print(n_grams)
        for name in indian_names:
            for n_gram in n_grams:
                if name == n_gram:
                    found_names.add(name)


    # Print the found names
    found_names = list(found_names)
    found_names = sorted(found_names, key=len)
    # print(found_names)
    # print(found_names[-1].split())
    if found_names:
        print("this is db_name=========", found_names)
        print("this is db_name=========", found_names[-1].split())
        return found_names[-1].split()
    else:
        # pass

    # text blob ----------------
        blob_object1 = TextBlob(input_text)  
        print(blob_object1.tags)  
        n_list = [obj[0] for obj in blob_object1.tags if obj[1] == "NNP"]
        input_text = " ".join(n_list)
        input_text = input_text.lower()
        nlp = spacy.load('en_core_web_lg')
    
        doc = nlp(input_text)
        text = []
        for ent in doc.ents:
            if ent.label_=='PERSON':
                print(ent.text, ent.label_)
                text.append(ent.text)

        if text:
            name_text = text[0].split()
            print("spacy =======",name_text[0:3])
            return name_text
        else:
            pass
        
        #need to change the path of this file.........................................and create the file as well
        
        temp_input_file = str(BASE_DIR)+'/temp_inpupt.txt'
         
        with open(temp_input_file, 'w', encoding='utf-8') as temp_file:
            temp_file.write(input_text.title())

        command = [
            "java",
            "-mx1000m",
            "-cp",
            f"{stanford_ner_path}/stanford-ner.jar:{stanford_ner_path}/lib/*",
            "edu.stanford.nlp.ie.crf.CRFClassifier",
            "-loadClassifier",
            f"{stanford_ner_path}/classifiers/{model_name}",
            "-textFile",
            temp_input_file,
            "-outputFormat",
            "slashTags",
            "-tokenizerFactory",
            "edu.stanford.nlp.process.WhitespaceTokenizer",
            "-tokenizerOptions",
            "tokenizeNLs=false",
            "-encoding",
            "utf-8",
        ]
        print(input_text)
        # Run Stanford NER using subprocess
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            
            # Split the output into sentences
            sentences = re.split(r'\n\n', output.strip())
            
            # Process each sentence to extract tokens and tags
            for sentence in sentences:
                tokens_and_tags = [tuple(token.split('/')) for token in sentence.split()]
            person = []    
            
            for tag in range(len(tokens_and_tags)):
                if len(tokens_and_tags[tag]) == 2:
                    if tokens_and_tags[tag][1] == "PERSON":
                        person.append(tokens_and_tags[tag]) 

            name1 = []
            for item in person:
                name1.append(item[0])
            print("this is stanford ============",name1[0:3])
            return name1[0:3]

        except subprocess.CalledProcessError as e:
            # print(f"Error: {e}")s
            traceback.print_exc()
            return []
                # return f"Error: {e}"

        # name1 = [" "]
        # return name1
# text = """
#     Jaipur 302019 9166887689 « sharma puneet39gmail com Profile puneet ExperiencedRecruitment Professional prakash chand with a demonstrated 
#     history of working in the staffing and recruiting industry Ski
#     """
# print(name_recog(text))


# import re
# from nltk.util import ngrams
# from nltk.tokenize import word_tokenize
# import csv

# # Read Indian names from the CSV file into a list
# indian_names = []
# with open('/home/priyanksharma/Downloads/Indian-Male-Names.csv', 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         # Assuming the name is in the first column of the CSV file
#         indian_names.append(row[0])
#         # time.sleep(1)

# # Input text
# text = """
# Jaipur 302019 9166887689 « sharma puneet39gmail com Profile ExperiencedRecruitment Professional with a demonstrated 
# history of working in the staffing and recruiting industry Ski
# """

# # Convert text to lowercase
# text = text.lower()

# # Tokenize the text into words
# words = word_tokenize(text)

# # Function to generate n-grams
# def generate_ngrams(text, n):
#     n_grams = ngrams(text, n)
#     return [' '.join(gram) for gram in n_grams]

# # Initialize a set to store found names
# found_names = set()

# # Iterate through different n-gram lengths
# for n in range(1, 4):  # You can adjust the range for different n-gram lengths
#     n_grams = generate_ngrams(words, n)
#     print(n_grams)
#     for name in indian_names:
#         for n_gram in n_grams:
#             if name == n_gram:
#                 found_names.add(name)


# # Print the found names
# found_names = list(found_names)
# found_names = sorted(found_names, key=len)
# print(found_names)
# if found_names:
#     return found_names[-1].split()
# else:
#     pass

# -------------------------------------------------------------------------------------------------------------------------------------------------

# def name_recog(text):

#     text = re.sub(r"[,.();@#?!&$/]+ *", "  ", text)
#     words = word_tokenize(text)
#     credentials = ['cv','resume', "engineer", "engineering","curriculam", 'curriculum', 'autocad','curricular','vita','vitae','contact','personal','summary','career', 'design','objective','state','university','school', '','institute','proposed','specialist', 'data', 'date', 'education', 'name', 'experience', 'technology', 'certificate', 'power', 'structural', 'icfai','system', "bachelor", 'diploma', 'business', 'gsm', 'management', 'tripura', 'm.tech', 'e-mail', "email", "mail","cell", 'civil', 'transportation']
#     # pattern = r'\b(?:' + '|'.join(map(re.escape, credentials)) + r')\b'
#     refiltered_words = [word for word in words if word.lower() not in credentials]
#     text = ' '.join(refiltered_words)
#     # Specify the path to Stanford NER
#     # need to provide the path of the package here................................................
#     stanford_ner_path = r"/home/priyanksharma/download-2023.9.28_12.55.37-cvm-(growthgrids.com) (copy)/Stanford-NER-Python-master/stanford-ner-2015-12-09"

#     # Specify the path to the Stanford NER model
#     model_name = "english.all.3class.distsim.crf.ser.gz"
#     input_text = re.sub(r'\n', ' ', text)
#     input_text = re.sub(r"[,;@+#?!&$.:/%^\"°-]+ *"," ", input_text)
#     print("text is =======", input_text)
#     # Read Indian names from the CSV file into a list
#     indian_names = []
#     with open('/home/priyanksharma/Downloads/Indian-Male-Names.csv', 'r', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             # Assuming the name is in the first column of the CSV file
#             indian_names.append(row[0])
#             # time.sleep(1)

#     # Input text
#     # text = """
#     # Jaipur 302019 9166887689 « sharma puneet39gmail com Profile ExperiencedRecruitment Professional with a demonstrated 
#     # history of working in the staffing and recruiting industry Ski
#     # """

#     # Convert text to lowercase
#     text = input_text.lower()

#     # Tokenize the text into words
#     words = word_tokenize(text)

#     # Function to generate n-grams
#     def generate_ngrams(text, n):
#         n_grams = ngrams(text, n)
#         return [' '.join(gram) for gram in n_grams]

#     # Initialize a set to store found names
#     found_names = set()

#     # Iterate through different n-gram lengths
#     for n in range(1, 4):  # You can adjust the range for different n-gram lengths
#         n_grams = generate_ngrams(words, n)
#         print(n_grams)
#         for name in indian_names:
#             for n_gram in n_grams:
#                 if name == n_gram:
#                     found_names.add(name)


#     # Print the found names
#     found_names = list(found_names)
#     found_names = sorted(found_names, key=len)
#     # print(found_names)
#     # print(found_names[-1].split())
#     if found_names:
#         print("this is db_name=========", found_names[-1].split())
#         # return found_names[-1].split()
#     else:
#         pass

#     # text blob ----------------
#     blob_object1 = TextBlob(input_text)  
#     print(blob_object1.tags)  
#     n_list = [obj[0] for obj in blob_object1.tags if obj[1] == "NNP"]
#     input_text = " ".join(n_list)
#     input_text = input_text.lower()
#     nlp = spacy.load('en_core_web_lg')
  
#     doc = nlp(input_text)
#     text = []
#     for ent in doc.ents:
#         if ent.label_=='PERSON':
#             print(ent.text, ent.label_)
#             text.append(ent.text)

#     if text:
#         name_text = text[0].split()
#         print("spacy =======",name_text)
#         # return name_text
#     else:
#         #need to change the path of this file.........................................and create the file as well
#         temp_input_file = "/home/priyanksharma/download-2023.9.28_12.55.37-cvm-(growthgrids.com) (copy)/resumeparser/general/temp_input.txt"  
#         with open(temp_input_file, 'w', encoding='utf-8') as temp_file:
#             temp_file.write(input_text.title())

#         command = [
#             "java",
#             "-mx1000m",
#             "-cp",
#             f"{stanford_ner_path}/stanford-ner.jar:{stanford_ner_path}/lib/*",
#             "edu.stanford.nlp.ie.crf.CRFClassifier",
#             "-loadClassifier",
#             f"{stanford_ner_path}/classifiers/{model_name}",
#             "-textFile",
#             temp_input_file,
#             "-outputFormat",
#             "slashTags",
#             "-tokenizerFactory",
#             "edu.stanford.nlp.process.WhitespaceTokenizer",
#             "-tokenizerOptions",
#             "tokenizeNLs=false",
#             "-encoding",
#             "utf-8",
#         ]
#         print(input_text)
#         # Run Stanford NER using subprocess
#         try:
#             output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            
#             # Split the output into sentences
#             sentences = re.split(r'\n\n', output.strip())
            
#             # Process each sentence to extract tokens and tags
#             for sentence in sentences:
#                 tokens_and_tags = [tuple(token.split('/')) for token in sentence.split()]
#             person = []    
            
#             for tag in range(len(tokens_and_tags)):
#                 if len(tokens_and_tags[tag]) == 2:
#                     if tokens_and_tags[tag][1] == "PERSON":
#                         person.append(tokens_and_tags[tag]) 

#             name1 = []
#             for item in person:
#                 name1.append(item[0])
#             print(name1[0:3])
#             return name1[0:3]

#         except subprocess.CalledProcessError as e:
#             # print(f"Error: {e}")s
#             pass
#             # return f"Error: {e}"

# # text = """
# #     Jaipur 302019 9166887689 « sharma puneet39gmail com Profile puneet ExperiencedRecruitment Professional prakash chand with a demonstrated 
# #     history of working in the staffing and recruiting industry Ski
# #     """
# # print(name_recog(text))

