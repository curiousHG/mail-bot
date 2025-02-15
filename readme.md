# Python Mail to Bot to send customized message to multiple recipients

### I am using here to apply for job applications, along with my resume. 😋

To run one is required to have a GCP project with OAuth2.0 client ID and secret key. The client ID and secret key are to be stored in the `credentials.json` file. The `credentials.json` file is to be stored in the same directory as the python script. Which can be learned from the following link: [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)

For this repo purpose i have a message.py file which gives me a function where i provide the name of the recipient and the company to be sent to the recipient. Then a custom message is returned from the function.

```python
# message.py
def give_text_html(recipient_name, recipient_company):
    text = f"Dear {recipient_name},\n\n{recipient_company}\n\nRegards,\nSender"
    html = f"""\
    <html>
    <body>
        <p>Dear {recipient_name},<br>
        {recipient_company}<br>
        Regards,<br>
        Sender
        </p>
    </body>
    </html>
    """
    return text, html
```

You should create a separate account for testing and add that account has a user of the OAuth2.0 service.

Add your email in a .env file as SENDER_EMAIL as shown in .env.example file.


To Run the script:
```bash
python3 main.py
```
