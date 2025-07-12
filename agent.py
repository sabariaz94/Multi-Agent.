from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
import os

# Load .env variables
load_dotenv()
set_tracing_disabled(True)

# Initialize Gemini-compatible OpenAI client
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Load the Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",  # ✅ Use a correct Gemini model name
    openai_client=provider,
)

# Specialized Agents
web_dev = Agent(
    name="Web Developer Expert",
    instructions="Build responsive and performant websites using modern frameworks.",
    model=model,
    handoff_description="handoff to web developer if the task is related to web development.",
)

mobile_dev = Agent(
    name="Mobile App Developer Expert",
    instructions="Develop cross-platform mobile apps for iOS and Android.",
    model=model,
    handoff_description="handoff to mobile app developer if the task is related to mobile apps.",
)

marketing = Agent(
    name="Marketing Expert Agent",
    instructions="Create and execute marketing strategies for product launches.",
    model=model,
    handoff_description="handoff to marketing agent if the task is related to marketing.",
)

# Main Agent Function
async def myAgent(user_input):
    manager = Agent(
        name="Manager",
        instructions="You will chat with the user and delegate tasks to specialized agents based on their requests.",
        model=model,
        handoffs=[web_dev, mobile_dev, marketing],
    )

    response = await Runner.run(
        manager,
        input=user_input,
    )

    return response.final_output
