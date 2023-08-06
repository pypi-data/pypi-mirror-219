from src.lemonai import execute_workflow
import os
from langchain import OpenAI


os.environ["OPENAI_API_KEY"] = "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"
# os.environ["AIRTABLE_SECRET_TOKEN"] = "patJoC5EBAvPKdAjY.42c1c66934da89b3935cad9c41c88d7de750101dfcc111e1958a3c679b01599a"
os.environ["GITHUB_API_KEY"] = "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"
os.environ["DISCORD_WEBHOOK_URL"] = "https://discord.com/api/webhooks/1130492847578161222/ZYS1ewlNF1IGEdnKK4TU38wSAF8e4iYUSMlMIBPCPAZDZsiw5XOntZ8JUssAyB6r2Tme"

# prompt = "Get me information for Hackernews user kimburgess"
# prompt = "Read information from Hackernews for user kimburgess and then write the results to Airtable (BaseId: app2VdQRffkyAiIcc, tableId: tblscnilGk6BHVkVn). Only write the fields 'username', 'karma' and 'created_at_i'. Please make sure that Airtable does NOT automatically convert the field types."
# prompt = "Run the Hackernews Airtable User Workflow for user kimburgess, baseId app2VdQRffkyAiIcc and tableId tblscnilGk6BHVkVn. Only write the fields 'username', 'karma' and 'created_at_i' to the Airtable table. Please make sure that Airtable does NOT automatically convert the field types."
# prompt = f"List the names of my starred repositories on Github, and rank the top 5 in descending order of their stargazer_count field. The owner is felixbrock."
# prompt = "List only the names of my starred repositories on Github. Owner is felixbrock"
# prompt = "List the top growing repositories that I have starred (my username is Abdus2609). Then, send a Discord message in a leaderboard format, numerically bullet pointing each repository and its growth. Also, get the description of the repository lemonai (owner felixbrock) and within the Discord message, use the description of each starred repository to explain how each tool would be relevant to lemonai."

# prompt = "Get the description for a repository I am working with called lemonai (owner felixbrock). Also, get my top growing starred repositories (useername Abdus2609). Then, construct and send a Discord message that firstly displays a numerically bullet pointed leaderboard of the top growing starred repositories and their growth, and secondly explains how each tool could be useful to use in lemonai based on your analysis of lemonai's description and the description of each starred repository."
# prompt = "Get the description for a repository I am working with called lemonai (owner felixbrock). Also, get my top growing starred repositories (useername Abdus2609). Analyse the descriptions of both the LemonAI repository and my top starred repositories. Then, send a Discord message that firstly displays a numerically bullet pointed leaderboard of the top growing starred repositories and their growth, and secondly discusses how each tool could be useful specifically to lemonai's use case based on your analysis of the descriptions of each repository."

model = OpenAI(temperature=0)
execute_workflow(model, prompt_string=prompt)