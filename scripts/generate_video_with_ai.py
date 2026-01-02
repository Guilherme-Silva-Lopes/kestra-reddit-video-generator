"""
Generate video using AI agents (Gemini with GPT fallback) and MCP server
"""
import os
import json
import requests
from kestra import Kestra
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool


def main():
    # Obtém as credenciais e dados
    google_api_key = os.getenv('GOOGLE_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    mcp_server_url = os.getenv('MCP_SERVER_URL')
    
    post_title = """{{ outputs.parse_and_process_feed.vars.post_title }}"""
    post_content = """{{ outputs.parse_and_process_feed.vars.post_content }}"""
    
    # Define a tool MCP para criar vídeo
    @tool
    def create_short_video(title: str, content: str, ai_suggestion: str) -> dict:
        """
        Cria um vídeo curto usando o servidor MCP.
        
        Args:
            title: O título do vídeo
            content: O conteúdo/história para o vídeo
            ai_suggestion: Sugestões da IA para melhorar o vídeo
        
        Returns:
            Dados do vídeo criado incluindo videoId
        """
        mcp_url = f"{mcp_server_url}/api/short-video"
        
        # Estrutura o payload conforme esperado pela API MCP
        payload = {
            "scenes": [
                {
                    "text": content,
                    "duration": 10,
                    "searchTerms": [title]
                }
            ],
            "config": {
                "title": title,
                "voice": "af_nova",
                "backgroundMusic": True,
                "subtitles": True
            }
        }
        
        response = requests.post(
            mcp_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            video_id = result.get('videoId', result.get('id', 'unknown'))
            print(f"✓ Vídeo criado com sucesso! ID: {video_id}")
            return result
        else:
            raise Exception(f"Erro ao criar vídeo: {response.status_code} - {response.text}")
    
    # Configura modelos
    gemini_model = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=google_api_key,
        temperature=0.7
    )
    
    gpt_model = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    
    # System prompt para o agente
    system_prompt = (
        "You are a creative video content creator assistant.\n\n"
        "Your job is to:\n"
        "1. Analyze the provided story/joke\n"
        "2. Adapt it for a text-to-speech video format with subtitles\n"
        "3. Create the video using the create_short_video tool\n"
        "4. Return the video ID and suggested title for YouTube upload\n\n"
        "Keep the content engaging and easy to understand when read aloud."
    )
    
    print(f"📝 Post: {post_title[:50]}...")
    print(f"🎬 Criando vídeo via agente AI + MCP...")
    
    # Tenta usar Gemini primeiro
    model_used = None
    agent_result = None
    
    try:
        print("🤖 Tentando Gemini...")
        agent = create_agent(
            model=gemini_model,
            tools=[create_short_video],
            system_prompt=system_prompt
        )
        
        user_message = (
            f"Turn this story into a video:\n\n"
            f"Title: {post_title}\n\n"
            f"Content: {post_content}\n\n"
            f"Please adapt it slightly for text-to-speech format and create the video."
        )
        
        agent_result = agent.invoke({
            "messages": [
                {"role": "user", "content": user_message}
            ]
        })
        
        model_used = "gemini-3-flash-preview"
        print("✓ Gemini processou com sucesso!")
        
    except Exception as e:
        print(f"✗ Gemini falhou: {e}")
        print("🤖 Usando GPT como fallback...")
        
        try:
            agent = create_agent(
                model=gpt_model,
                tools=[create_short_video],
                system_prompt=system_prompt
            )
            
            user_message = (
                f"Turn this story into a video:\n\n"
                f"Title: {post_title}\n\n"
                f"Content: {post_content}\n\n"
                f"Please adapt it slightly for text-to-speech format and create the video."
            )
            
            agent_result = agent.invoke({
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            })
            
            model_used = "gpt-4o-mini"
            print("✓ GPT processou com sucesso!")
            
        except Exception as e2:
            raise Exception(f"Ambos os modelos falharam. Gemini: {e}, GPT: {e2}")
    
    # Extrai informações do resultado do agente
    # O agente já chamou a tool create_short_video internamente
    messages = agent_result.get("messages", [])
    
    # Procura por tool calls nos resultados
    video_id = "unknown"
    for msg in messages:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            # Pega o resultado da primeira tool call
            tool_result = msg.tool_calls[0]
            print(f"📊 Tool result: {tool_result}")
    
    # Como alternativa, podemos fazer uma chamada direta à API MCP
    # se o agente não retornar o videoId claramente
    print("📡 Chamando API MCP para garantir criação do vídeo...")
    mcp_url = f"{mcp_server_url}/api/short-video"
    
    video_payload = {
        "scenes": [
            {
                "text": post_content,
                "duration": 10,
                "searchTerms": [post_title]
            }
        ],
        "config": {
            "title": post_title,
            "voice": "af_nova",
            "backgroundMusic": True,
            "subtitles": True
        }
    }
    
    video_response = requests.post(
        mcp_url,
        json=video_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if video_response.status_code in [200, 201]:
        video_result = video_response.json()
        video_id = video_result.get('videoId', video_result.get('id', 'unknown'))
        
        print(f"✓ Vídeo final criado! ID: {video_id}")
        
        Kestra.outputs({
            'videoId': video_id,
            'videoTitle': post_title,
            'model_used': model_used,
            'video_data': json.dumps(video_result),
            'agent_result': str(agent_result)[:500]
        })
    else:
        raise Exception(f"Erro ao criar vídeo: {video_response.status_code} - {video_response.text}")


if __name__ == '__main__':
    main()
