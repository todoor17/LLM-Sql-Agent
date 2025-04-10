from queue import Queue

from business_logic.models import llm_models
from typing import Dict, List
from typing_extensions import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from data.db_data import db_info
from business_logic.models.llm_models import askMistral, model
from business_logic.database.db_connector import do_db_retrieve, do_db_insert, do_db_delete, do_db_update
from data.prompt_templates import template_prompt, template_prompt_1, template_prompt_2, template_prompt_4, template_prompt_5
from data.prompt_templates import template_check_correct_update, template_check_correct_delete, template_prompt_chat, template_prompt_natural_language_response

llm_model = llm_models.model

class State(TypedDict):
    prompt: str
    database_info: Dict[str, str]
    type: str
    answer: str
    status: str
    correct: bool
    suggested_new_query: str
    sql_answer: str
    insert_status: str
    all_fields_present: bool
    missing_fields: str
    success_answer: str
    conversation_flag: bool
    user_messages: List[str]
    ai_messages: List[str]

queue = Queue()

def get_query(state: State):
    global queue

    if not queue.empty():
        state["prompt"] = queue.get()
        print(state["prompt"])
    else:
        if state["status"] == "UNRELATED DELETE":
            state["prompt"] = input(f"You introduced a DELETE PROMPT that is not related to the database.\nPlease retry: ")
        elif state["prompt"] == "" or state["status"] == "START":
            state["prompt"] = input("Enter your prompt: \n")
        elif state["prompt"] != "" and state["type"] == "ERROR":
            state["prompt"] = input("You introduced an INCORRECT PROMPT. Please retry: \n")
        elif state["prompt"] != "" and state["type"] != "ERROR" and state["missing_fields"] != "":
            state["prompt"] = input(f"{state['missing_fields']}. Retry: \n")
        elif state["conversation_flag"]:
            state["prompt"] = input("\nEnter your prompt / message: \n")


    # translate_prompt = template_prompt_translate.format(initial_prompt=state["prompt"], db_info=db_info)
    # new_prompt = askMistral(translate_prompt)
    # print(new_prompt)
    #
    # state["prompt"] = new_prompt

    state["status"] = ""
    state["all_fields_present"] = True
    state["missing_fields"] = ""
    state["conversation_flag"] = False

    return state


def check_query_type(state: State):
    prompt = template_prompt.format(initial_prompt=state['prompt'], db_info=db_info, last_ai_response=state['ai_messages'][:-1])
    llm_response = askMistral(prompt).upper()
    # print(llm_response)

    if "INSERT" in llm_response:
        state["type"] = "INSERT"
    elif "RETRIEVE" in llm_response:
        state["type"] = "RETRIEVE"
    elif "DELETE" in llm_response:
        state["type"] = "DELETE"
    elif "UPDATE" in llm_response:
        state["type"] = "UPDATE"
    elif "CONVERSATION" in llm_response:
        state["type"] = "CONVERSATION"
    else:
        state["type"] = "ERROR"

    return state


def do_type_route(state: State):
    if state["type"] == "RETRIEVE":
        print("goes to retrieve\n")
        return "RETRIEVE"
    elif state["type"] == "INSERT":
        print("goes to insert\n")
        return "INSERT"
    elif state["type"] == "DELETE":
        print("goes to delete\n")
        return "DELETE"
    elif state["type"] == "UPDATE":
        print("goes to update\n")
        return "UPDATE"
    elif state["type"] == "CONVERSATION":
        # print("goes to conversation\n")
        return "CONVERSATION"
    elif state["type"] == "ERROR":
        print("ERROR. GRAPH ENDS HERE")
        return "ERROR"


def do_retrieve(state: State):
    retrieve_prompt = template_prompt_1.format(initial_prompt=state['prompt'], db_info=db_info, suggested_new_query=state['suggested_new_query'])
    llm_result = askMistral(retrieve_prompt)
    print(llm_result)
    print("\n")

    try:
        db_result = do_db_retrieve(llm_result)
        state["sql_answer"] = db_result
        state["answer"] = llm_result
        state["status"] = "SUCCESS"
        return state
    except Exception as e:
        state["status"] = "ERROR"
        return state


def do_retrieve_route(state: State):
    if state["status"] == "SUCCESS":
        print("goes to check_correct_retrieve")
        return "SUCCESS"
    elif state["status"] == "ERROR":
        return "ERROR"


def check_correct_retrieve(state: State):
    print("entered check retrieve query correctness")
    check_prompt = template_prompt_2.format(initial_prompt = state["prompt"], answer=state["answer"], db_info=db_info)
    check_response = askMistral(check_prompt)
    print(check_response)

    if "yes" in check_response or "Yes" in check_response or "YES" in check_response:
        state["correct"] = True
    elif "no" in check_response or "No" in check_response or "NO" in check_response:
        state["correct"] = False
        suggested_fix = "\n".join(state["suggested_new_query"].split("\n")[1:])
        state["suggested_new_query"] = suggested_fix

    return state


def check_retrieve_correctness_route(state: State):
    if state["correct"]:
        print("the program goes in print_result state\n")
        return "CORRECT"
    else:
        print("the program returns in do_retrieve\n")
        return "INCORRECT"


def check_for_all_fields(state: State):
    print("\nentered check_for_all_fields")
    check_prompt = template_prompt_4.format(initial_prompt=state["prompt"], db_info=db_info)
    check_response = askMistral(check_prompt).lower()
    print(check_response)

    if "all matched" in check_response:
        state["all_fields_present"] = True
        state["missing_fields"] = ""
    else:
        state["all_fields_present"] = False
        state["missing_fields"] = check_response

    return state


def check_for_all_fields_route(state: State):
    return str(state["all_fields_present"])


def do_insert(state: State):
    insert_prompt = template_prompt_5.format(initial_prompt=state["prompt"], db_info=db_info)
    insert_response = askMistral(insert_prompt)
    print(insert_response)

    try:
        do_db_insert(insert_response)
        state["status"] = "SUCCESS"
        return state
    except Exception as e:
        state["status"] = "ERROR"
        return state


def do_insert_route(state: State):
    return state["status"]


def check_correct_delete(state: State):
    print("entered check correct delete")
    response = askMistral(template_check_correct_delete.format(initial_prompt=state["prompt"], db_info = db_info)).lower()
    new_response = response

    #formatting the response if it contains markdowns
    if response.startswith("```"):
        response = response.split("\n")
        response = response[1:-1]
        new_response = "\n".join(unit for unit in response)

    if "no" in response:
        state["status"] = "UNRELATED DELETE"
    else:
        state["status"] = "SUCCESS"
        state["answer"] = new_response

    return state


def check_correct_delete_route(state: State):
    print("Entered check_correct_delete_route")
    return state["status"]


def do_delete(state: State):
    print("entered deleting part")
    print(state["answer"])
    try:
        do_db_delete(state["answer"])
        state["status"] = "SUCCESS"
        return state
    except Exception as e:
        state["status"] = "WRONG DELETE QUERY"
        return state
    pass


def do_delete_route(state: State):
    print("Entered do_delete_route")
    return state["status"]


def check_correct_update(state: State):
    print("entered check correct update")
    prompt = template_check_correct_update.format(initial_prompt=state["prompt"], db_info=db_info)
    response = askMistral(prompt).lower()
    new_response = response

    if response.startswith("```"):
        new_response = response.split("\n")[1:-1]

    if "no" in response:
        state["status"] = "UNRELATED UPDATE"
    else:
        state["status"] = "SUCCESS"
        state["answer"] = new_response

    print(new_response)
    return state


def check_correct_update_route(state: State):
    return state["status"]

def do_update(state: State):
    print("entered updating part")
    print(state["answer"])
    try:
        do_db_update(state["answer"])
        state["status"] = "SUCCESS"
        return state
    except Exception as e:
        state["status"] = "WRONG UPDATE QUERY"
        return state


def do_update_route(state: State):
    return state["status"]

def print_result(state: State):
    print_prompt = template_prompt_natural_language_response.format(prompt=state["prompt"], db_info=db_info, sql_answer=state["answer"], sql_answer_value=state["sql_answer"])
    result = askMistral(print_prompt)

    print(result)

    # choice is used when user runs llm_sql_agent with text, not with voice (from frontend)
    # choice = input("\nEnter 0 to exit the program\nEnter 1 to introduce another prompt\n\n")
    # choice = 0
    #
    # if choice == "0":
    #     state["status"] = "end"
    # else:
    #     state.update({
    #         "prompt": "",
    #         "type": "",
    #         "answer": "",
    #         "status": "restart",
    #         "sql_answer": "",
    #         "missing_fields": ""
    #     })

    return state

def conversation(state: State):
    # print("entered conversation")

    current_message = state["prompt"]

    human_messages = "\n".join(f"HUMAN MESSAGE[{index}]: " + message for index, message in enumerate(state["user_messages"][:3]))
    ai_messages = "\n".join(f"AI RESPONSE[{index}]: " + message for index, message in enumerate(state["ai_messages"][:3]))

    chat_prompt = template_prompt_chat.format(current_message=current_message, human_messages=human_messages, db_info=db_info, ai_messages=ai_messages)
    response = askMistral(chat_prompt)

    state["user_messages"].append(current_message)
    state["ai_messages"].append(response)

    print(response)

    state["conversation_flag"] = True
    return state


def print_result_route(state: State):
    print("\nEntered print_result_route\n")
    return state["status"]

builder = StateGraph(State)
builder.add_node("get_query", get_query)
builder.add_node("check_query_type", check_query_type)
builder.add_node("do_retrieve", do_retrieve)
builder.add_node("check_for_all_fields", check_for_all_fields)
builder.add_node("check_correct_retrieve", check_correct_retrieve)
builder.add_node("do_insert", do_insert)
builder.add_node("do_delete", do_delete)
builder.add_node("check_correct_delete", check_correct_delete)
builder.add_node("do_update", do_update)
builder.add_node("check_correct_update", check_correct_update)
builder.add_node("print_result", print_result)
builder.add_node("conversation", conversation)

builder.add_edge(START, "get_query")

builder.add_edge("get_query", "check_query_type")

builder.add_conditional_edges("check_query_type", do_type_route, {
    "RETRIEVE": "do_retrieve",
    "INSERT": "check_for_all_fields",
    "DELETE": "check_correct_delete",
    "UPDATE": "check_correct_update",
    "CONVERSATION": "conversation",
    "ERROR": "get_query"
})

builder.add_edge("conversation", "get_query")

builder.add_conditional_edges("check_for_all_fields", check_for_all_fields_route, {
    "True": "do_insert",
    "False": "get_query"
})

builder.add_conditional_edges("do_insert", do_insert_route, {
    "SUCCESS": "print_result",
    "ERROR": "do_insert"
})

builder.add_conditional_edges("do_retrieve", do_retrieve_route, {
    "ERROR": "do_retrieve",
    "SUCCESS": "check_correct_retrieve"
})

builder.add_conditional_edges("check_correct_retrieve", check_retrieve_correctness_route, {
    "CORRECT": "print_result",
    "INCORRECT": "do_retrieve"
})

builder.add_conditional_edges("check_correct_delete", check_correct_delete_route, {
    "UNRELATED DELETE": "get_query",
    "SUCCESS": "do_delete"
})

builder.add_conditional_edges("do_delete", do_delete_route, {
    "SUCCESS": "print_result",
    "WRONG DELETE QUERY": "check_correct_delete",
})

builder.add_conditional_edges("check_correct_update", check_correct_update_route, {
    "UNRELATED UPDATE": "check_correct_update",
    "SUCCESS": "do_update"
})

builder.add_conditional_edges("do_update", do_update_route, {
    "SUCCESS": "print_result",
    "WRONG UPDATE QUERY": "check_correct_update",
})

builder.add_edge("do_update", "print_result")

# builder.add_conditional_edges("print_result", print_result_route, {
#     "restart": "get_query",
#     "end": END
# })

builder.add_edge("print_result", END)

graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="diagram.png")

keyboard_input = input("Enter your prompt / message here:\n")

initial_state = {
    "database_info": db_info,
    "type": "",
    "answer": "",
    "status": "",
    "correct": False,
    "suggested_new_query": "",
    "all_fields_present": True,
    "missing_fields": "",
    "prompt": keyboard_input,
    "success_answer": "",
    "sql_answer": "",
    "insert_status": "",
    "conversation_flag": False,
    "user_messages": [],
    "ai_messages": [],
}

graph.invoke(initial_state, {"recursion_limit": 100})
