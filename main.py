from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import json

class Prompt(BaseModel):
    prompt: str


app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World!!'}


@app.get('/welcome')
def getName(name:str):
    return {'Hello 'f'{name}'}


@app.post('/chat')
async def chatApp(prompt:Prompt):
    prompt_data= prompt.prompt

    bedrock=boto3.client(service_name="bedrock-runtime")

    payload={
        "prompt":"[INST]"+ prompt_data +"[/INST]",
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
    }
    body=json.dumps(payload)
    model_id="meta.llama2-70b-chat-v1"
    response=bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body=json.loads(response.get("body").read())
    response_text=response_body['generation']
    return response_text