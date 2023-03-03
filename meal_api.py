import os
import openai
import pdb

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

def meal(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=1024,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.to_dict()

if __name__ == "__main__":
    prompt = "Whats a 15 minute keto meal that includes steak and brocoli?"
    ret = meal(prompt)
    print( ret['choices'][0].to_dict()['text'])
