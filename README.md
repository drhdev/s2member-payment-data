# s2member-payment-data Python Script

A bunch of Python scripts allowing to extract and post process the data from the Transactional Payments Emails created by the WordPress plugin S2member.  


## s2member-email2csv.py

Python script to extract the fields from an S2Member transaction Email regarding payments from Paypal and store them in a local output.csv for further use.

1. Install dependencies with pip install -r requirements.txt

2. Rename env.txt to .env and fill in your Email Server's credentials

3. Script will gather all S2Member transactional Emails from INBOX, extract Information and store it in a local output.csv
 
4. Every time the script is run, it creates additional lines to the output.csv (if new emails are found).

5. The output.csv file can be used as a ledger for all transactions an post-processed further.
