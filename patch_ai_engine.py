with open('backend/services/extraction/core/ai_engine.py', 'r') as f:
    content = f.read()

import_statement = "from google.api_core.exceptions import DeadlineExceeded"
new_import_statement = "from google.api_core.exceptions import DeadlineExceeded, ResourceExhausted"
content = content.replace(import_statement, new_import_statement)

exception_block = """            except DeadlineExceeded as e:
                if attempt == max_retries - 1:
                    raise e # Exhausted retries
                await asyncio.sleep(2) # Backoff before retrying
                print(f"Vision AI Timeout (Attempt {attempt + 1}). Retrying...")"""

new_exception_block = """            except DeadlineExceeded as e:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(2)
                print(f"Vision AI Timeout (Attempt {attempt + 1}). Retrying...")
            except ResourceExhausted as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"Gemini Free Tier Rate Limit Hit (Attempt {attempt + 1}). Pausing for 40 seconds...")
                await asyncio.sleep(40) # Pause safely beyond the 35 second API penalty window
                print("Resuming extraction...")"""

content = content.replace(exception_block, new_exception_block)

with open('backend/services/extraction/core/ai_engine.py', 'w') as f:
    f.write(content)

print("Patched AI engine to handle 429 automatically.")
