'''
read.py

Reads a local file into a text buffer, then sends it to GPT-4 for translation into an English string that is easily understood by humans.
The string is sent to Eleven Labs for trancoding into audio, which is then played back to the user.
'''

import openai
import elevenlabs
import json
import os
import sys
import time
import datetime

# OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Eleven Labs API key
elevenlabs.api_key = os.environ['ELEVENLABS_API_KEY']

elevenlabs.set_api_key(elevenlabs.api_key)


# OpenAI engine ID
engine = 'gpt-4-0613'


def read_file(file):
    with open(file, 'r') as f:
        text = f.read()
    return text


def summarize_with_llm(filename, text, **kwargs):
    # Summarize text with OpenAI GPT-4
    prompt = '''
    As a member of a highly-skilled translation team, your mission is to translate complex computer codes, technical formulas, and mathematical notations into comprehensive, listener-friendly English audio transcripts. Your task starts with analyzing an unidentified language file and turning it into an accessible audio script that clearly communicates the inherent logic and structure of the code. In the event of encountering code ambiguities, make an educated judgement. Moreover, you are required to discern the programming language from the input and filename.

    Ensure to provide sufficient context, including brief and fitting explanations—up to a paragraph—for known acronyms and jargon to facilitate understanding amongst a technically proficient audience who may be unfamiliar with the given code or formula. Include relevant comments presented within the code into the audio translation, but omit those that are trivial or irrelevant to the logic of the code.

    In the case of acknowledging an architectural pattern, mention it specifically, and provide a brief explanation. If the code belongs to a function which appears to be part of a greater system, envision the probable broader role, and incorporate this understanding into your explanation. For any functions found within the code that seem to be divided, they should be considered independently yet portrayed in relation to each other.

    Your ultimate objective is not to provide a literal line-by-line translation, but to create an auditory tool that helps in deciphering nuanced code details and understanding them on a deeper level. Remember, strive for clarity in an auditory context. Context is less important than the meat of the code.

    File: {filename}

    Input: 
    {text} 
    '''

    prompt = prompt.format(text=text, filename=filename)

    if 'model' not in kwargs:
        kwargs['model'] = engine

    response = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )

    message = response["choices"][0]["message"]['content']

    print(message)

    return message


def convert_to_audio(text, voice='Adam', model='eleven_monolingual_v1', stream=False):
    # Convert text to audio with Eleven Labs
    audio = elevenlabs.generate(
      text=text,
      voice=voice,
      model=model,
      stream=stream
    )

    return audio

def play_audio(audio):
    elevenlabs.play(audio)

def read_aloud(file, max_tokens=4000, stream=False, voice='Adam'): #, audience='technical'):
    # Read file
    text = read_file(file)

    # Summarize text
    summary = summarize_with_llm(text, file, temperature=0.9, max_tokens=max_tokens)#, audience=audience)

    # Convert text to audio
    audio = convert_to_audio(summary, stream=stream, voice=voice)

    # Play audio
    if stream:
        elevenlabs.stream(audio)
    else:
        elevenlabs.play(audio)

if __name__ == '__main__':
    main()
