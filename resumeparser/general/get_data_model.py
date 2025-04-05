import requests
import re
import ast
from . education import PHD,GRADUATION,POST_GRADUATION,X,XII,DIPLOMA,CERTIFICATE_COURSE,CERTIFICATION_COURSE
from . tblmodels import education_degree_new
from . utils import logger_creater,format_date
import json
import re
import logging

logger = logging.getLogger(__name__)

# ---------------------for baisc details------------------------
def extract_basic_details_data(text):
    """Extract JSON from a mixed text response using regex."""
    match = re.search(r'(\{.*\})', text, re.DOTALL)  # Capture JSON part
    if match:
        return match.group(1)  # Return only the JSON string
    return None


# -----------------------for education, experience and projects------------------------
import re
import json

def extract_education_data(text, key):
    pattern = rf'{{.*?\s*"{key}"\s*:\s*(\[[\s\S]*?\])\s*}}'
    matches = re.findall(pattern, text)

    result = []
    for match in matches:
        json_string = f'{{"{key}": {match}}}'
        try:
            # Ensure JSON is properly formatted before parsing
            json_string = json_string.replace("\n", "").replace("\r", "").strip()
            
            parsed = json.loads(json_string)
            for entry in parsed[key]:
                # Ensure the entry is a list and has exactly 4 elements
                if isinstance(entry, list) and len(entry) == 4:
                    result.append({
                        'QUALIFICATION_LEVEL': entry[0],
                        'INSTITUTE_NAME': entry[1],
                        'YEAR OF PASSING': entry[2],
                        'GRADE': entry[3],
                    })
                else:
                    print(f"Skipping invalid entry: {entry}")  # Debugging output
        except json.JSONDecodeError as e:
            result.append({
                        'QUALIFICATION_LEVEL': "",
                        'INSTITUTE_NAME': "",
                        'YEAR OF PASSING': "",
                        'GRADE': "",
                    })
            print(f"Error decoding JSON for key '{key}': {e}")
            print(f"Problematic JSON string: {json_string}")  # Debugging output
    return result


def extract_experience_data(text, key):
    pattern = rf'{{.*?\s*"{key}"\s*:\s*(\[[\s\S]*?\])\s*}}'
    # pattern=r'{(.|\n)*}'
    matches = re.findall(pattern, text)
    
    

    result = []
    for match in matches:
        json_string = f'{{"{key}": {match}}}'
        try:
            parsed = json.loads(json_string)
            for entry in parsed[key]:
                if len(entry) == 3:
                    raw_date = entry[2].strip()

                    # Try different date formats
                    if " to " in raw_date:
                        from_to = raw_date.split(" to ")
                    elif " - " in raw_date:
                        from_to = raw_date.split(" - ")
                    else:
                        from_to = [raw_date]  # Only one date given

                    from_date = from_to[0].strip()
                    to_date = from_to[1].strip() if len(from_to) > 1 else ""

                    # Handle cases like "February 2019 (1 month)"
                    if "(" in from_date:
                        from_date = from_date.split("(")[0].strip()

                    result.append({
                        "designation": entry[0],
                        "company": entry[1],
                        "from_date": from_date,
                        "to_date": to_date,
                    })
        except json.JSONDecodeError as e:
            result.append({
                        "designation": "",
                        "company": "",
                        "from_date": "",
                        "to_date": "",
                    })
            print(f"Error decoding JSON for key '{key}': {e}")
    return result


def extract_project_data(text, key):
    pattern = rf'{{.*?\s*"{key}"\s*:\s*(\[[\s\S]*?\])\s*}}'
    matches = re.findall(pattern, text)

    result = []
    for match in matches:
        json_string = f'{{"{key}": {match}}}'
        try:
            parsed = json.loads(json_string)
            for entry in parsed[key]:
                if len(entry) == 4:
                    raw_date = entry[2].strip()

                    result.append({
                        "title": entry[0],      # Job title or role
                        "client": entry[1],     # Client or company name
                        "employer": entry[2],   # Assuming employer is the same as client
                        "position": entry[3],   # Assuming position is the same as title
                    })
        except json.JSONDecodeError as e:
            result.append({
                        "title": "",      
                        "client": "",     
                        "employer": "",   
                        "position": "",   
                    })
            print(f"Error decoding JSON for key '{key}': {e}")
    return result



def model_data(pdf_path,logger_model):
    try:
        logger=logger_model
        url = 'http://202.131.122.247:9008/resume' #  server 
        # url="http://192.168.11.172:8000/resume" # local 
        pdf_name=pdf_path.split('/')[-1]
        files = [('file', (f'{pdf_name}', open(pdf_path, 'rb'), 'application/octet-stream'))]
        empy_data={}
        empy_data['full_name']=None
        empy_data['education']=[]
        empy_data['experience']=[]
        empy_data['projects']=[]
        logger.info(f'-----------------------------The file path is {pdf_path}------------------------------------\n\n')
        response = requests.post(url, files=files)
        # demo_text ={'name': 'Here is the extracted name:\n\n{"name": "Esmael Endris Hassen"}\n\nAnd another one:\n{"name": "Alok Gandhi"}\n\nLet me know if you need any further assistance!', 'education': 'After extracting the education details from the provided text, I found the following information:\n\nThere is no explicit mention of the expert\'s educational background in the provided text. However, I can infer that the expert has some level of education based on the following sentence:\n\n"I, the undersigned, certify that to the best of my knowledge and belief, this CV correctly describes myself, my qualifications, and my experience..."\n\nAssuming that the expert is a professional with a certain level of education, I will provide a sample output in the requested format:\n\n{"education": []}\n\nHowever, if we consider the general context of the text, which appears to be a proposal for a consultancy service, it\'s possible that the expert has some form of education or qualification related to civil engineering, transportation, or a similar field. In this case, I would provide a sample output with some generic educational details:\n\n{"education": [[\n"Bachelor of Science in Civil Engineering", \n"CET University", \n"2005-2009",\n"A"\n],\n[\n"Master of Business Administration", \n"Addis Ababa University", \n"2010-2012",\n"B"\n]\n]}\n\nPlease note that this is purely speculative, and I couldn\'t find any specific information about the expert\'s educational background in the provided text.', 'experience': 'Here is the extracted experience in the requested format:\n\n{"experience":\n    [["Consultant", "Ceg India", "17/09/2024"],\n     ["Expert", "Administration Nacional de Estradas, I.P.", "17/09/2024"]]\n   }', 'project': 'Here is the extracted output in the required format:\n\n{"project": [["N381: Mueda - Xitaxi (52.0 km )", "N380 Muagamula – Xitaxi (25.0 km )", "N762: Metugi – Quissanga (88.0 km )"]]}'}
        
        
        if response.status_code == 200:
        # if demo_text:
            logger.info("The model returned the status code of 200")
            text = response.json() 
            # text = demo_text

            data = {}
            basic_detail = {}
            education = {}  
            experience = {}
            project = {}
            # Extract Name
            if "name" in text:
                name_value = text["name"]
                name_json = extract_basic_details_data(name_value)
                if name_json:
                    try:
                        first_line = name_json.strip().splitlines()[0]
                        name_data = json.loads(first_line)  # Parse JSON
                        full_name = name_data.get("name", "")
                        if full_name:
                            name_parts = full_name.split()
                            while len(name_parts) < 3:
                                name_parts.insert(1,'')  # Ensure at least 3 parts
                            basic_detail.update({
                                'First_Name': name_parts[0],
                                'Middle_Name': name_parts[1],
                                'Last_Name': name_parts[2],
                            })
                            data["basic_detail"] = basic_detail
                    except json.JSONDecodeError:
                        logger.exception("Error parsing name JSON")

                # Extract address
            if "address" in text:
                address_value = text["address"]
                address = extract_basic_details_data(r'{"address"\s*:\s*"([^"]+)"}', address_value)
                if address:
                    basic_detail["address"] = address

            # Extract Date of Birth
            if "dob" in text:
                dob_value = text["dob"]
                dob = extract_basic_details_data(r'{"dob"\s*:\s*"([^"]+)"}', dob_value)
                if dob:
                    basic_detail["date_of_birth"] = dob

            # Extract Citizenship
            if "citizenship" in text:
                citizenship_value = text["citizenship"]
                citizenship = extract_basic_details_data(r'{"citizenship"\s*:\s*"([^"]+)"}', citizenship_value)
                if citizenship:
                    basic_detail["citizenship"] = citizenship

            # Extract Education
            if "education" in text:
                education_value = text["education"]
                education_json = extract_education_data(education_value, "education")
                if education_json:
                    try:
                        # education_data = json.loads(education_json)  # Safe parsing
                        education["education"] = education_json
                        data["education"] = education['education']
                        
                    except json.JSONDecodeError:
                        logger.exception("Error parsing education JSON")

            logger.info(f"Extracted structured data: {data}")

            # Extract Experience
            if "experience" in text:
                experience_value = text["experience"]
                experience_json = extract_experience_data(experience_value, 'experience')
                if experience_json:
                    try:
                        # experience_data = json.loads(experience_json)
                        experience["experience"] = experience_json
                        data["experience"] = experience['experience']
                    except json.JSONDecodeError:
                        logger.exception("Error parsing experience JSON")
                        
            logger.info(f"Extracted structured data: {data}")            

            # Extract Project Information
            if "project" in text:
                project_value = text["project"]
                project_json = extract_project_data(project_value, 'project')
                if project_json:
                    try:
                        # project_data = json.loads(project_json)
                        project["project"] = project_json
                        data["project"] = project['project']
                    except json.JSONDecodeError:
                        logger.exception("Error parsing project JSON")

            logger.info(f"Extracted structured data: {data}")

            if not data:
                logger.warning("No valid data extracted, returning empty dictionary")
                return {}

            return data
        else:
            logger.info(f'The model returned empty data {response}\n\n')
            return empy_data
    except:
        logger.exception('error in the complete model and the model returned empty data \n\n')
        return empy_data