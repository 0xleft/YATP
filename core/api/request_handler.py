import json

from requests import post, Response

prompt = """
You need to make an executive summary in english referencing all the photos. The executive summary is about a building site and what is wrong with the building site. The what is wrong part is more important. After the summary you need to make a list of things that were bad, referencing the photos. You should only mention one issue that is summary of a few photos and if the issue is not associated with other issues you should mention it differently. Just keep in mind that Idem means 'the same as the last one'.  Do not use italian words. An executive summary should be only  a short paragraph. Try to be as concise as possible. DO NOT INCLUDE ANY DISCLAIMERS. Do not say P1, P2 say Photo 1, Photo 2. Try to talk about issues very shortly. Ok means good. Do not forget to list the issues at the bottom. Smoking is not permitted on a building site and should be treated as a separate issue. DO NOT mention photos in the executive summary you should only summarize the descriptions. Only the part where you list should mention photos. If there are good things you should also mention them in the summary. MENTION PHOTOS ONLY IN THE LIST AND NOT IN THE PARAGRAPH. If one photo is idem group it up the the last one. DO NOT MENTION PHOTOS THAT DO NOT EXIST.
GENERATE AN EXECUTIVE SUMMARY FOR THIS INPUT: USER_INPUT
"""


def model_complete_request(api_key, messages, model="gpt-3.5-turbo") -> Response:
    return post("http://pageup.lt:8700/pleasegivetomeyes", data=json.dumps({
        "model": model
        , "messages": messages}),
                headers={"Authorization": f"{api_key}", "Content-Type": "application/json"})


def model_complete_request_prompt(api_key, user_input: str, input_prompt=prompt) -> Response:
    input_prompt = input_prompt.replace("USER_INPUT", user_input)
    print(input_prompt)
    return model_complete_request(api_key, [{"role": "system", "content": input_prompt}])
