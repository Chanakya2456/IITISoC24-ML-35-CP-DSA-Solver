from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig, pipeline
import torch
torch.random.manual_seed(0)
from rag import *
def load_phi_model():
    config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    model_phi = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-128k-instruct",
        device_map="cuda",
        torch_dtype="auto",
        quantization_config=config,
        trust_remote_code=True,
    )
    tokenizer_phi = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")
    return model_phi,tokenizer_phi



def new_problem(problem,db):
    model_phi,tokenizer_phi = load_phi_model()
    docs = new_question(problem,db)
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", trust_remote_code=True, torch_dtype=torch.bfloat16)
    messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": f""""simplify: Convert the following competitive programming question into a clear and concise problem statement suitable for an automated code generation model.
                                        Make sure to keep the response more technical and to the point. Also , give the constraints and the example inputs and outputs.
             {problem}."""},
    {"role": "assistant", "content": "Sure!, Here is a more understandable translation of the question:"}, 
    ]

    pipe = pipeline( 
        "text-generation", 
        model=model_phi, 
        tokenizer=tokenizer_phi, 
    ) 

    generation_args = { 
        "max_new_tokens": 1000, 
        "return_full_text": False, 
        "temperature": 0.0, 
        "do_sample": False, 
    } 
    context  = docs[0].page_content + docs[1].page_content
    simplified_problem = pipe(messages, **generation_args)[0]['generated_text'] 
    
    prompt = f"""
    You are an expert assistant for solving coding problems. Provide a detailed solution to the given problem.
    Write the code in C++ if the language is not specified.

    1. Understand the Problem: Comprehend the input, output, and constraints.
    2. Explain the Solution: Break down the logic and flow.
    3. Complexity Analysis: Analyze time and space complexity.
    Context(Use this if helpful):
    {context}

    Solve the following question:
    {simplified_problem}
    Here is the solution:
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=2000)
    solution = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    position = solution.find("Here is the solution:")

    if(position != -1):
        trimmed_solution = solution[position:]
    else:
        trimmed_solution = solution
    
    return trimmed_solution



def codeforces_problem(problem):
    model_phi,tokenizer_phi = load_phi_model()
    tokenizer_ft = AutoTokenizer.from_pretrained("Kushagra-2023/Fine-tuned-deepseek")
    model_ft = AutoModelForCausalLM.from_pretrained("Kushagra-2023/Fine-tuned-deepseek")
    messages = [ 
    {"role": "system", "content": "You are a helpful AI assistant."}, 
    {"role": "user", "content": f""""simplify: Convert the following  question into a clear and concise problem statement suitable for an automated code generation model.
                                        Make sure to keep the response more technical and to the point. Also , give the constraints and the example inputs and outputs.
             {problem}."""},
    {"role": "assistant", "content": "Sure!, Here is a more understandable translation of the question:"}, 
    ]

    pipe = pipeline( 
        "text-generation", 
        model=model_phi, 
        tokenizer=tokenizer_phi, 
    ) 

    generation_args = { 
        "max_new_tokens": 1000, 
        "return_full_text": False, 
        "temperature": 0.0, 
        "do_sample": False, 
    } 

    simplified_problem = pipe(messages, **generation_args)[0]['generated_text']
    
    prompt = f"""
    You are an expert assistant for solving coding problems. Provide a detailed solution to the given problem.

    {simplified_problem}

    Write the code in C++ if the language is not specified.

    1. Understand the Problem: Comprehend the input, output, and constraints.
    2. Outline the Approach: Describe your approach, mentioning any algorithms or data structures used.
    3. Provide the Solution: Write clean, well-commented code.
    4. Explain the Solution: Break down the logic and flow.
    5. Complexity Analysis: Analyze time and space complexity.
    6. Example Walkthrough: Show an example input and walk through the code step-by-step.

    Here is the solution:
    """

    inputs = tokenizer_ft(prompt, return_tensors="pt").to(model_ft.device)
    outputs = model_ft.generate(**inputs, max_length=2000)
    solution = tokenizer_ft.decode(outputs[0], skip_special_tokens=True)
    
    position = solution.find("Here is the solution:")

    if(position != -1):
        trimmed_solution = solution[position:]
    else:
        trimmed_solution = solution
    
    return trimmed_solution