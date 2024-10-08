import requests
from bs4 import BeautifulSoup
import json

# Function to scrape the job data
def scrape_job_data(url):
    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store all job data
    jobs = []

    # Find all job postings by selecting <h3> tags with the specific class
    job_tags = soup.find_all('h3', class_='alert alert-dark')

    for job_tag in job_tags:
        job_type = job_tag.text.split('(')[0].strip()  # Extract job type by splitting before '('
        
        # Find the corresponding job description and eligibility criteria from the <dl> section
        post_detail = job_tag.find_next('div', class_='text post-detail')
        if post_detail:
            job_description = ""
            eligibility_criteria = ""

            # Parse the text inside <dl> and categorize under job description and eligibility
            dts = post_detail.find_all('dt')
            dds = post_detail.find_all('dd')

            for i, dt in enumerate(dts):
                if "Job Description" in dt.text:
                    job_description = dds[i].text.strip()
                if "Experience/Skills" in dt.text:
                    eligibility_criteria = dds[i].text.strip()

        # Create a job dictionary with the required fields
        job = {
            "company": "acesoftex",
            "location": "India",
            "job_type": job_type,
            "exp_needed": None,
            "eligibility_criteria": eligibility_criteria,
            "job_description": job_description,
            "posted_before": None
        }

        # Append the job to the jobs list
        jobs.append(job)

    return jobs

# Main function to save the scraped data into a JSON file
def save_to_json_file(jobs, filename="jobs.json"):
    try:
        # Read existing data from the JSON file
        with open(filename, 'r') as file:
            existing_jobs = json.load(file)
    except FileNotFoundError:
        existing_jobs = {}

    # Append new job data to the existing JSON object
    for job in jobs:
        existing_jobs[job['job_type']] = job

    # Write the updated data back to the JSON file
    with open(filename, 'w') as file:
        json.dump(existing_jobs, file, indent=4)

# URL of the website to scrape
url = "https://www.acesoftex.com/careers.html"

# Scrape the job data
jobs = scrape_job_data(url)

# Save the scraped data to a JSON file
if jobs:
    save_to_json_file(jobs)
    print("Data has been successfully saved to jobs.json")
