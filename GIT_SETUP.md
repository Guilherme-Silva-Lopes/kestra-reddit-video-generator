# Comandos Git para fazer upload do projeto

## 1. Crie um novo repositório no GitHub
- Acesse: https://github.com/new
- Nome sugerido: `kestra-reddit-video-generator`
- Torne-o público ou privado conforme preferir
- **NÃO** adicione README, .gitignore ou licença (já criamos)

## 2. Inicialize o repositório local e faça push

Abra o terminal na pasta do projeto e execute:

```powershell
# Entre na pasta do projeto
cd "d:/PC essentials/TESTES DE IA/Kestra Langchain Shorts MCP"

# Inicializa o repositório Git
git init

# Adiciona todos os arquivos
git add .

# Faz o commit inicial
git commit -m "Initial commit: Reddit video generator workflow for Kestra"

# Adiciona o repositório remoto (SUBSTITUA SEU_USUARIO pelo seu usuário GitHub)
git remote add origin https://github.com/SEU_USUARIO/kestra-reddit-video-generator.git

# Renomeia branch para main
git branch -M main

# Faz push para o GitHub
git push -u origin main
```

## 3. Atualize o workflow no Kestra

Após fazer o push para o GitHub:

1. Abra o arquivo `reddit-video-generator-github.yml`
2. Na linha 7, **atualize** a variável `github_repo` com a URL do seu repositório:
   ```yaml
   github_repo: "https://github.com/SEU_USUARIO/kestra-reddit-video-generator.git"
   ```
3. Salve o arquivo
4. Faça upload deste workflow no Kestra

## 4. Configure o KV Store no Kestra

Certifique-se de que as seguintes chaves estão configuradas no KV Store:

```
GOOGLE_API_KEY: sua-chave-google-aqui
OPENAI_API_KEY: sua-chave-openai-aqui
SHORTS_GENERATOR_MCP: https://projeto-1-mcp-shorts-generator-tiny.2eisou.easypanel.host
```

## 5. Teste o workflow

Execute o workflow `reddit-video-generator` no Kestra e verifique se:
- ✅ Clona o repositório corretamente
- ✅ Executa os scripts do GitHub
- ✅ Usa a variável `SHORTS_GENERATOR_MCP` do KV Store

## Estrutura do repositório criado:

```
kestra-reddit-video-generator/
├── scripts/
│   ├── parse_reddit_feed.py
│   ├── generate_video_with_ai.py
│   └── wait_and_download_video.py
├── reddit-video-generator.yml (workflow original)
├── reddit-video-generator-github.yml (workflow que usa GitHub)
├── test-video-status.yml
├── requirements.txt
├── README.md
└── .gitignore
```

## Vantagens desta abordagem:

✅ **Código centralizado**: Scripts em um repositório Git
✅ **Versionamento**: Histórico completo de mudanças
✅ **Colaboração**: Fácil compartilhar e receber contribuições
✅ **Manutenção**: Atualizar código sem editar YAML do Kestra
✅ **Segurança**: Credenciais no KV Store, não no código
✅ **CI/CD**: Possibilidade de testes automatizados

## Próximas melhorias possíveis:

- [ ] Adicionar testes unitários para os scripts Python
- [ ] Criar GitHub Actions para validação automática
- [ ] Implementar múltiplos workflows para diferentes subreddits
- [ ] Adicionar notificações (Discord, Slack, Email)
- [ ] Implementar upload automático para YouTube
