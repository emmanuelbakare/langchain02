import os
import re
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv

load_dotenv()

#Setup the directroy where all projects will live
PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
os.makedirs(PROJECT_DIR, exist_ok=True)

#project folder naming tool
def name_project(project_name:str)->str:
    """
    Create a project folder with the given name.

    Call this FIRST before writing any files. The name should be short, descriptive,
    lowercase slug using hyphens (e.g., 'email-validator', 'todo-api','csv-parser).
    The folder should be created under ./projects/.

    Args:
        project_name: A short, lowercase, hyphenated name for the project
    """

    #sanitize project name
    slug = project_name.lower().strip()
    slug = re.sub(r"[\s_]+","-", slug) # change any underscore to an hyphen
    slug = re.sub(r"[^a-z0-9-]","", slug) # remove any character that is not alpha numberic
    slug = slug.strip("-")

    if not slug:
        return " Error: Could not create a valid project name. Try a descriptive name like 'email-validator'"
    
    project_path = os.path.join(PROJECT_DIR, slug)
    os.makedirs(project_path, exist_ok=True)

    return {
        "status": "success",
        "project_name": slug,
        "path": project_path,
        "message": f"Project folder created: {slug}/"
    }
    # return f"Project folder created: {slug}/\nWrite all files into this folder using the folder name prefix - e.g. write-file('{slug}/main.py',...)"



REVIEW_PROMPT = """
    You are an expert Python code reviewer. You will be given a task describing which files to review. 
    Use ls to find the files, then use read_file to read each one and provide a structured review.

    ## Review Checklist:
    1. **Correctness** - Are there logic errors or bugs
    2. **Edge cases** - Does the code handle empty inputs, None values, boundary conditions?
    3. **Style** - Does it follow Python conventions (PEP 8, clear naming, docstrings)?
    4. **Type hints** - Are function singatures properly annotated?
    5. **Simplicity** - Can anything be simplified without lossing clarity?

    Also check that a README.md exisits and is accurate.

    ## Output format

    for each file, respond with:
    
    **File: filename.py**
    - Status:  PASS or NEEDS CHANGES
    - Issues (list each issue with line reference and suggested fix)
    - Strengthen: (what the code foes well)

    If all files pass, say "All filess pass review -code is ready for delivery."

    Keep your review concise and actionable. DO NOT rewrite the code -just describe the issues.
    """

code_reviewer = {
    "name": "code-reviewer",
    "description": "Review Python code for bugs, style issues, and best practices. Use when code has been written and needs a quality check before delivery.",
    "system_prompt": REVIEW_PROMPT,
    "tools" : []
}


SYSTEM_PROMPT = """
You are a senior Python developer. Your job is to take coding tasks from the user and produce clean,
 well-structured Python projects.

 ## Your Workflow

 1. **Name the project.** Use the name_project tool with a short, descriptive slug (e.g. 'email-validator', 'palindrome-checker'). This create the project folder. 
 After naming, write all files using the folder name as a path prefix (e.g. write_file('my-project/main.py',...)).
 2. **Plan** Use write_todos to break the task into clear implementation steps.
 3. *Write code**. Save all code files using write_file. Use descriptive filename. Always include docstring and type hints
 4. **Write README.md** Create a README.md file that includes: 
    - A brief description of what the project does
    - setup instructions:

    ```
        python -m venv venv
        # Linux/Mac call
        source venv/bin/activate
        # Windows call
        venv\Scripts\activate
        pip install -r requirements.txt. #only if there are dependencies
    ```
    - How to run the program (.e.g "python main.py)
    - Example output (if applicable)
5. **Write requirements.txt** if the project uses any third-party packages. If it only uses the standard library, skip this file.
6. *Request a review.** Delegate a code review to the 'code-reviewer' subagent using the task tool. In your task description, tell it to use ls and review all files
7. **Apply fixes.** Read the review feedback carefully. If the reviewer flagged issues, use edit_file to fix each one. If the review is clean, skip to step 8.
8. **Deliver.** After all fixes are applied.
    a. Use ls to confirm the final list of files.
    b. Tell the user the project folder name and how to get started (point them to the README)
    c. Update your to-do list to mark everything as completed.

## Guidelines
- Write production-quality code - not pseudocde or sketches.
- Each function should do one thing well.
- Include a biref module-level docstring explaining the files purpose
- If the task is complex, split it across multiple files with a clear entry point.
- Always update your to-do list as you progress
"""

checkpointer  = MemorySaver()

model = ChatOpenAI(
    model="gpt-4o-mini",
    max_retries= 3,
    request_timeout = 60
)

agent = create_deep_agent(
    model = model,
    system_prompt=SYSTEM_PROMPT,
    tools = [name_project],
    subagents= [code_reviewer],
    backend= FilesystemBackend(root_dir=PROJECT_DIR, virtual_mode=True),
    checkpointer= checkpointer
)

def main():
    print("SIMPLE CODING AGENT")
    print("PLAN ->WRITE ->REVIEW -> FIX ->DElIVER")
    print("="*60)
    print()
    print(f"Project will be save to :{PROJECT_DIR}/")
    print()
    print("Describe a coding task: Type 'quit' to exit")
    print()

    task_count = 0
    while True:
        user_input = input("> ").strip()

        if user_input.lower() in ('quit','exit','q'):
            print("Goodbye")
            break

        if not user_input:
            continue

        task_count += 1
        config = {"configurable":{"thread_id":task_count}}

        print()
        print("="*60)
        print("Agent is working..")
        print("="*60)
        print()

        for step in agent.stream(
            {"messages":[{"role":"user", "content": user_input}]},
            config,
            stream_mode = "updates"
        ):
            for node_name, update in step.items():
                if update and (messages := update.get("messages")):
                    for message in (
                        messages if isinstance(messages, list) else [messages]
                    ):
                        if isinstance(message, BaseMessage):
                            message.pretty_print()
        print()


if __name__=="__main__":
    main()

