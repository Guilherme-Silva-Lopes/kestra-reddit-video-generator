"""
Wait for video to be ready and download it
"""
import requests
import time
import json
import os
from kestra import Kestra


def main():
    mcp_server_url = os.getenv('MCP_SERVER_URL')
    video_id = os.getenv('VIDEO_ID')
    max_attempts = int(os.getenv('MAX_WAIT_ATTEMPTS', '30'))
    wait_seconds = 120  # 2 minutos
    
    if not all([mcp_server_url, video_id]):
        raise Exception("Missing required environment variables: MCP_SERVER_URL or VIDEO_ID")
    
    print(f"Verificando status do vídeo {video_id}...")
    
    for attempt in range(max_attempts):
        try:
            # Verifica o status
            status_url = f"{mcp_server_url}/api/short-video/{video_id}/status"
            response = requests.get(status_url)
            
            print(f"📡 Tentativa {attempt + 1}/{max_attempts}")
            print(f"   URL: {status_url}")
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                status_data = response.json()
                print(f"   Resposta completa: {json.dumps(status_data, indent=2)}")
                
                video_status = status_data.get('status', 'unknown')
                
                # Normaliza status para lowercase para comparação case-insensitive
                video_status_lower = str(video_status).lower()
                
                print(f"   Status do vídeo: {video_status}")
                
                if video_status_lower == 'ready':
                    print("✓ Vídeo pronto! Baixando...")
                    
                    # Baixa o vídeo
                    video_url = f"{mcp_server_url}/api/short-video/{video_id}"
                    video_response = requests.get(video_url)
                    
                    if video_response.status_code == 200:
                        # Salva o vídeo
                        with open('video.mp4', 'wb') as f:
                            f.write(video_response.content)
                        
                        print(f"✓ Vídeo baixado com sucesso! Tamanho: {len(video_response.content)} bytes")
                        
                        Kestra.outputs({
                            'status': 'ready',
                            'video_file': 'video.mp4',
                            'download_success': 'true'
                        })
                        break
                    else:
                        raise Exception(f"Erro ao baixar vídeo: {video_response.status_code}")
                
                elif video_status_lower == 'failed' or video_status_lower == 'error':
                    error_msg = status_data.get('error', status_data.get('message', 'Unknown error'))
                    raise Exception(f"Vídeo falhou no processamento: {error_msg}")
                
                else:
                    # Aguarda antes da próxima verificação
                    print(f"   Status ainda não pronto. Aguardando {wait_seconds} segundos...")
                    if attempt < max_attempts - 1:
                        time.sleep(wait_seconds)
            else:
                print(f"✗ Erro ao verificar status: {response.status_code}")
                print(f"   Resposta: {response.text[:200]}")
                if attempt < max_attempts - 1:
                    time.sleep(wait_seconds)
        
        except Exception as e:
            print(f"✗ Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt < max_attempts - 1:
                time.sleep(wait_seconds)
            else:
                raise
    
    else:
        raise Exception(f"Timeout: vídeo não ficou pronto após {max_attempts} tentativas")


if __name__ == '__main__':
    main()
