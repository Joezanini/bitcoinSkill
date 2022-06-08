from webex_skills.api import SimpleAPI
from webex_skills.dialogue import responses
from webex_skills.models.mindmeld import DialogueState
import requests
import json
from requests.structures import CaseInsensitiveDict

api = SimpleAPI()
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"

@api.handle(default=True)
async def greet(current_state: DialogueState) -> DialogueState:
    text = 'Hello I am a super simple skill'
    new_state = current_state.copy()

    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state


@api.handle(pattern=r'.*\sbitcoin\s?.*')
async def btc_to_usd(current_state: DialogueState) -> DialogueState:
    new_state = current_state.copy()
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200 :
        text = 'Bitcoin price not currently available'
    else :
        text = "The current Bitcoin price is $" + str(resp.json()['bitcoin']['usd'])
    
      # Call lights API to turn on your light here.
    
    new_state.directives = [
        responses.Reply(text),
        responses.Speak(text),
        responses.Sleep(10),
    ]

    return new_state
