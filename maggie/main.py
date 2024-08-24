import sys
print(sys.path)
from kate import get_response
import matilde
from send_message import send_message

def maggie(website):
    body = 'This is a test email sent from Joseph Roulin.'
    recipient = 'crespo.crespo@gmail.com'
    send_message(body, recipient)
    #print("Hello Maggie!")
# Send a prompt to OpenAI
#website_audit = "example website audit"
#welcome_email_message = "example welcome email message"
#initial_prompt = (f"You are Maggie, an SEO Copilot. We were hired by Bob, owner of the website example.com. You will be talking with them by email. We sent they this welcome email message: {welcome_email_message}. Now you will help them to improve their website. Your main tolls will be your knowledge on SEO, and this website audit: {website_audit}")
#response = get_response('Hello, world!', 'llama3')
#print(response)

#example usage:
using_test = maggie('mysitefaster.com')