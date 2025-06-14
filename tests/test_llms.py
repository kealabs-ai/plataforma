import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llms.base_llm import BaseLLM
from llms.openai_llm import OpenAILLM
from llms.gemini_llm import GeminiLLM
from llms.llm_factory import LLMFactory

class TestLLMFactory:
    """Testes para a fábrica de LLMs."""
    
    def test_get_openai_llm(self):
        """Testa se a fábrica retorna o LLM correto para OpenAI."""
        with patch.object(OpenAILLM, '__init__', return_value=None):
            llm = LLMFactory.get_llm("gpt")
            assert isinstance(llm, OpenAILLM)
    
    def test_get_gemini_llm(self):
        """Testa se a fábrica retorna o LLM correto para Gemini."""
        with patch.object(GeminiLLM, '__init__', return_value=None):
            llm = LLMFactory.get_llm("gemini")
            assert isinstance(llm, GeminiLLM)
    
    def test_fallback_to_openai(self):
        """Testa se a fábrica usa OpenAI como fallback para modelos desconhecidos."""
        with patch.object(OpenAILLM, '__init__', return_value=None):
            llm = LLMFactory.get_llm("unknown_model")
            assert isinstance(llm, OpenAILLM)

class TestOpenAILLM:
    """Testes para o LLM da OpenAI."""
    
    @patch('requests.post')
    def test_generate(self, mock_post):
        """Testa a geração de texto com o LLM da OpenAI."""
        # Configura o mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Resposta de teste"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Testa a geração
        with patch.object(OpenAILLM, 'validate_api_key', return_value=True):
            llm = OpenAILLM(api_key="test_key")
            response = llm.generate("Olá, como vai?")
            
            assert response == "Resposta de teste"
            mock_post.assert_called_once()

# Mais testes seriam adicionados aqui para cobrir outras funcionalidades dos LLMs