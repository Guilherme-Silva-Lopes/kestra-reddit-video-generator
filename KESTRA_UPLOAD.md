# Como fazer upload dos scripts para o Kestra

## Opção 1: Via Interface Web do Kestra

1. Acesse o Kestra no navegador
2. Vá em **Namespaces** → **company.team**
3. Clique em **Files** (ou Editor)
4. Crie a pasta `scripts/` se não existir
5. Faça upload dos seguintes arquivos:
   - `scripts/parse_reddit_feed.py`
   - `scripts/generate_video_with_ai.py`
   - `scripts/wait_and_download_video.py`

## Opção 2: Via CLI do Kestra

Se você tiver o Kestra CLI instalado:

```bash
# Upload dos scripts
kestra namespace files upload company.team scripts/parse_reddit_feed.py scripts/parse_reddit_feed.py
kestra namespace files upload company.team scripts/generate_video_with_ai.py scripts/generate_video_with_ai.py
kestra namespace files upload company.team scripts/wait_and_download_video.py scripts/wait_and_download_video.py
```

## Estrutura Esperada no Namespace

Após o upload, a estrutura deve ficar assim no namespace `company.team`:

```
company.team/
└── scripts/
    ├── parse_reddit_feed.py
    ├── generate_video_with_ai.py
    └── wait_and_download_video.py
```

## Verificação

Após fazer upload, execute o workflow novamente. O Kestra vai:
1. Buscar os scripts do namespace files usando `{{ read('scripts/parse_reddit_feed.py') }}`
2. Executar cada script com as variáveis de ambiente configuradas

## Vantagens desta abordagem:

✅ **Mais simples**: Não precisa de Git Clone
✅ **Mais rápido**: Scripts já estão no Kestra
✅ **Mais confiável**: Sem dependência de plugins externos
✅ **Versionamento**: Kestra mantém histórico de mudanças
✅ **Ainda usa GitHub**: Você mantém o código no Git para backup e colaboração

## Workflow de desenvolvimento recomendado:

1. **Desenvolva** localmente e faça **commit/push** no GitHub
2. **Upload** manual dos scripts atualizados no Kestra Namespace Files
3. **Execute** o workflow no Kestra

Ou automatize isso com um workflow Kestra separado que:
- Clona o repositório
- Faz upload automático dos scripts para namespace files
