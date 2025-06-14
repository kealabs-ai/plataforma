import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
import google.api_core.exceptions as google_exceptions

from .base_llm import BaseLLM

# Carrega variáveis de ambiente
load_dotenv()

class GeminiLLMError(Exception):
    """Custom exception for GeminiLLM errors."""
    pass

class GeminiLLM(BaseLLM):
    """Implementação do LLM usando a API do Google Gemini."""

    DEFAULT_GENERATION_MODEL = "gemini-1.5-flash-latest"
    DEFAULT_EMBEDDING_MODEL = "models/text-embedding-004"

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY")
        super().__init__(api_key=api_key, **kwargs)

        if not self.api_key: # self.api_key should be set by BaseLLM
            raise ValueError("Google Gemini API key não configurada (GOOGLE_GEMINI_API_KEY).")

        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise GeminiLLMError(f"Falha ao configurar a API Key do Google Gemini: {e}") from e

        self.generation_model_name = kwargs.get("model", self.DEFAULT_GENERATION_MODEL)
        self.embedding_model_name = kwargs.get("embedding_model", self.DEFAULT_EMBEDDING_MODEL)

        if not self.validate_api_key():
            raise ValueError("Validação da Google Gemini API key falhou (método validate_api_key da BaseLLM).")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Gera uma resposta usando a API do Google Gemini.
        
        Args:
            prompt: O texto de entrada para o modelo.
            **kwargs: Parâmetros adicionais para a API.
                      Pode incluir 'model', 'temperature', 'max_tokens',
                      'top_p', 'top_k', 'safety_settings'.

        Returns:
            str: A resposta gerada pelo modelo.

        Raises:
            GeminiLLMError: Se ocorrer um erro durante a geração.
        """
        model_to_use = kwargs.get("model", self.generation_model_name)

        gen_config_params = {
            "temperature": kwargs.get("temperature", 0.7),
            "max_output_tokens": kwargs.get("max_tokens", 2048), # SDK usa max_output_tokens
            "top_p": kwargs.get("top_p", 0.95),
            "top_k": kwargs.get("top_k", 40)
        }
        # Filtra None para não passar explicitamente para GenerationConfig se não definido
        gen_config_params = {k: v for k, v in gen_config_params.items() if v is not None}
        generation_config = GenerationConfig(**gen_config_params)

        safety_settings = kwargs.get("safety_settings")

        try:
            sdk_model_instance = genai.GenerativeModel(model_to_use)
            response = sdk_model_instance.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            if not response.candidates:
                feedback = response.prompt_feedback
                block_reason_message = f"Razão: {feedback.block_reason.name}" if feedback.block_reason else "Razão desconhecida."
                safety_ratings_message = f" Avaliações de segurança: {feedback.safety_ratings}" if feedback.safety_ratings else ""
                raise GeminiLLMError(
                    f"Geração de conteúdo bloqueada ou sem candidatos. {block_reason_message}{safety_ratings_message}"
                )
            return response.text
        except (google_exceptions.GoogleAPIError, ValueError, GeminiLLMError) as e:
            raise GeminiLLMError(f"Erro ao gerar resposta com Gemini: {str(e)}") from e
        except Exception as e: # Captura outros erros inesperados
            raise GeminiLLMError(f"Erro inesperado ao gerar resposta com Gemini: {str(e)}") from e

    def get_embedding(self, text: str) -> List[float]:
        """
        Obtém o embedding vetorial para o texto fornecido usando a API do Google.

        Args:
            text: O texto para gerar o embedding.
            **kwargs: Pode incluir 'embedding_model', 'task_type'.

        Returns:
            List[float]: O vetor de embedding.

        Raises:
            GeminiLLMError: Se ocorrer um erro durante a geração do embedding.
        """
        embedding_model_to_use = self.embedding_model_name # Usa o modelo padrão da instância
        task_type = "RETRIEVAL_DOCUMENT" # Default task type, pode ser sobrescrito por kwargs se necessário

        try:
            result = genai.embed_content(
                model=embedding_model_to_use,
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except (google_exceptions.GoogleAPIError, KeyError) as e: # KeyError se 'embedding' não estiver no resultado
            raise GeminiLLMError(f"Erro ao gerar embedding com Gemini: {str(e)}") from e
        except Exception as e: # Captura outros erros inesperados
            raise GeminiLLMError(f"Erro inesperado ao gerar embedding com Gemini: {str(e)}") from e