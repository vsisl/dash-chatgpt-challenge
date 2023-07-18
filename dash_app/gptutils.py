"""
Functions making openAI API calls.
"""
import openai  # chat-gpt API

openai.api_key = open("openai_api_key.txt", "r").read().strip("\n")


def get_completion(prompt, model="gpt-3.5-turbo"):
    """Creates chatGPT response

    :param prompt: str
    :param model: str; optional, default: "gpt-3.5-turbo"
    :return: tuple of str: response
                      int: total API call tokens used by this function
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=300,
        temperature=0.3,  # this is the degree of randomness of the model's output, bigger number = greater 'creativity'
    )
    return response.choices[0].message["content"], response["usage"]["total_tokens"]


# def get_image(text):
#     """Creates an image based on the input text
#
#     :param prompt: str
#     :param model: str; optional, default: "gpt-3.5-turbo"
#     :return: str: response
#     """
#     # input_img = Image.open("moscow.png").convert('RGBA')
#     # mask_img = Image.open("moscow_mask.png").convert('RGBA')
#     # import pdb; pdb.set_trace()
#     # import pdb; pdb.set_trace()
#     response = openai.Image.create_edit(
#         image=open("moskau.png", "rb"),
#         mask=open("moskau_mask.png", "rb"),
#         prompt="A city surrounded by {text} in pastel colors",
#         n=1,
#         size="256x256",
#     )
#
#     image_url = response["data"][0]["url"]
#     print(image_url)
#     import pdb
#
#     pdb.set_trace()
#     response = openai.Image.create(prompt=prompt, n=1, size="256x256")
#     return response.choices[0].message["content"], response["usage"]["total_tokens"]


def get_classification(input_text, model="text-davinci-003"):
    response = openai.Completion.create(
        model=model,
        # prompt=f'The following is a list of techniques used in propaganda texts: 'Appeal to Authority', 'Appeal to Fear Prejudice', 'Bandwagon or Reductio ad hitlerum', 'Black and White Fallacy', 'Causal Oversimplification', 'Doubt', 'Exaggeration or Minimisation', 'Flag-Waving',  'Loaded Language', 'Name Calling or Labeling', 'Repetition', 'Slogans', 'Thought-terminating Cliches', 'Whataboutism or Straw Man or Red Herring'.\n\nThe following is a list of techniques and their defintions used in propaganda texts: \n'Appeal to Authority' - Stating that a claim is true simply because a valid authority or expert on the issue said it was true, without any other supporting evidence offered.\n'Appeal to Fear Prejudice' - Seeking to build support for an idea by instilling anxiety and/or panic in the population towards an alternative.\n'Bandwagon or Reductio ad hitlerum' - Attempting to persuade the target audience to join in and take the course of action because "everyone else is taking the same action".\n'Black and White Fallacy'-Presenting two alternative options as the only possibilities, when in fact more possibilities exist. As an the extreme case, tell the audience exactly what actions to take, eliminating any other possible choices.\n'Causal Oversimplification'-Assuming a single cause or reason when there are actually multiple causes for an issue.\n'Doubt'-Questioning the credibility of someone or something.\n'Exaggeration or Minimisation'-Either representing something in an excessive manner: making things larger, better, worse (e.g., "the best of the best", "quality guaranteed") or making something seem less important or smaller than it really is (e.g., saying that an insult was just a joke). \n'Flag-Waving'- Playing on strong national feeling (or to any group; e.g., race, gender, political preference) to justify or promote an action or idea \n'Loaded Language'- Using specific words and phrases with strong emotional implications (either positive or negative) to influence an audience.\n'Name Calling or Labeling'-Labeling the object of the propaganda campaign as either something the target audience fears, hates, finds undesirable or loves, praises. \n'Repetition'-Repeating the same message over and over again so that the audience will eventually accept it.\n'Slogans'-A brief and striking phrase that may include labeling and stereotyping. Slogans tend to act as emotional appeals.\n'Thought-terminating Cliches'-Words or phrases that discourage critical thought and meaningful discussion about a given topic. They are typically short, generic sentences that offer seemingly simple answers to complex questions or that distract attention away from other lines of thought. \n'Whataboutism or Straw Man or Red Herring'- A technique that attempts to discredit an opponent\'s position by charging them with hypocrisy without directly disproving their argument, when an opponent\'s proposition is substituted with a similar one which is then refuted in place of the original proposition or introducing irrelevant material to the issue being discussed, so that everyone\'s attention is diverted away from the points made.\n\nIn the following text identify which of these techniques are present, it can be multiple or none. Enclose the found techniques in square brackets imitating input for Python list. Separate the techniques with a comma, put parantheses around each found technique, e.g. ['Flag-Waving',  'Loaded Language'] or None if no technique is found.\n\nText: {input_text}\nFound techniques:',
        prompt=f"The following is a list of techniques used in propaganda texts: \
        'Appeal to Authority', 'Appeal to Fear Prejudice', 'Bandwagon or Reductio ad hitlerum', \
        'Black and White Fallacy', 'Causal Oversimplification', 'Doubt', 'Exaggeration or Minimisation', 'Flag-Waving',\
        'Loaded Language', 'Name Calling or Labeling', 'Repetition', 'Slogans', 'Thought-terminating Cliches',\
        'Whataboutism or Straw Man or Red Herring'.The following is a list of techniques and their definitions used in \
        propaganda texts: 'Appeal to Authority' - Stating that a claim is true simply because a valid authority or \
        expert on the issue said it was true, without any other supporting evidence offered.'Appeal to Fear Prejudice' \
        - Seeking to build support for an idea by instilling anxiety and/or panic in the population towards an \
        alternative.'Bandwagon or Reductio ad hitlerum' - Attempting to persuade the target audience to join in \
        and take the course of action because 'everyone else is taking the same action'.'Black and White Fallacy'-\
        Presenting two alternative options as the only possibilities, when in fact more possibilities exist. As an the\
        extreme case, tell the audience exactly what actions to take, eliminating any other possible choices.'Causal\
        Oversimplification'-Assuming a single cause or reason when there are actually multiple causes for an issue.\
        'Doubt'-Questioning the credibility of someone or something.'Exaggeration or Minimisation'-Either\
        representing something in an excessive manner: making things larger, better, worse (e.g., 'the best of the \
        best', 'quality guaranteed') or making something seem less important or smaller than it really is (e.g., \
        saying that an insult was just a joke). 'Flag-Waving'- Playing on strong national feeling (or to any group; \
        e.g., race, gender, political preference) to justify or promote an action or idea 'Loaded Language'- Using \
        specific words and phrases with strong emotional implications (either positive or negative) to influence an \
        audience.'Name Calling or Labeling'-Labeling the object of the propaganda campaign as either something the \
        target audience fears, hates, finds undesirable or loves, praises. 'Repetition'-Repeating the same message \
        over and over again so that the audience will eventually accept it.'Slogans'-A brief and striking phrase that \
        may include labeling and stereotyping. Slogans tend to act as emotional appeals.'Thought-terminating Cliches'-\
        Words or phrases that discourage critical thought and meaningful discussion about a given topic. They are \
        typically short, generic sentences that offer seemingly simple answers to complex questions or that distract \
        attention away from other lines of thought. 'Whataboutism or Straw Man or Red Herring'- A technique that \
        attempts to discredit an opponent's position by charging them with hypocrisy without directly disproving \
        their argument, when an opponent's proposition is substituted with a similar one which is then refuted in \
        place of the original proposition or introducing irrelevant material to the issue being discussed, so that \
        everyone's attention is diverted away from the points made.In the following text presented after the \
        word 'Text' identify which of these techniques are present, it can be multiple or none. Enclose the found \
        techniques in square brackets imitating input for Python list consisting of strings. Separate the techniques \
        with a comma, put parantheses around each found technique, e.g. ['Flag-Waving',  'Loaded Language'] or None if \
        no technique is found.Text: {input_text}\n"
        + "\n\n###\n\n",
        temperature=0,
        max_tokens=35,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )

    return response["choices"][0]["text"]


def get_classification_cheaper(prompt, model="gpt-3.5-turbo"):
    """Creates chatGPT response

    :param prompt: str
    :param model: str; optional, default: "gpt-3.5-turbo"
    :return: str: response
    """
    messages = [
        {
            "role": "system",
            "content": "You are a model that finds propaganda techniques in a provided text. The following is a list of techniques and their definitions used in propaganda texts:\n\n'Appeal to Authority' - Stating that a claim is true simply because a valid authority or expert on the issue said it was true, without any other supporting evidence offered.\n\n'Appeal to Fear Prejudice' - Seeking to build support for an idea by instilling anxiety and/or panic in the population towards an alternative.\n\n'Bandwagon or Reductio ad hitlerum' - Attempting to persuade the target audience to join in and take the course of action because everyone else is taking the same action.\n\n'Black and White Fallacy' - Presenting two alternative options as the only possibilities, when in fact more possibilities exist. As an extreme case, tell the audience exactly what actions to take, eliminating any other possible choices.\n\n'Causal Oversimplification' - Assuming a single cause or reason when there are actually multiple causes for an issue.\n\n'Doubt' - Questioning the credibility of someone or something.\n\n'Exaggeration or Minimisation' - Either representing something in an excessive manner: making things larger, better, worse (e.g., the best of the best, quality guaranteed) or making something seem less important or smaller than it really is (e.g., saying that an insult was just a joke).\n\n'Flag-Waving' - Playing on strong national feeling (or to any group; e.g., race, gender, political preference) to justify or promote an action or idea.\n\n'Loaded Language' - Using specific words and phrases with strong emotional implications (either positive or negative) to influence an audience.\n\n'Name Calling or Labeling' - Labeling the object of the propaganda campaign as either something the target audience fears, hates, finds undesirable or loves, praises.\n\n'Repetition' - Repeating the same message over and over again so that the audience will eventually accept it.\n\n'Slogans' - A brief and striking phrase that may include labeling and stereotyping. Slogans tend to act as emotional appeals.\n\n'Thought-terminating Cliches' - Words or phrases that discourage critical thought and meaningful discussion about a given topic. They are typically short, generic sentences that offer seemingly simple answers to complex questions or that distract attention away from other lines of thought.\n\n'Whataboutism or Straw Man or Red Herring' - A technique that attempts to discredit an opponent's position by charging them with hypocrisy without directly disproving their argument, when an opponent's proposition is substituted with a similar one which is then refuted in place of the original proposition or introducing irrelevant material to the issue being discussed, so that everyone's attention is diverted away from the points made.",
        },
        {
            "role": "user",
            "content": "In the following text identify which of these techniques are present in a sentence, it can be multiple or none. Enclose the found techniques in each sentence in square brackets imitating input for Python list. Separate the techniques with a comma, put parentheses around each found technique, e.g. ['Flag-Waving',  'Loaded Language'] or None if no technique is found.",
        },
        {
            "role": "assistant",
            "content": "Okay, I understand. I will either return a list containing the found techniques or None. For multiple sentences a will return a combination of lists and None delimited by commas.",
        },
        {
            "role": "user",
            "content": "The global economy would plunge into chaos, with skyrocketing fuel prices, widespread unemployment, and a devastating blow to industries heavily reliant on oil.",
        },
        {"role": "assistant", "content": "['Appeal to Fear Prejudice']"},
        {
            "role": "user",
            "content": "Democrats bolted as soon as Trump's speech ended in an apparent effort to signal they can't even stomach being in the same room as the president.",
        },
        {
            "role": "assistant",
            "content": "['Exaggeration or Minimisation', 'Loaded Language']",
        },
        {
            "role": "user",
            "content": "By banning oil, they aim to cripple not only their adversaries but also their allies, leaving them at the mercy of their own agenda.",
        },
        {
            "role": "assistant",
            "content": "['Exaggeration or Minimisation']",
        },
        {
            "role": "user",
            "content": "Together, we can expose America's true intentions and safeguard the world from their manipulative grasp.",
        },
        {
            "role": "assistant",
            "content": "['Appeal to Fear Prejudice']",
        },
        {
            "role": "user",
            "content": "This is a car.",
        },
        {
            "role": "assistant",
            "content": "None",
        },
        {
            "role": "user",
            "content": "Our vast reserves and unwavering determination will ensure that the global oil market remains stable and prosperous.",
        },
        {
            "role": "assistant",
            "content": "['Loaded Language']",
        },
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )

    return response.choices[0].message["content"]
