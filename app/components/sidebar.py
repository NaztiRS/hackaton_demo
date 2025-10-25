import reflex as rx
from app.states.sidebar_state import SidebarState


def nav_item(text: str, href: str, icon: str, is_active: rx.Var[bool]) -> rx.Component:
    return rx.el.a(
        rx.el.li(
            rx.icon(icon, class_name="h-5 w-5 shrink-0"),
            rx.cond(
                SidebarState.is_collapsed, None, rx.el.span(text, class_name="truncate")
            ),
            class_name=rx.cond(
                is_active,
                "bg-gray-100 text-gray-900 font-semibold",
                "text-gray-600 hover:bg-gray-50 hover:text-gray-900",
            ),
            style={
                "display": "flex",
                "align_items": "center",
                "gap": "0.75rem",
                "padding": "0.5rem 0.75rem",
                "border_radius": "0.375rem",
                "transition": "colors 0.2s",
                "justify_content": rx.cond(
                    SidebarState.is_collapsed, "center", "flex-start"
                ),
            },
        ),
        href=href,
        class_name="block w-full",
    )


def sidebar() -> rx.Component:
    route = rx.State.router.page.path
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("bar-chart-big", class_name="h-8 w-8 text-black"), href="/"
                ),
                rx.el.button(
                    rx.icon("panel-left-close", class_name="h-5 w-5"),
                    on_click=SidebarState.toggle_collapse,
                    class_name="p-2 rounded-md hover:bg-gray-100",
                    style={
                        "display": rx.cond(SidebarState.is_collapsed, "none", "block")
                    },
                ),
                class_name="flex h-16 items-center justify-between border-b px-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("panel-right-close", class_name="h-5 w-5"),
                    on_click=SidebarState.toggle_collapse,
                    class_name="p-2 rounded-md hover:bg-gray-100 self-center mt-4",
                ),
                style={
                    "display": rx.cond(SidebarState.is_collapsed, "flex", "none"),
                    "justify_content": "center",
                },
            ),
        ),
        rx.el.nav(
            rx.el.ul(
                nav_item("Presentation", "/", "file_sliders", route == "/"),
                nav_item("Chat Agent", "/chat", "message_circle", route == "/chat"),
                nav_item("MCP", "/mcp", "file_code_2", route == "/mcp"),
                nav_item("Docs", "/docs", "folder_kanban", route == "/docs"),
                class_name="space-y-1",
            ),
            class_name="flex-1 overflow-auto p-2",
        ),
        class_name="flex flex-col min-h-0 border-r bg-white h-screen shrink-0 transition-all duration-300",
        style={"width": rx.cond(SidebarState.is_collapsed, "4rem", "16rem")},
    )