import openai
import os

# Set up authentication for the OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]
START_EDIT_TAG = "START_PSEUDO"
END_EDIT_TAG = "END_PSEUDO"
MAX_TOKENS = 4000
LOG_MSG = True
