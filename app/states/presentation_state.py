import reflex as rx
from typing import TypedDict, Literal, Union


class TextSlide(TypedDict):
    type: Literal["text"]
    title: str
    content: list[str]
    image: Literal[""]


class ImageSlide(TypedDict):
    type: Literal["image"]
    title: str
    image: str
    content: list[str]


Slide = Union[TextSlide, ImageSlide]


class PresentationState(rx.State):
    current_slide: int = 0
    slides: list[Slide] = [
        {
            "type": "text",
            "title": "Introducción a Agentes de IA",
            "content": [
                "Una nueva era en la automatización inteligente.",
                "Más allá de los modelos de lenguaje tradicionales.",
                "Capaces de razonar, planificar y ejecutar tareas complejas.",
            ],
            "image": "",
        },
        {
            "type": "text",
            "title": "¿Qué son los Agentes?",
            "content": [
                "Sistemas de software que perciben su entorno y actúan de forma autónoma para alcanzar objetivos.",
                "Componentes clave: LLM (cerebro), Percepción, Planificación, Memoria y Herramientas (actuadores).",
                "Ejemplos: asistentes personales, automatización de flujos de trabajo, análisis de datos complejos.",
            ],
            "image": "",
        },
        {
            "type": "image",
            "title": "Visualizing Agent Architecture",
            "content": [],
            "image": "https://images.unsplash.com/photo-1677756119517-756a188d2d94?q=80&w=2070&auto=format&fit=crop",
        },
        {
            "type": "text",
            "title": "Ingeniería de Contexto",
            "content": [
                "El arte y la ciencia de proporcionar al agente la información correcta en el momento adecuado.",
                "Un buen contexto es crucial para la precisión y relevancia de las respuestas del agente.",
                "Va más allá del 'prompt engineering' tradicional.",
            ],
            "image": "",
        },
        {
            "type": "image",
            "title": "Context is Key",
            "content": [],
            "image": "https://images.unsplash.com/photo-1556075798-4825dfaaf498?q=80&w=2070&auto=format&fit=crop",
        },
        {
            "type": "text",
            "title": "Técnicas de Ingeniería de Contexto",
            "content": [
                "Recuperación de Información (RAG - Retrieval-Augmented Generation).",
                "Uso de Bases de Datos Vectoriales para búsquedas semánticas.",
                "Construcción de Grafos de Conocimiento.",
                "Integración con APIs y herramientas externas.",
            ],
            "image": "",
        },
        {
            "type": "text",
            "title": "MCPs (Model Context Protocols)",
            "content": [
                "Un protocolo estandarizado para estructurar y presentar el contexto a los modelos de lenguaje.",
                "Define cómo se deben formatear y organizar los datos, el conocimiento y las capacidades (herramientas).",
                "Facilita la interoperabilidad y el rendimiento de los agentes.",
            ],
            "image": "",
        },
        {
            "type": "text",
            "title": "Beneficios de MCPs",
            "content": [
                "Mejora la fiabilidad y consistencia del agente.",
                "Reduce la 'alucinación' y las respuestas incorrectas.",
                "Permite a los modelos entender y utilizar herramientas de manera más efectiva.",
                "Simplifica el desarrollo y la depuración de agentes complejos.",
            ],
            "image": "",
        },
        {
            "type": "image",
            "title": "The Future is Autonomous",
            "content": [],
            "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2070&auto=format&fit=crop",
        },
        {
            "type": "text",
            "title": "Conclusión",
            "content": [
                "Los agentes de IA, impulsados por una sólida ingeniería de contexto y protocolos como MCPs, están listos para revolucionar industrias.",
                "La clave del éxito reside en la calidad del contexto que proporcionamos.",
                "El futuro es de los sistemas autónomos e inteligentes.",
            ],
            "image": "",
        },
    ]

    @rx.var
    def current_slide_data(self) -> Slide:
        return self.slides[self.current_slide]

    @rx.var
    def progress(self) -> float:
        if not self.slides:
            return 0
        return (self.current_slide + 1) / len(self.slides) * 100

    @rx.event
    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1

    @rx.event
    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1

    @rx.event
    def go_to_slide(self, index: int):
        if 0 <= index < len(self.slides):
            self.current_slide = index