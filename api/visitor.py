from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from config import GOOGLE_GEMINI_API_KEY, API_PORT, DOCKER_ENV

# Carrega variáveis de ambiente
load_dotenv()

# Cria o router para as rotas do visitor
router = APIRouter(prefix="/visitor", tags=["visitor"])

# Modelos Pydantic
class ChatRequest(BaseModel):
    message: str
    sector: Optional[str] = None
    fileData: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str

def format_llm_response(text: str) -> str:
    """
    Aplica formatação HTML às respostas da LLM
    """
    import re
    
    # Títulos (## Título -> <h3>Título</h3>)
    text = re.sub(r'^## (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    
    # Negrito (**texto** -> <strong>texto</strong>)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Itálico (*texto* -> <em>texto</em>)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Bullet points (- item -> <li>item</li>)
    lines = text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        if re.match(r'^\s*[-*]\s+', line):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            item = re.sub(r'^\s*[-*]\s+', '', line)
            formatted_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            formatted_lines.append(line)
    
    if in_list:
        formatted_lines.append('</ul>')
    
    # Quebras de linha
    text = '\n'.join(formatted_lines)
    text = text.replace('\n\n', '<br><br>')
    text = text.replace('\n', '<br>')
    
    return text

@router.post("/audio-chat")
async def audio_chat(audio: UploadFile = File(...), sector: str = Form("")):
    """
    Endpoint para chat com áudio
    """
    try:
        from llms.gemini_llm import GeminiLLM
        import google.generativeai as genai
        import io
        
        # Lê o conteúdo do arquivo de áudio
        audio_content = await audio.read()
        
        # Usa Gemini para transcrever áudio
        genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
        
        try:
            # Upload do arquivo de áudio para Gemini
            audio_file = genai.upload_file(io.BytesIO(audio_content), mime_type=audio.content_type)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Transcreve o áudio
            response = model.generate_content([
                "Transcreva este áudio para texto em português:",
                audio_file
            ])
            text = response.text
        except Exception as e:
            return {"response": "Erro ao processar áudio. Tente novamente."}
        
        # Processa com Gemini
        gemini_llm = GeminiLLM(api_key=GOOGLE_GEMINI_API_KEY)
        
        prompt_text = ""
        if sector:
            prompt_text += f"O usuário está no setor de {sector}. "
        prompt_text += f"Mensagem de voz transcrita: {text}"
        
        response_text = gemini_llm.generate(prompt_text)
        formatted_response = format_llm_response(response_text)
        
        return {"response": formatted_response, "transcription": text}
        
    except Exception as e:
        print(f"Erro no chat de áudio: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar áudio.")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint para chat com Gemini AI
    """
    print("Recebendo requisição de chat...")
    
    try:
        from llms.gemini_llm import GeminiLLM
        
        # Inicializa o GeminiLLM
        gemini_llm = GeminiLLM(api_key=GOOGLE_GEMINI_API_KEY)
        
        # Constrói o prompt
        prompt_text = ""
        if request.sector:
            prompt_text += f"O usuário está no setor de {request.sector}. "
        
        # Se houver anexo, usa o SDK do Gemini para processar
        if request.fileData:
            import base64
            import google.generativeai as genai
            from PIL import Image
            import io
            
            try:
                decoded_data = base64.b64decode(request.fileData['data'])
                if request.fileData['mimeType'].startswith('text/'):
                    file_content = decoded_data.decode('utf-8')
                    prompt_text += f"Arquivo anexado:\n{file_content}\n\n"
                elif request.fileData['mimeType'].startswith('image/'):
                    # Processa imagem com Gemini Vision
                    image = Image.open(io.BytesIO(decoded_data))
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response_text = model.generate_content([prompt_text + request.message, image]).text
                    formatted_response = format_llm_response(response_text)
                    return ChatResponse(response=formatted_response)
            except Exception as e:
                prompt_text += "Erro ao processar anexo. "
        
        prompt_text += request.message
        
        # Gera resposta usando a camada GeminiLLM
        response_text = gemini_llm.generate(prompt_text)
        
        # Aplica formatação à resposta
        formatted_response = format_llm_response(response_text)
        
        return ChatResponse(response=formatted_response)
        
    except Exception as e:
        print(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail="Erro ao processar chat.")