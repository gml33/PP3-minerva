import json
import logging
import os
from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


logger = logging.getLogger(__name__)


class IAProcessingError(Exception):
    """Error genérico al procesar links con IA."""


@dataclass
class AnalisisIA:
    categorias: List[str]
    resumen: str
    confianza: float


class LinkAIProcessor:
    """Orquesta la descarga del artículo y la consulta a la IA."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise IAProcessingError(
                "No se configuró la variable de entorno OPENAI_API_KEY."
            )
        if OpenAI is None:
            raise IAProcessingError(
                "La librería openai no está disponible en el entorno."
            )
        self.client = OpenAI(api_key=api_key)

    def extraer_texto(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as exc:  # pragma: no cover
            logger.error("No se pudo descargar el contenido de %s: %s", url, exc)
            raise IAProcessingError(
                f"No se pudo descargar el contenido del link {url}"
            ) from exc

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        texto = " ".join(soup.stripped_strings)
        if not texto:
            raise IAProcessingError("No se pudo extraer contenido del link.")
        return texto[:5000]

    def analizar(self, url: str, texto: str) -> AnalisisIA:
        prompt = (
            "Analizá el artículo provisto y devolvé únicamente un JSON con este formato: "
            '{"categorias": ["categoria 1", "categoria 2"], '
            '"resumen": "Resumen en español del artículo (máximo 80 palabras).", '
            '"confianza": 0.0}. '
            "Las categorías deben corresponder a secciones periodísticas (Política, Economía, Seguridad, Sociedad, "
            "Internacional, Cultura, Deportes, etc.). "
            "Confianza es un número entre 0 y 1. "
            f"URL: {url}\n\n"
            f"Contenido:\n\"\"\"\n{texto}\n\"\"\""
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Sos un clasificador periodístico que responde estrictamente en formato JSON válido.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=500,
            )
            contenido = response.choices[0].message.content  # type: ignore[attr-defined]
        except Exception as exc:  # pragma: no cover
            logger.error("Fallo consultando a OpenAI: %s", exc)
            raise IAProcessingError("No se pudo obtener la respuesta de la IA.") from exc

        try:
            data = json.loads(contenido)
        except json.JSONDecodeError as exc:
            logger.error("La IA devolvió un JSON inválido: %s", contenido)
            raise IAProcessingError("La respuesta de la IA no pudo interpretarse.") from exc

        categorias = [c.strip() for c in data.get("categorias", []) if c.strip()]
        resumen = data.get("resumen", "").strip()
        confianza = float(data.get("confianza", 0))
        return AnalisisIA(
            categorias=categorias,
            resumen=resumen,
            confianza=max(0, min(confianza, 1)),
        )
