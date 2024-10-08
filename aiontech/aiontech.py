import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://www.aiontech.ai/careers.html"

# Send a GET request to the website
response = requests.get(url)

# Check if the response is successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all job postings based on the provided structure
    job_postings = soup.find_all('article', class_='job')

    # Initialize an empty list to store the job openings
    job_openings = []

    # Loop through each job posting
    for job in job_postings:
        # Extract the job role
        job_role = job.find('h3').text.strip() if job.find('h3') else 'N/A'
        
        # Extract job metadata
        metadata = job.find('div', class_='job-metadata')
        job_info = metadata.find_all('span') if metadata else []

        # Extract job type from the metadata span
        job_type = next((span.text.strip().replace(' -', '').replace('Full Time -', '') for span in job_info if 'Full Time' in span.text), 'N/A')
        
        # Extract location
        location = job_info[1].text.strip().replace(' -', '').replace('Gurgaon,', '').strip() if len(job_info) > 1 else 'N/A'

        # Extract the posted date
        posted_before = job_info[2].text.strip() if len(job_info) > 2 else 'N/A'

        # Extract the job description
        job_description = job.find('div', class_='job-details').p.text.strip() if job.find('div', class_='job-details') else 'N/A'

        # Extract experience needed from the bold tag
        experience_needed_tag = job.find(string="Experience Req:")
        exp_needed = 'N/A'  # Default value
        if experience_needed_tag:
            exp_needed_text = experience_needed_tag.find_next(text=True)  # Get the text directly after the bold tag
            exp_needed = exp_needed_text.strip() if exp_needed_text else 'N/A'

        # Extract the job link (from the onclick function in the button)
        job_link = None
        apply_button = job.find('button', class_='btn btn-primary')
        if apply_button and 'onclick' in apply_button.attrs:
            onclick_value = apply_button['onclick']
            job_link = f"https://www.aiontech.ai/{onclick_value.split('openJobApplicationModal')[1].split('()')[0].strip()}"

        # Create a dictionary to store the job opening details
        job_opening = {
            "company": "AionTech",  # Hardcoding the company name as specified
            "location": location,
            "job_type": job_type,  # Updated to extract job type
            "exp_needed": exp_needed,  # Updated to extract experience needed
            "eligibility_criteria": "N/A",  # Since no specific eligibility criteria were mentioned
            "job_role": job_role,  # Added job role
            "job_description": job_description,
            "posted_before": posted_before,
            "job_link": job_link  # Adding the job application link
        }

        # Add the job opening to the list
        job_openings.append(job_opening)

    # Convert the list to JSON format
    json_output = json.dumps(job_openings, indent=4)

    # Print the JSON output
    print(json_output)

    # Optionally, you can save the output to a JSON file
    with open('aiontech_job_openings.json', 'w') as json_file:
        json.dump(job_openings, json_file, indent=4)

    print("Job openings have been saved to 'aiontech_job_openings.json'.")
    
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
