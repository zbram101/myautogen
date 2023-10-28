# from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample.json
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


assistant = AssistantAgent("AlertIdetntifer", llm_config={"config_list": config_list})

user_proxy = UserProxyAgent("user_proxy", 
                            human_input_mode="TERMINATE", 
                            max_consecutive_auto_reply=10,
                            code_execution_config={"work_dir": "coding"},
                            llm_config={"config_list": config_list},
                            system_message="Reply TERMINATE if the task has been solved at full satisfaction. Otherwise, reply CONTINUE, and the reason why the task is not solved yet"
                                                   )


user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
# This initiates an automated chat between the two agents to solve the task