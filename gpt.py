from gpt4all import GPT4All

model_name: str = "DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
gpt_model: GPT4All = GPT4All(model_name, model_path="./", device="cpu")

with gpt_model.chat_session():
    response = gpt_model.generate("Tell me how strong a gorilla is", temp=0.6, max_tokens=100)

print(response)
# responses are not that great, as it includes the thinking done by the model