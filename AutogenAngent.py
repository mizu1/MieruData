from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
##
config_list = [{'model': 'gpt-3.5-turbo', 'api_key': 'your api'}]
assistant = AssistantAgent(
    name="Monika",
    llm_config={
        "seed": 42,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)
user_proxy = UserProxyAgent(
    name="user_proxy",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
    llm_config={"config_list": config_list}
)


