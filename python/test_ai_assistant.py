from ai_assistant import build_prompt, ask_llm, clean_sql, run_sql


def answer(question):
    sql = clean_sql(ask_llm(build_prompt(question)))
    return run_sql(sql)


result = answer("Which region makes the highest profit?")
assert result.iloc[0, 0] == "South"

result = answer("What is the total profit?")
assert round(result.iloc[0, 0], 2) == 42763505.14

print("All tests passed")
