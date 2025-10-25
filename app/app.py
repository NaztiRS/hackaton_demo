import reflex as rx
from app.states.presentation_state import PresentationState
from app.components.sidebar import sidebar
from app.states.sidebar_state import SidebarState


def slide_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="w-full bg-gray-200 rounded-full h-1.5"),
                rx.el.div(
                    class_name="bg-black h-1.5 rounded-full transition-all duration-1000 ease-in-out",
                    style={"width": PresentationState.progress.to_string() + "%"},
                ),
                class_name="relative w-full mb-6",
            ),
            rx.match(
                PresentationState.current_slide_data["type"],
                (
                    "image",
                    rx.el.div(
                        rx.image(
                            src=PresentationState.current_slide_data["image"],
                            class_name="w-full h-full object-cover",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                PresentationState.current_slide_data["title"],
                                class_name="text-2xl font-bold text-white",
                            ),
                            class_name="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-black/80 to-transparent",
                        ),
                        class_name="relative w-full h-full animate-in fade-in-0 duration-700",
                        key=PresentationState.current_slide.to_string()
                        + "-image-slide",
                    ),
                ),
                (
                    "text",
                    rx.el.div(
                        rx.el.h1(
                            PresentationState.current_slide_data["title"],
                            class_name="text-4xl font-bold text-gray-900 mb-4 animate-in fade-in-50 slide-in-from-bottom-5 duration-1000",
                            key=PresentationState.current_slide.to_string() + "-title",
                        ),
                        rx.el.ul(
                            rx.foreach(
                                PresentationState.current_slide_data["content"],
                                lambda item, index: rx.el.li(
                                    rx.icon(
                                        "square_check",
                                        class_name="h-5 w-5 text-green-500 mr-3 shrink-0",
                                    ),
                                    rx.el.span(
                                        item, class_name="text-lg text-gray-600"
                                    ),
                                    class_name="flex items-start mb-2 animate-in fade-in-50 slide-in-from-bottom-5 duration-1000",
                                    style={"animation_delay": f"{200 + index * 150}ms"},
                                ),
                            ),
                            class_name="list-none p-0 mb-8",
                            key=PresentationState.current_slide.to_string()
                            + "-content",
                        ),
                        class_name="w-full",
                    ),
                ),
                rx.el.div("Invalid slide type"),
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        PresentationState.slides,
                        lambda _, index: rx.el.button(
                            on_click=lambda: PresentationState.go_to_slide(index),
                            class_name=rx.cond(
                                PresentationState.current_slide == index,
                                "w-3 h-3 bg-black rounded-full transition-all scale-125",
                                "w-3 h-3 bg-gray-300 rounded-full transition-all hover:bg-gray-400",
                            ),
                        ),
                    ),
                    class_name="flex items-center justify-center gap-3",
                ),
                class_name="absolute bottom-8 left-1/2 -translate-x-1/2",
            ),
            class_name="relative flex flex-col justify-center h-full p-12 w-full max-w-2xl mx-auto",
        ),
        class_name="flex w-full h-[500px] md:h-full bg-white rounded-2xl shadow-md overflow-hidden items-center justify-center",
    )


def presentation_view() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                slide_content(),
                key=PresentationState.current_slide.to_string(),
                class_name="w-full h-full",
            ),
            rx.el.button(
                rx.icon("arrow-left", class_name="h-6 w-6"),
                on_click=PresentationState.prev_slide,
                is_disabled=PresentationState.current_slide == 0,
                class_name="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full shadow-lg hover:bg-white hover:scale-105 focus:ring-2 focus:ring-black focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all",
            ),
            rx.el.button(
                rx.icon("arrow-right", class_name="h-6 w-6"),
                on_click=PresentationState.next_slide,
                is_disabled=PresentationState.current_slide
                == PresentationState.slides.length() - 1,
                class_name="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full shadow-lg hover:bg-white hover:scale-105 focus:ring-2 focus:ring-black focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all",
            ),
            class_name="relative w-full h-full max-w-4xl max-h-[600px] aspect-[16/9]",
        ),
        class_name="flex-1 p-4 md:p-6 bg-gray-100 flex items-center justify-center",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        presentation_view(),
        class_name="flex min-h-screen w-screen font-['Inter']",
    )


from app.states.chat_state import ChatState


def message_bubble(message: dict) -> rx.Component:
    is_user = message["role"] == "user"
    is_assistant = message["role"] == "assistant"
    is_user = message["role"] == "user"
    is_assistant = message["role"] == "assistant"
    is_tool_call = message["role"] == "tool"
    is_thinking = message["role"] == "thinking"
    return rx.match(
        message["role"],
        (
            "tool",
            rx.el.div(
                rx.el.div(
                    rx.icon("flask-round", class_name="h-4 w-4 mr-2"),
                    rx.el.p(message["content"], class_name="text-sm italic"),
                    class_name="flex items-center text-gray-500",
                ),
                class_name="flex w-full justify-center my-2",
            ),
        ),
        (
            "thinking",
            rx.el.div(
                rx.el.div(
                    rx.el.span(class_name="animate-pulse"),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce",
                            style={"animation_delay": "0s"},
                        ),
                        rx.el.div(
                            class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce",
                            style={"animation_delay": "0.2s"},
                        ),
                        rx.el.div(
                            class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce",
                            style={"animation_delay": "0.4s"},
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="bg-gray-100 text-gray-800 p-3 rounded-2xl",
                    style={"max_width": "70%"},
                ),
                class_name="flex w-full",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(message["content"], class_name="text-sm"),
                class_name=rx.cond(
                    is_user,
                    "bg-black text-white p-3 rounded-2xl",
                    "bg-gray-100 text-gray-800 p-3 rounded-2xl",
                ),
                style={"max_width": "70%"},
            ),
            class_name=rx.cond(is_user, "flex w-full justify-end", "flex w-full"),
        ),
    )


def chat_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.foreach(ChatState.messages, message_bubble),
                class_name="flex flex-col gap-4 p-4 overflow-y-auto h-full",
                id="chat-messages",
                style={"scroll_behavior": "smooth"},
            ),
            class_name="flex-1 h-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    ChatState.attached_files,
                    lambda f: rx.el.div(
                        rx.el.span(f, class_name="text-xs font-medium"),
                        rx.el.button(
                            rx.icon("x", class_name="h-3 w-3"),
                            on_click=lambda: ChatState.remove_attachment(f),
                            class_name="p-0.5 rounded-full hover:bg-gray-200",
                        ),
                        class_name="flex items-center gap-1.5 bg-gray-100 rounded-full pl-2 pr-1 py-0.5",
                    ),
                ),
                class_name="flex flex-wrap gap-2 px-4 pb-2",
            ),
            rx.el.form(
                rx.upload.root(
                    rx.el.button(
                        rx.icon("paperclip", class_name="h-5 w-5"),
                        type="button",
                        class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                    ),
                    id="chat_upload",
                    on_drop=ChatState.handle_upload(
                        rx.upload_files(upload_id="chat_upload")
                    ),
                    multiple=True,
                ),
                rx.el.input(
                    placeholder="Ask the agent...",
                    name="user_input",
                    class_name="flex-1 bg-transparent focus:outline-none text-sm font-medium",
                    disabled=ChatState.is_processing,
                ),
                rx.el.button(
                    rx.cond(
                        ChatState.is_processing,
                        rx.spinner(class_name="h-5 w-5 border-gray-400"),
                        rx.icon("arrow-up", class_name="h-5 w-5"),
                    ),
                    type="submit",
                    class_name="p-2 rounded-full bg-black text-white disabled:bg-gray-300 disabled:cursor-not-allowed",
                    disabled=ChatState.is_processing,
                ),
                on_submit=ChatState.process_message,
                reset_on_submit=True,
                class_name="flex items-center w-full p-2 border border-gray-200 rounded-full bg-white shadow-sm focus-within:ring-2 focus-within:ring-black",
            ),
            rx.el.div(
                rx.el.p("Active MCPs:", class_name="text-xs font-semibold mr-4"),
                rx.foreach(
                    ChatState.mcps,
                    lambda mcp: rx.el.div(
                        rx.el.button(
                            rx.icon(
                                rx.cond(ChatState.active_mcps[mcp["id"]], "check", ""),
                                class_name="h-3.5 w-3.5",
                            ),
                            on_click=lambda: ChatState.toggle_mcp(mcp["id"]),
                            class_name=rx.cond(
                                ChatState.active_mcps[mcp["id"]],
                                "w-5 h-5 rounded border border-blue-600 bg-blue-600 text-white flex items-center justify-center",
                                "w-5 h-5 rounded border border-gray-300 bg-white",
                            ),
                        ),
                        rx.el.span(mcp["name"], class_name="text-xs text-gray-600"),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex items-center justify-start gap-4 pt-3 px-4",
            ),
            class_name="pt-2 pb-4 bg-white/80 backdrop-blur-md",
        ),
        class_name="flex flex-col h-full w-full max-w-lg mx-auto bg-gray-50 rounded-2xl shadow-md",
    )


def chat() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            chat_view(),
            class_name="flex-1 p-6 bg-gray-100 flex items-center justify-center",
        ),
        class_name="flex min-h-screen w-screen font-['Inter']",
    )


from app.states.mcp_state import MCPState


def code_block(code: str, language: str) -> rx.Component:
    return rx.el.div(
        rx.el.pre(
            rx.el.code(code.strip(), class_name=f"language-{language} p-4"),
            class_name=f"bg-gray-800 rounded-lg my-2 overflow-x-auto text-sm",
        ),
        class_name="w-full",
    )


def tool_card(tool: dict, index: int) -> rx.Component:
    is_expanded = MCPState.expanded_tool_index == index
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("wrench", class_name="h-5 w-5 text-gray-500"),
                rx.el.span(tool["name"], class_name="font-semibold text-gray-800"),
                class_name="flex items-center gap-3",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    is_expanded,
                    "transform rotate-180 transition-transform",
                    "transition-transform",
                ),
            ),
            on_click=lambda: MCPState.toggle_tool_expand(index),
            class_name="flex items-center justify-between w-full p-3 text-left bg-gray-50 rounded-md",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Description",
                        class_name="font-semibold text-gray-700 mb-1 text-sm",
                    ),
                    rx.el.p(tool["description"], class_name="text-sm text-gray-600"),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Parameters",
                        class_name="font-semibold text-gray-700 mb-2 text-sm",
                    ),
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Name",
                                    class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Type",
                                    class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                                rx.el.th(
                                    "Required",
                                    class_name="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase",
                                ),
                                class_name="bg-gray-100",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                tool["parameters"],
                                lambda param: rx.el.tr(
                                    rx.el.td(
                                        param["name"],
                                        class_name="px-3 py-2 text-sm text-gray-800 font-mono",
                                    ),
                                    rx.el.td(
                                        param["type"],
                                        class_name="px-3 py-2 text-sm text-gray-600 font-mono",
                                    ),
                                    rx.el.td(
                                        param["required"].to_string(),
                                        class_name="px-3 py-2 text-sm",
                                    ),
                                ),
                            ),
                            class_name="bg-white divide-y divide-gray-200",
                        ),
                        class_name="min-w-full divide-y divide-gray-200 border rounded-lg overflow-hidden",
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Example Output",
                        class_name="font-semibold text-gray-700 mb-2 text-sm",
                    ),
                    code_block(tool["output"], "json"),
                ),
                class_name="p-3 border-t",
            ),
            class_name=rx.cond(is_expanded, "max-h-[500px]", "max-h-0"),
            style={"overflow": "hidden", "transition": "max-height 0.5s ease-in-out"},
        ),
        class_name="border rounded-lg bg-white overflow-hidden my-2 shadow-sm",
    )


def mcp_card(mcp: dict, index: int) -> rx.Component:
    is_mcp_expanded = MCPState.expanded_mcp_index == index
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("box", class_name="h-6 w-6 text-gray-600"),
                rx.el.div(
                    rx.el.h2(
                        mcp["name"], class_name="font-semibold text-lg text-gray-900"
                    ),
                    rx.el.p(mcp["description"], class_name="text-sm text-gray-500"),
                    class_name="text-left",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.icon(
                "chevron-down",
                class_name=rx.cond(
                    is_mcp_expanded,
                    "transform rotate-180 transition-transform",
                    "transition-transform",
                ),
            ),
            on_click=lambda: MCPState.toggle_mcp_expand(index),
            class_name="flex items-center justify-between w-full p-4 text-left bg-white rounded-lg shadow-md hover:bg-gray-50 transition",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(mcp["tools"], lambda tool, i: tool_card(tool, i)),
                class_name="p-4",
            ),
            class_name=rx.cond(is_mcp_expanded, "max-h-screen", "max-h-0"),
            style={"overflow": "hidden", "transition": "max-height 0.7s ease-in-out"},
        ),
        class_name="border rounded-lg overflow-hidden bg-white",
    )


def mcp_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("file_code_2", class_name="h-10 w-10 text-gray-400"),
                        class_name="flex justify-center p-4 bg-gray-100 rounded-full mb-4",
                    ),
                    rx.el.h1(
                        "Model Context Protocols (MCPs)",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Available tools and their specifications, grouped by protocol.",
                        class_name="text-gray-600",
                    ),
                    class_name="text-center mb-8",
                ),
                rx.el.div(
                    rx.foreach(MCPState.mcps, lambda mcp, index: mcp_card(mcp, index)),
                    class_name="space-y-4 w-full max-w-3xl",
                ),
            ),
            class_name="flex-1 p-6 bg-gray-50 flex items-start justify-center overflow-y-auto",
        ),
        class_name="flex min-h-screen w-screen font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.states.docs_state import DocsState


def docs_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.aside(
                    rx.el.div(
                        rx.el.h2("Documents", class_name="text-lg font-semibold mb-4"),
                        rx.upload.root(
                            rx.el.div(
                                rx.icon(
                                    "cloud_upload",
                                    class_name="h-6 w-6 text-gray-500 mb-2",
                                ),
                                rx.el.p(
                                    "Drop files here or click to upload",
                                    class_name="text-sm text-gray-600",
                                ),
                                class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50 transition-colors",
                            ),
                            id="docs_upload",
                            multiple=True,
                            on_drop=DocsState.handle_upload(
                                rx.upload_files(upload_id="docs_upload")
                            ),
                            accept={
                                "text/plain": [".txt"],
                                "text/markdown": [".md"],
                                "application/json": [".json"],
                            },
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                rx.selected_files("docs_upload"),
                                lambda file: rx.el.div(
                                    file, class_name="text-xs p-1 bg-gray-100 rounded"
                                ),
                            ),
                            class_name="space-y-1 mb-4",
                        ),
                        rx.el.hr(class_name="my-4"),
                        rx.el.div(
                            rx.foreach(
                                DocsState.doc_files,
                                lambda doc: rx.el.button(
                                    rx.icon("file_text", class_name="h-4 w-4 mr-2"),
                                    rx.el.span(doc, class_name="truncate"),
                                    on_click=lambda: DocsState.select_doc(doc),
                                    class_name=rx.cond(
                                        DocsState.selected_doc == doc,
                                        "w-full flex items-center text-left p-2 rounded-md bg-gray-100 font-semibold text-gray-900",
                                        "w-full flex items-center text-left p-2 rounded-md hover:bg-gray-100 text-gray-700",
                                    ),
                                ),
                            ),
                            class_name="flex flex-col gap-1",
                        ),
                        class_name="w-64 border-r bg-white p-4 flex flex-col h-full",
                    ),
                    rx.el.div(
                        rx.cond(
                            DocsState.selected_doc == "",
                            rx.el.div(
                                rx.icon(
                                    "mouse_pointer",
                                    class_name="h-12 w-12 text-gray-400 mb-4",
                                ),
                                rx.el.h3(
                                    "Select a document",
                                    class_name="text-lg font-semibold text-gray-700",
                                ),
                                rx.el.p(
                                    "Choose a document from the left to view its content.",
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center h-full text-center",
                            ),
                            rx.el.div(
                                rx.el.h1(
                                    DocsState.selected_doc,
                                    class_name="text-2xl font-bold mb-4 pb-2 border-b",
                                ),
                                rx.cond(
                                    DocsState.is_loading,
                                    rx.spinner(class_name="h-8 w-8"),
                                    rx.el.pre(
                                        rx.el.code(
                                            DocsState.selected_doc_content,
                                            class_name="text-sm",
                                        ),
                                        class_name="bg-gray-50 p-4 rounded-lg overflow-x-auto",
                                    ),
                                ),
                                class_name="p-6",
                            ),
                        ),
                        class_name="flex-1 h-full overflow-y-auto",
                    ),
                ),
                class_name="flex h-full w-full bg-white rounded-2xl shadow-md overflow-hidden",
            ),
            class_name="flex-1 p-6 bg-gray-100 flex items-center justify-center",
            on_mount=DocsState.on_load,
        ),
        class_name="flex min-h-screen w-screen font-['Inter']",
    )


app.add_page(index, route="/")
app.add_page(chat, route="/chat")
app.add_page(mcp_page, route="/mcp")
app.add_page(docs_page, route="/docs")