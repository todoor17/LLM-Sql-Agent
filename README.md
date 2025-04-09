# SQL Agent with Open-Source LLMs

![image](https://github.com/user-attachments/assets/85719010-a296-432d-affb-c05477049411)

## Overview

A powerful SQL agent that leverages open-source LLMs (Llama3.2 and Mistral-Nemo) to generate and validate database queries from natural language. Designed as a cost-effective alternative to paid API solutions while maintaining competitive accuracy.

## Key Features

✅ **Open-Source Advantage**  
- Uses free LLMs (Llama3.2 and Mistral-Nemo) instead of paid APIs  
- Multi-step validation ensures result quality comparable to commercial solutions  

🔌 **Database Agnostic**  
- Works with any database schema  
- Simply modify `data.db_info` to connect to your database  

📊 **Current Database Schema**  
![Database Schema](https://github.com/user-attachments/assets/9059a84c-5256-4768-ab8e-1fa0c352de93)  
*Tables: users, products, orders, orders_content*

## Capabilities

### Natural Language to SQL
- "Show me the top 10 most sold products in 2024"
- "Which product did John Stones buy most frequently?"
- "What's the total revenue from electronics last quarter?"

### Data Manipulation
- "Add user: John Stones, age 20, registered May 17, 2014"
- "Update John Stones' age to 69"
- "Delete user John Stones and all associated orders"

### Complex Queries
- "Find customers who purchased more than 5 different products"
- "Calculate monthly sales trends for the past year"
- "Identify products with declining sales"

## How It Works

1. **Natural Language Processing**  
   - Parses user intent from free-form text

2. **Query Generation**  
   - Generates candidate SQL queries using LLMs

3. **Multi-Stage Validation**  
   - Schema compliance checking  
   - Syntax validation  
   - Result sanity checks  

4. **Execution & Feedback**  
   - Runs validated queries  
   - Provides explanations for results  
