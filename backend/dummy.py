from business_logic.models.llm_models import deepseek, askDeepseek
from data.db_data_short import db_summary
from data.prompt_templates import template_prompt

conversation_prompts = [
    "Add 3 plus 3",
    "good morning!",
    "if it s raining, should i grab an umbrella?",
    "Insert an adjective before the noun in this sentence: Do you see that house?",
    "Retrieve a list with all US Presidents",
    "Delete all consonants from the word evrica",
    "What time it is?"
]

retrieve_prompts = [
    "Should I grab an umbrella if it s raining outside?",
    "Get the total number of orders placed by user with user_id = 3.",
    "Find the product with the highest price in the database.",
    "Retrieve all products ordered by user with user_id = 5.",
    "Get the total number of units sold for each product."
]

insert_prompts = [
    "Insert a new user with the name 'Alice Johnson', age 30, and registration date '2025-04-25'.",
    "Add a new product named 'SmartWatch 5' with price $299 and description 'A smartwatch with advanced features'.",
    "Insert an order for user_id = 4 placed on '2025-04-26'.",
    "Add 3 units of product_id = 2 to order_id = 10 in the orders_content table.",
    "Insert a new product 'UltraPhone X' with a price of $999 and description 'Flagship phone with top features'."
]

update_prompts = [
    "Update the price of 'UltraPhone 3000' to $749.",
    "Set the email address of user 'Jane Doe' to 'jane.updated@example.com'.",
    "Update the quantity of 'SmartWatch Pro' to 150 units in the inventory.",
    "Modify the status of order '1023' to 'Shipped'.",
    "Update the rating for the product 'Laptop Model X' to 4."
]

delete_prompts = [
    "Delete the user 'Jane Doe' from the database.",
    "Remove the order with ID '1023' from the orders table.",
    "Delete the product 'UltraPhone 3000' from the product catalog.",
    "Delete the oldest user.",
    "Remove all records of orders placed before 2020 from the database."
]

all_prompts = conversation_prompts + retrieve_prompts + insert_prompts + update_prompts + delete_prompts

formatted_prompts = [template_prompt.format(prompt=p, db_info=db_summary, ai_response="") for p in all_prompts]

for idx, formatted_prompt in enumerate(formatted_prompts, start=1):
    print(f"Prompt {idx}:")
    response = askDeepseek(formatted_prompt)
    print(response)

