import os
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config_list_gpt = [
    {
        "model": "gpt-4o-mini",
        "api_key": OPENAI_API_KEY
    }
]

# Pizza Agent
pizza_agent = ConversableAgent(
    name = "pizza_lover",
    system_message= "You are a person who loves pizza and wants to spread its deliciousness around the world. Speak passionately about the allure of pizza.",
    llm_config={"config_list": config_list_gpt},
    human_input_mode="NEVER",
)

# Sushi Agent
sushi_agent = ConversableAgent(
    name = "sushi_lover",
    system_message= "You are a person who loves sushi and wants to spread its deliciousness around the world. Speak passionately about the allure of sushi.",
    llm_config={"config_list": config_list_gpt},
    human_input_mode="NEVER",
)

# Judge Agent
judge_agent = ConversableAgent(
    name = "judge_agent",
    system_message= "You are acting as the ultimate facilitator. Your job is to guide the debate between the two and declare a winner based on who makes the most convincing argument. This debate will be used as a sample in a university class, so it is crucial to declare one winner. Once a clear conclusion is reached, you must declare 'That's enough!' and announce the winner. The debate cannot end without this phrase, so make sure to include it.",
    llm_config={"config_list": config_list_gpt},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "That's enough" in msg["content"]
)

pizza_agent.description = "The ultimate pizza fan"
sushi_agent.description = "The ultimate sushi fan"
judge_agent.description = "The facilitator who decides the debate winner"

group_chat = GroupChat(
    agents = [pizza_agent, sushi_agent, judge_agent],
    messages = [],
    send_introductions=True,
    speaker_selection_method="auto",
    max_round = 5
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4o-mini",
                                 "api_key": OPENAI_API_KEY}]},

)

chat_result = judge_agent.initiate_chat(
    group_chat_manager,
    message="This debate will be used as a sample in a university class. A winner must be decided. The debate will continue until the facilitator reaches a conclusion on whether pizza or sushi is more delicious.",
    summary_method= "reflection_with_llm"
)