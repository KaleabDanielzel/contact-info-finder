import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search

def extract_emails_and_phones(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"(\+?\d{1,3}[\s\-]?)?(\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{4}", text)
    phones = set(["".join(phone) for phone in phones])
    return set(emails), phones

def get_first_website(company_name):
    query = company_name + " official website"
    for url in search(query, num_results=5):
        if "linkedin.com" in url.lower():
            continue
        return url
    return None

def get_contact_info(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        emails, phones = extract_emails_and_phones(text)
        return emails, phones
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return set(), set()

def get_website_title(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string.strip()
    except:
        return "No title found"

def save_to_txt(company, website, title, emails, phones):
    with open("contact_results.txt", "a", encoding="utf-8") as file:
        file.write(f"Company: {company}\n")
        file.write(f"Website: {website}\n")
        file.write(f"Title: {title}\n")
        file.write(f"Emails: {', '.join(emails) if emails else 'None'}\n")
        file.write(f"Phones: {', '.join(phones) if phones else 'None'}\n")
        file.write("-" * 40 + "\n")

if __name__ == "__main__":
    print("=== Company Contact Info Finder ===\n")
    while True:
        company = input("Enter company name (or 'exit' to quit): ")
        if company.lower() == "exit":
            print("Goodbye!")
            break

        website = get_first_website(company)
        if website:
            print(f"\nFound website: {website}")
            title = get_website_title(website)
            print(f"Website Title: {title}")

            emails, phones = get_contact_info(website)

            print("Emails found:", emails if emails else "No emails found")
            print("Phone numbers found:", phones if phones else "No phone numbers found")
            
            save_to_txt(company, website, title, emails, phones)
            print("Results saved to contact_results.txt\n")
        else:
            print("Could not find official website.\n")
