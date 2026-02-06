from llm.model import LLM


def create_agent(provider: str, model_name: str, tools: list):

    factory = LLM(provider=provider)
    llm = factory.get_model(model_name=model_name)
    return llm.bind_tools(tools)
