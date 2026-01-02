# Reddit to Video Generator - Kestra Workflow

Workflow automatizado que busca posts do Reddit, processa o conteúdo com IA (Gemini/GPT) e gera vídeos curtos usando MCP (Media Content Platform).

## 📋 Descrição

Este projeto migra um workflow do n8n para Kestra, automatizando:
1. **Busca de posts** do Reddit via RSS feed
2. **Processamento de conteúdo** com parsing XML
3. **Geração de vídeo** usando agentes AI (Gemini 3 Flash Preview com fallback para GPT-4o-mini)
4. **Integração com MCP** para criação de vídeos curtos
5. **Monitoramento e download** automático do vídeo quando pronto

## 🏗️ Estrutura do Projeto

```
.
├── scripts/
│   ├── parse_reddit_feed.py           # Parse do feed RSS do Reddit
│   ├── generate_video_with_ai.py       # Geração de vídeo com AI + MCP
│   └── wait_and_download_video.py      # Verificação de status e download
├── reddit-video-generator.yml          # Workflow principal do Kestra
├── test-video-status.yml               # Workflow de teste
├── requirements.txt                    # Dependências Python
└── README.md                           # Este arquivo

```

## 🔧 Configuração

### Pré-requisitos

- Kestra instalado e rodando
- Conta Google Cloud (para Gemini API)
- Conta OpenAI (para GPT API)
- Acesso ao MCP Server

### Variáveis do KV Store (Kestra)

Configure as seguintes chaves no KV Store do Kestra:

```yaml
GOOGLE_API_KEY: "sua-chave-google-aqui"
OPENAI_API_KEY: "sua-chave-openai-aqui"
SHORTS_GENERATOR_MCP: "https://projeto-1-mcp-shorts-generator-tiny.2eisou.easypanel.host"
```

### Instalação

1. Clone este repositório
2. Configure as variáveis do KV Store no Kestra
3. Faça upload do workflow `reddit-video-generator.yml` no Kestra
4. Execute manualmente ou configure um trigger Schedule

## 🚀 Como Funciona

### Workflow Principal

1. **fetch_reddit_feed**: Busca o feed RSS do Reddit r/stories
2. **parse_and_process_feed**: Converte XML para JSON e extrai posts
3. **generate_video_with_ai**: 
   - Usa Gemini 3 Flash Preview para processar o conteúdo
   - Se falhar, tenta GPT-4o-mini como fallback
   - Chama API MCP para criar o vídeo
4. **wait_and_download_video**: 
   - Verifica status a cada 2 minutos (até 30 tentativas = 1 hora)
   - Baixa o vídeo quando estiver pronto
   - Salva no storage do Kestra

### Workflow de Teste

O arquivo `test-video-status.yml` permite testar rapidamente a verificação de status e download de vídeos já prontos, sem precisar esperar 30+ minutos.

## 📦 Scripts Python

### parse_reddit_feed.py
Processa o feed RSS do Reddit:
- Parse XML usando xmltodict
- Extração de título, autor, link, data e conteúdo
- Output formatado para o próximo step

### generate_video_with_ai.py
Gera vídeo usando AI:
- Configura agentes Langchain com Gemini e GPT
- Define tool MCP para criação de vídeo
- Implementa fallback automático Gemini → GPT
- Retorna videoId para monitoramento

### wait_and_download_video.py
Monitora e baixa vídeo:
- Polling a cada 2 minutos
- Máximo de 30 tentativas (1 hora)
- Status case-insensitive ("ready", "Ready", "READY")
- Download automático quando pronto

## 🔄 Variáveis do Workflow

```yaml
variables:
  reddit_feed_url: "https://www.reddit.com/r/stories/top/.rss?t=week"
  max_wait_attempts: 30
  wait_interval: PT2M  # 2 minutos
```

## 📝 Outputs

Após execução bem-sucedida:
- `videoId`: ID do vídeo criado
- `videoTitle`: Título do post/vídeo
- `model_used`: Modelo AI usado (gemini-3-flash-preview ou gpt-4o-mini)
- `video_file`: Arquivo video.mp4 no storage do Kestra
- `download_success`: Status do download

## 🐛 Troubleshooting

### Vídeo falha no processamento
- Verifique os logs do MCP server
- Valide o conteúdo do post (pode ser muito longo/curto)

### Timeout na verificação de status
- Aumente `max_wait_attempts` nas variáveis
- Verifique conectividade com o MCP server

### Erro de API Key
- Verifique se as keys estão configuradas no KV Store
- Confirme que as chaves são válidas e têm quota

## 📄 Licença

Este projeto é de código aberto para uso educacional.

## 🤝 Contribuindo

Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro para discutir.
