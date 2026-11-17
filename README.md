# TicketPilot – Week 1: First Tool-Calling LLM Call

A small Python script where an LLM decides to call a function
(`lookup_order_status`) instead of just replying with text.

## What is a tool call?
A tool call is when the model, instead of answering directly, returns a
structured request such as "call `lookup_order_status` with
`order_id="A123"`". The model never runs code itself. My script runs the
function and sends the result back so the model can write a grounded answer.

## Flow
1. User asks: "What's the status of order A123?"
2. The script sends the message plus the tool schema to the model.
3. The model replies with a tool call (name + JSON arguments).
4. The script runs `lookup_order_status` on the hardcoded order data.
5. The result is sent back as a `tool` message.
6. The model returns a final natural-language answer.

## Files
- `main.py` – tool function, tool schema, and glue code
- `.env` – holds `GROQ_API_KEY` (not committed)

## Setup
pip install groq python-dotenv
Create a `.env` file:
GROQ_API_KEY=your_key_here

## Run
python main.py

Try:
- `What's the status of order A123?` → tool-grounded answer
- `Status of order Z999?` → tool returns "not found" and the model says so

## Tech
Python, Groq API (openai/gpt-oss-20b), python-dotenv