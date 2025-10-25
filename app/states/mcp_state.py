import reflex as rx
from typing import TypedDict, Optional


class ToolParameter(TypedDict):
    name: str
    type: str
    required: bool


class Tool(TypedDict):
    name: str
    description: str
    parameters: list[ToolParameter]
    output: str


class MCP(TypedDict):
    id: str
    name: str
    description: str
    tools: list[Tool]


class MCPState(rx.State):
    expanded_mcp_index: int = -1
    expanded_tool_index: int = -1
    mcps: list[MCP] = [
        {
            "id": "general_tools",
            "name": "General Purpose Tools",
            "description": "A collection of common tools for everyday tasks.",
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get the current weather for a specific location. For this demo, it provides a forecast for Madrid.",
                    "parameters": [
                        {"name": "city", "type": "string", "required": True}
                    ],
                    "output": """{
  "city": "Madrid",
  "temperature": "25\x08°C",
  "condition": "Sunny",
  "humidity": "30%"
}""",
                }
            ],
        },
        {
            "id": "data_analysis",
            "name": "Data Analysis Toolkit",
            "description": "Tools for processing and analyzing data from various sources.",
            "tools": [
                {
                    "name": "read_csv",
                    "description": "Reads a CSV file and returns its content as a list of dictionaries.",
                    "parameters": [
                        {"name": "file_path", "type": "string", "required": True}
                    ],
                    "output": """[
  {"name": "John Doe", "age": "30"},
  {"name": "Jane Smith", "age": "25"}
]""",
                },
                {
                    "name": "calculate_mean",
                    "description": "Calculates the mean of a list of numbers.",
                    "parameters": [
                        {"name": "data", "type": "list[float]", "required": True}
                    ],
                    "output": """{
  "mean": 45.5
}""",
                },
            ],
        },
        {
            "id": "content_creation",
            "name": "Content Creation Suite",
            "description": "A set of tools to assist in generating and managing content.",
            "tools": [
                {
                    "name": "summarize_text",
                    "description": "Summarizes a long piece of text into a few key sentences.",
                    "parameters": [
                        {"name": "text", "type": "string", "required": True}
                    ],
                    "output": '"AI agents are transforming industries by automating complex tasks. Their success depends heavily on the quality of context provided to them, with MCPs being a key standard for this."',
                }
            ],
        },
    ]

    @rx.event
    def toggle_mcp_expand(self, index: int):
        if self.expanded_mcp_index == index:
            self.expanded_mcp_index = -1
            self.expanded_tool_index = -1
        else:
            self.expanded_mcp_index = index
            self.expanded_tool_index = -1

    @rx.event
    def toggle_tool_expand(self, index: int):
        if self.expanded_tool_index == index:
            self.expanded_tool_index = -1
        else:
            self.expanded_tool_index = index