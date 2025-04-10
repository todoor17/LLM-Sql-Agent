template_prompt = """
Analyze the following user prompt and database structure to determine the appropriate operation type:

USER PROMPT: '{initial_prompt}'
DATABASE STRUCTURE: {db_info}
LAST AI RESPONSE: {last_ai_response}

INSTRUCTIONS:
1. Context Analysis:
   - First check if this is a follow-up to the last AI response
   - Then determine if the prompt is a general knowledge question or conversation
   - If not conversation and not in English, translate it to English
   - Perform all subsequent analysis on the processed version

2. Operation Classification:
   Strictly respond with ONLY ONE of the following:

   *CONVERSATION* if:
   - The prompt is a direct follow-up to {last_ai_response}
   - It's a general knowledge question (math, facts, etc.)
   - It's conversational (greetings, opinions, etc.)
   - No database tables are referenced
   - It references previous non-DB context
   (Examples: "What's 3+3?", "Hello", "How are you?", "About what you just said...")

   *INSERT*/*RETRIEVE*/*UPDATE*/*DELETE* only if:
   - The prompt explicitly references NEW database operations
   - Required tables exist in {db_info}
   - Not building on previous non-DB conversation
   (Follow original keyword rules for these)

   *ERROR* only if:
   - Prompt attempts database operations but tables don't exist
   - Contains harmful/unsupported requests

3. Special Cases:
   - Follow-ups to non-DB responses → *CONVERSATION*
   - Math operations without DB context → *CONVERSATION* 
   - References to previous answers → *CONVERSATION*
   - Mixed prompts (DB + general) → Prefer *CONVERSATION*

4. Output Rules:
   - ONLY respond with the tag, no explanations
   - Valid tags: *INSERT*, *RETRIEVE*, *UPDATE*, *DELETE*, *CONVERSATION*, *ERROR*

Examples:
Last AI: "3+3 equals 6"
Input: "Now divide by 2" → *CONVERSATION*

Last AI: "Users table contains 5 records" 
Input: "Show me those users" → *RETRIEVE*

Last AI: "Hello there!"
Input: "How are you?" → *CONVERSATION*

Input: "Delete customers" → *DELETE* (if table exists) or *ERROR*
"""

template_prompt_1 = """
# PostgreSQL Query Generation Prompt

"I need a PostgreSQL query that fulfills this request: {initial_prompt}

It is possible this to be a generation retry. If so, here is a suggested_new_query: {suggested_new_query}. Take it into consideration. If no, skip it.

## Database Context
Database structure can be found here: {db_info}

## Goal
- Create a valid PostgreSQL query matching the user's request
- Use only the specified tables/columns with proper joins
- Validate all foreign key relationships
- Return ONLY the raw SQL query (no explanations)

## Return Format
A single PostgreSQL query in plain text format

## Warnings
- Reject any tables/columns not in the provided schema
- Ensure proper joins using the documented relationships
- Validate date constraints
- Check age non-negativity requirements
- Handle decimal precision for price calculations

## Context Dump
User seeks data about: {initial_prompt}
Special considerations: 
- Age must be non-negative
- Price calculations need proper decimal handling
"""

template_prompt_2 = """
# Query Validation Prompt

"I need to verify if this PostgreSQL query: {answer}
accurately solves: {initial_prompt}. Modify it only if the answer would be wrong. If it s a small mistake that doesn't affect the result, skip it.

## Database Context
Database structure can be found here: {db_info}

## Goal
- Confirm query matches all user requirements
- Identify schema mismatches or logic errors
- Validate all joins and constraints
- Check for proper date filtering 

## Return Format
First line: 'yes' or 'no' 
Second line: Error explanation (if 'no') + fix suggestion
Modify it only if the answer would be wrong. If it s a small mistake that doesn't affect the result, skip it.

## Warnings
- Flag incorrect table/column references
- Catch invalid joins missing relationship paths
- Verify date constraints 
- Check age non-negativity enforcement
- Validate decimal handling for price calculations

## Context Dump
Query purpose: {initial_prompt}
Critical constraints:
- User ages cannot be negative
- Price calculations require precision
"""

template_prompt_3 = """
User's prompt: {initial_prompt}
The query was executed correctly. It was a {type} query.
Provide a one line conclusion about the prompt and say it was a successful operation.
"""

template_prompt_4 = """
Database structure: {db_info}
Prompt: "{initial_prompt}". If prompt contains two names, they are basically the first_name and the last_name in that order.

Perform this analysis:
1. Identify which table (users/products/orders/orders_content) the prompt targets
2. Check if all required fields for that table are provided
3. Skip any _id fields (they're auto-generated)
4. Return EXACTLY one line:
   - If complete: "all matched"
   - If incomplete: "You must introduce all [table_name] fields: [required_fields]"

Required fields per table:
- users: first_name, last_name, age, registration_date
- products: product_name, product_desc, price
- orders: user_id, date
- orders_content: order_id, product_id, units
"""

template_prompt_5 = """
# PostgreSQL INSERT Query Generation Prompt
I need a PostgreSQL INSERT query that fulfills this request: {initial_prompt}

## Database Context
Database structure is available here: {db_info}.

## Goal
- Construct a valid PostgreSQL `INSERT` query that resolves the user's request
- Use only the specified tables/columns while maintaining foreign key integrity
- Ensure all required fields are included for a successful insertion
- Return ONLY the raw SQL query (no explanations)

## Return Format
A single PostgreSQL `INSERT` query in plain text format

## Warnings
- Reject any tables/columns not listed in the schema
- Ensure all required fields are provided
- Validate date constraints 
- Ensure proper handling of numeric values (e.g., age non-negative, price as decimal)
- Maintain relational integrity when inserting related records

## Context Dump
User's request: {initial_prompt}
Database Structure: {db_info}
"""

template_prompt_delete = """
I need a PostgreSQL DELETE query that fulfills this request: {initial_prompt}

## Database Context
Database structure is available here: {db_info}.

## Goal
- Construct a valid PostgreSQL `DELETE` query that resolves the user's request.
- Use only the specified tables/columns while maintaining foreign key integrity.
- When you check values, for strings check all lowercase / uppercase / starting with capital (If you delete user with first_name adrian, check for all "Adrian", "ADRIAN", "adrian').
- Ensure the correct rows are targeted for deletion.
- Return ONLY the raw SQL query (no explanations).

## Return Format
A single PostgreSQL `DELETE` query in plain text format.

## Warnings
- Reject any tables/columns not listed in the schema.
- Ensure the right rows are affected by the delete operation.
- Validate the conditions for deleting (e.g., only valid records for deletion).
- Maintain relational integrity when deleting records that are linked by foreign keys.

## Context Dump
User's request: {initial_prompt}  
Database Structure: {db_info}
"""

template_check_correct_delete = """
Database schema: {db_info}
User's prompt: {initial_prompt}

### Strict Validation Protocol:
1. Validate natural language prompt:
   - Must contain ALL required elements:
     a) Clear table reference (users/products/orders/orders_content)
     b) Specific record identifier (name/id/unique condition)
3. FINALLY verify schema compliance:
   - All referenced tables/columns must exist in {db_info}

### Case-Insensitive Handling:
- Names like 'Todor Ioan' must match any case variation (TODOR, todor, etc.) via LOWER()/ILIKE.

### Absolute Rules:
- Missing table reference or identifier → "no"
- Schema violations → "no"

### Response Format:
ONLY "no" OR a valid DELETE query like:
DELETE FROM users WHERE LOWER(first_name) = LOWER('Todor') AND LOWER(last_name) = LOWER('Ioan');
NO MARKDOWN/EXPLANATIONS
"""

template_check_correct_update = """
Database schema: {db_info}
User's prompt: '{initial_prompt}'

### Strict Validation Protocol:
1. FIRST check if input contains complete SQL statement:
   - If input looks like raw SQL (contains UPDATE/SET/WHERE) → IMMEDIATELY return "no"
2. THEN validate natural language prompt:
   - Must contain ALL required elements:
     a) Clear table reference (users/products/orders/orders_content)
     b) At least one column-value pair
     c) Specific record identifier
   - Must NOT contain SQL keywords
3. FINALLY verify schema compliance:
   - All referenced tables/columns must exist in {db_info}
   - Value types must match column definitions

### Case-Insensitive Handling:
- Names like 'Todor Ioan' must match any case variation via LOWER()/ILIKE.

### Absolute Rules:
- Input containing SQL → "no"
- Missing any requirement (table/column/value/identifier) → "no"
- Schema violations → "no"

### Response Format:
ONLY "no" OR a valid UPDATE query like:
UPDATE users SET age = 69 WHERE first_name ILIKE 'todor' AND last_name ILIKE 'ioan';
NO MARKDOWN/EXPLANATIONS
"""

template_prompt_translate = """
User prompt: {initial_prompt}.
Database structure: {db_info}. Use it for context.

Translate this prompt to technical English following these rules:
0. Keep the original meaning of the prompt.
1. If non-English → Literal technical translation
2. If English → Precise technical rephrasing
3. Output ONLY the final prompt (no explanations, no quotes)
4. Keep all names/values exactly as provided
"""

template_prompt_chat = """
# CONTEXT
You are QueryMate, an AI assistant that helps with both general conversations and database queries. 
Database schema available: {db_info}

# CONVERSATION HISTORY
Human messages: {human_messages}
AI messages (LLM's previous responses): {ai_messages}

# CURRENT MESSAGE
Human: {current_message}

# INSTRUCTIONS
1. Response Style:
   - Be concise (1-3 sentences)
   - Use natural, friendly language
   - Maintain consistent personality
   - If referencing DB schema, keep it brief

2. Special Cases:
   - For math/questions: Show working steps ("3+3=6")
   - For greetings: Respond warmly but briefly
   - For unclear messages: Ask for clarification
   - For DB-related questions: Acknowledge you can help with that

3. Rules:
   - NEVER include tags like *CONVERSATION*
   - DON'T mention you're an AI unless asked
   - DON'T list options unless requested
   - ALWAYS respond in complete sentences

4. Output Format:
   Just your response text, nothing else.

# EXAMPLES
Human: "Hi there!" 
AI: "Hello! How can I help you today?"

Human: "What's 3+3?"
AI: "3 plus 3 equals 6."

Human: "Can you show me users?"
AI: "I can retrieve user data for you. Would you like me to do that?"

# YOUR RESPONSE:
"""

template_prompt_natural_language_response = """
This is user's prompt: {prompt}
This is our database's structure: {db_info}. Use it for context.
This is the SQL answer generated for the prompt: {sql_answer}.
This is the value returned by the SQL query: {sql_answer_value}.

I want you to generate some natural language response based on the user's prompt and the values returned by the SQL query, using database info and SQL answer for context.
"""
