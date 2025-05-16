from os.path import isfile
import json
import ollama
from datetime import datetime
import time
import json
from google import genai
from openai import OpenAI

def WriteFile():
    pass

def ReadQuestionsFromFile(instructionFullPath: str, rag = False):
    with open(instructionFullPath, encoding='utf-8') as f:
        instructions: list = json.load(f)

    result = []

    for instruction in instructions:
        if instruction['rag_prompt'] == '' and rag: continue

        result.append(instruction)

    return result

def GetOllamaAnswer(model,prompt,client = None):
    answer = ollama.generate(model=model, prompt=prompt)

    return answer.response

def GetGoogleApiAnswer(model,prompt,client):
    answer = client.models.generate_content(
        model=model, contents=prompt
    )

    return answer.text

def GetOpenRouterApiAnswer(model,prompt,client):
    answer = client.chat.completions.create(
        extra_body={},
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return answer.choices[0].message.content

def GetResponses(AnswerFunction,data_path,save_path,model,params,timeout,rag=False,api_client = None):
    instructions = ReadQuestionsFromFile(data_path,rag=rag)

    modelName = model.replace('/',';').replace(':','_')
    saveFile = f'results_{modelName}.json'
    saveFile = 'RAG_' + saveFile if rag else saveFile
    saveFile = 'CustomRAG_' + saveFile if rag and data_path != 'instructions/ModelInstructions.json' else saveFile
    
    fullpath = save_path + '/' + saveFile

    if isfile(fullpath):
        with open(fullpath, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = {
            'model': model,
            'params': params,
            'Qs&As':[]
        }

    starts = len(results['Qs&As'])
    ends = len(instructions)

    print(starts,'-',ends)
    checkpoint = datetime.now()
    for i in range(starts,ends):
        inst = instructions[i]
        if "prompt" in inst.keys(): prompt = inst['prompt']
        elif rag and 'rag_prompt' not in inst.keys(): continue
        elif rag and inst['rag_prompt'] != '': prompt = inst['rag_prompt']
        elif not(rag) : prompt = inst['question']
        else: continue

        print(i,inst['id'], prompt[:64])

        answer = ""
        while answer == "":
            answer = AnswerFunction(model,prompt,api_client) 

        results['Qs&As'].append({
            'id': inst['id'],
            'question': inst['question'],
            'answer': answer,
            'gold': inst['gold'],
            'RAG': inst['rag_prompt'] != ''
        })
        print(i, datetime.now() - checkpoint, len(answer))
        time.sleep(timeout)
        checkpoint = datetime.now()

        with open(fullpath, 'wt', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

with open('keys.json', encoding='utf-8') as f:
    api_keys = json.load(f)

google_api_key = api_keys['Gemini']
openrouter_api_key = api_keys['OpenRouter']

google_client = genai.Client(api_key=google_api_key)
openrouter_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=openrouter_api_key,
)

GetResponses(GetGoogleApiAnswer,'instructions/ModelInstructions.json','ModelResponses','gemma-3-27b-it',27,5,False,google_client)
GetResponses(GetOpenRouterApiAnswer,'instructions/ModelInstructions.json','ModelResponses','meta-llama/llama-4-maverick:free',17,5,False,openrouter_client)

model = 'modelName'
GetResponses(GetOllamaAnswer,'instructions/ModelInstructions.json','ModelResponses',model,9,1,False)