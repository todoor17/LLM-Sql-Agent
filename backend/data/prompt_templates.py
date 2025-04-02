template_prompt = """
This is the user's prompt: '{initial_prompt}'. It can be in various languages. If it is in a language other than English, translate it into English.
This is the database structure: {db_info}

First, double-check if the prompt is related to database operations. Analyze the prompt and strictly respond with one of the following based on its contents:

- *ERROR* if the prompt is not database-related or tables do not exist in the database structure.
- *INSERT* if the prompt contains any of: insert, add, create, new, register, introduce, enter, store, save, append, put, establish, initialize, generate, make, load, populate, enroll, submit, post
- *RETRIEVE* if the prompt contains any of: get, find, show, list, return, select, fetch, query, search, lookup, extract, obtain, view, display, print, read, check, verify, examine, scan
- *DELETE* if the prompt contains any of: delete, remove, get rid of, erase, wipe, clear, cut, eliminate, etc., **but only if the target table(s) exist(s) in the database structure**.
- *UPDATE* if the prompt contains any of: update, change, modify, edit, revise, adjust, alter, transform, replace, enhance, refactor and so on.
Respond with exactly one of: *INSERT*, *RETRIEVE*, *DELETE*, *ERROR* and no other word. The output will strictly be one of these 4 options.

Note: If the target table does not exist in the database, return *ERROR* instead of *DELETE*.
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


