from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample.json
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


alert_idetntifer = AssistantAgent("alert_idetntifer", llm_config={"config_list": config_list}, system_message="Your goal is to identify if the user has mentioned any dangerour or illegal activities in the chat. If you identify any, reply ALERT. Otherwise, reply CONTINUE.")

stuck_idetntifer = AssistantAgent("stuck_idetntifer", llm_config={"config_list": config_list}, system_message="Your goal is to identify if the user is stuck or is not willing to share things with you. If you identify they are stuck, reply STUCK. Otherwise, reply CONTINUE.")

user_proxy = UserProxyAgent("user_proxy", 
                            human_input_mode="ALWAYS", 
                            max_consecutive_auto_reply=10,
                            code_execution_config={"work_dir": "coding"},
                            llm_config=False,
                            system_message="Formulate a response to user in the conversation. There are some things you need to consider when responding to the user. 1) if user has mentioned any dangerour or illegal activities in the chat, you should TERMINATE with OH NO BAD IDEA. 2) if the user seems stuck in the conversation you should TERMINATE OH NO YOUR STUCK"
                                                   )


groupchat = GroupChat(agents=[user_proxy, alert_idetntifer, stuck_idetntifer], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


user_proxy.initiate_chat(manager, message="AI: how are you User: I dont know")
# This initiates an automated chat between the two agents to solve the task