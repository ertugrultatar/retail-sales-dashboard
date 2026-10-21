from ai_assistant import ask_llm, run_sql

sql = ask_llm("Which region makes the highest profit?")
result = run_sql(sql)

assert result["region"][0] == "South"

sql = ask_llm("What is the total profit?")
result = run_sql(sql)

assert round(result["SUM(profit)"][0], 2) == 42763505.14

print("All tests passed")
