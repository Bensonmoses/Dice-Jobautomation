from scripts.scrape_jobs import scrape_dice_jobs, scrape_monster_jobs, scrape_linkedin_jobs
from scripts.resume_match import match_resume_to_job
from scripts.customize_resume import customize_resume
from scripts.apply_jobs import apply_for_jobs
import os
import time
from config.config import DICE_USERNAME, DICE_PASSWORD

def main():
    # Step 1: Scrape job listings from various platforms
    print("Scraping job listings...")
    dice_jobs = scrape_dice_jobs(DICE_USERNAME, DICE_PASSWORD)
    monster_jobs = scrape_monster_jobs()
    linkedin_jobs = scrape_linkedin_jobs()

    # Combine all job listings into one list
    all_jobs = dice_jobs + monster_jobs + linkedin_jobs
    print(f"Found {len(all_jobs)} job listings.")

    # Step 2: Check each job and apply if there's a match
    for job in all_jobs:
        print(f"\nProcessing job: {job['title']} - {job['company']}")

        # Step 2.1: Match resume to job description
        if not match_resume_to_job(job):
            print(f"Skipping job {job['title']} due to mismatch.")
            continue

        # Step 2.2: Customize resume for the job
        print(f"Customizing resume for {job['title']}...")
        customized_resume = customize_resume("storage/updated_resume.pdf", job)

        # Step 2.3: Apply for the job
        print(f"Applying for job {job['title']}...")
        apply_for_jobs([job], customized_resume)

        # Optional: Sleep between applications to avoid rate-limiting
        time.sleep(5)

    print("All jobs processed.")

if __name__ == "__main__":
    main()
