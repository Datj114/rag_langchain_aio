import torch
from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer, AutoModeForCausaLLM, pipeline
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

def get_hf_llm(model_name:str="meta-llama/Llama-3.2-3B-Instruct",
               max_new_tokens:int=1024,
               **kwargs):
    """
    Get Hugging Face LLM model and tokenizer.
    """
    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=nf4_config,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Create pipeline for inference
    model_pineline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        device_map="auto",
    )
    llm = HuggingFacePipeline(
        pipeline=model_pineline,
        model_kwargs=kwargs
    )

    return llm