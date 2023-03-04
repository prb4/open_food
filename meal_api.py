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
    prompt = "What is a 15 minute keto meals that include steak and brocoli?  And tell me where you got the meal from"
    ret = meal(prompt)
    print( ret['choices'][0].to_dict()['text'])
