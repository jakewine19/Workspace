**Secret Pollyanna**

Script to generate matches for a secret santa or pollyanna gift exchange and then email each participant their match plus that persons Christmas wish list. 

It uses two yaml configuration files:
1. fields.yaml - Holds an email address, name and then list of gift ideas
2. significant_others.yaml - Holds the pairs of significant others that are participating in the secret pollyanna

It has two functions:
1. pair_email_randomly - Pairs all of the participants up randomly and sends out the emails
2. pair_emails_with_prohibition - Pairs all of the participants up randonmly, but they cannot be paired to their significant other.

Run the script through the command line by passing it arguments
- --fields <file path> | 
- --sig_others <file path> |
- --prohibit | 
