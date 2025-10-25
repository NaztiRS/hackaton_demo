import reflex as rx
from typing import TypedDict, cast
import logging
from app.tools.weather import get_weather
from app.states.mcp_state import MCPState, MCP


class Message(TypedDict):
    role: str
    content: str


class ChatState(rx.State):
    messages: list[Message] = []
    is_processing: bool = False
    is_thinking: bool = False
    _agent = None
    attached_files: list[str] = []
    active_mcps: dict[str, bool] = {
        "general_tools": True,
        "data_analysis": False,
        "content_creation": False,
    }

    def _get_agent(self):
        if self._agent is None:
            from agno.agent import Agent
            from agno.models.openai import OpenAIChat

            self._agent = Agent(model=OpenAIChat(id="gpt-4o"), tools=[get_weather])
        return self._agent

    @rx.event
    async def process_message(self, form_data: dict):
        from agno.agent import RunEvent

        user_input = form_data.get("user_input")
        if not user_input or not user_input.strip():
            return
        self.is_processing = True
        self.messages.append({"role": "user", "content": user_input})
        self.messages.append({"role": "thinking", "content": ""})
        self.is_thinking = True
        yield
        try:
            agent = self._get_agent()
            response_stream = agent.arun(user_input, stream=True, stream_events=True)
            assistant_message_started = False
            async for chunk in response_stream:
                if self.is_thinking:
                    self.messages.pop()
                    self.is_thinking = False
                    yield
                if chunk.event == RunEvent.tool_call_started:
                    self.messages.append(
                        {
                            "role": "tool",
                            "content": f"Calling tool: `{chunk.tool.tool_name}` with arguments: `{chunk.tool.tool_args}`",
                        }
                    )
                    yield
                elif chunk.event == RunEvent.run_content:
                    if not assistant_message_started:
                        self.messages.append(
                            {"role": "assistant", "content": chunk.content}
                        )
                        assistant_message_started = True
                    else:
                        self.messages[-1]["content"] += chunk.content
                    yield
        except Exception as e:
            if self.is_thinking:
                self.messages.pop()
                self.is_thinking = False
            logging.exception(f"Error processing message: {e}")
            self.messages.append(
                {"role": "assistant", "content": f"An error occurred: {str(e)}"}
            )
        finally:
            if self.is_thinking:
                self.messages.pop()
                self.is_thinking = False
            self.is_processing = False
            yield rx.call_script(
                "document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight"
            )

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            self.attached_files.append(file.name)
        yield rx.clear_selected_files("chat_upload")

    @rx.event
    def toggle_mcp(self, mcp_id: str):
        self.active_mcps[mcp_id] = not self.active_mcps[mcp_id]

    @rx.event
    def remove_attachment(self, filename: str):
        self.attached_files.remove(filename)

    @rx.var
    async def mcps(self) -> list[MCP]:
        mcp_state = await self.get_state(MCPState)
        return mcp_state.mcps