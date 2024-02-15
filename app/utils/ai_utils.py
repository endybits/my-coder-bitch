import asyncio
from openai import OpenAI

client = OpenAI()

async def thread_coder_assistant(
    thread_id: str = None,
    assistant_id: str = None,
    user_message: str = None,
):
    model = "gpt-4-0125-preview"
    if not thread_id or len(thread_id) == 0:
        thread = client.beta.threads.create()
        thread_id = thread.id
    if not assistant_id or len(assistant_id) == 0:
        assistant = client.beta.assistants.create(
            name="Coder Assistant",
            description="A funny coder assistant",
            model=model
        )
        assistant_id = assistant.id
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )
    print("Creating new run...")
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model=model
    )

    print("Waiting for response", end='')
    coder_assistan_answer = ''
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            for message in messages.data:
                if message.role == "assistant":
                    coder_assistan_answer = message.content[0].text.value
                    break
            break
        await asyncio.sleep(1)
        print(".", end='')
    print("\n")
    print(coder_assistan_answer)
    return {
        "thread_id": thread_id,
        "assistant_id": assistant_id,
        "coder_assistan_answer": coder_assistan_answer
    }