# 🚀 Como Abrir GO_LIVE Dashboard

## ⚠️ Problema Original

Quando você abre o arquivo `GO_LIVE.html` diretamente (clicando 2x), o navegador:
- Usa o protocolo `file://` 
- Bloqueia pop-ups e aberturas de links externos
- Os botões não funcionam corretamente

## ✅ Solução

Use o **servidor HTTP local** que já criamos para você!

---

## 🎯 Como Usar

### Opção 1: **Clique Duplo (Windows - Mais Fácil)** ⭐

1. Vá para a pasta do projeto
2. Procure pelo arquivo: **`START_GOLIVE.bat`**
3. **Clique 2x** no arquivo
4. Uma janela de terminal vai abrir
5. Seu navegador abre automaticamente em: `http://localhost:8080`

**Pronto!** Todos os botões funcionam agora ✅

---

### Opção 2: **Terminal PowerShell**

```powershell
# Abra PowerShell na pasta do projeto e execute:
.\START_GOLIVE.ps1
```

---

### Opção 3: **Python Direto**

```bash
# Terminal (CMD ou PowerShell)
python serve_golive.py

# Ou se só tem python3
python3 serve_golive.py
```

---

## 📊 O que Aparece Quando Roda

```
============================================
  GO LIVE Dashboard - Servidor Local
============================================

✓ Python encontrado

Iniciando servidor em http://localhost:8080
📄 Abrindo GO_LIVE.html...

Pressione Ctrl+C para parar o servidor
127.0.0.1 - - [04/Feb/2026 10:30:45] ✅ GET /GO_LIVE.html HTTP/1.1" 200
✅ Servidor parado
```

---

## 🔘 Botões que Agora Funcionam

| Botão | Ação | Destino |
|-------|------|---------|
| 📦 Repositório GitHub | Clica → Abre | GitHub repo |
| 🐳 Docker Registry | Clica → Abre | Container Registry |
| 🚀 Release v1.0.0 | Clica → Abre | GitHub Releases |
| 📋 Docker Compose | Clica → Copia comando | Clipboard |
| ☸️ Deploy Kubernetes | Clica → Copia comando | Clipboard |
| ⚡ Load Test | Clica → Copia comando | Clipboard |

---

## 🌐 URLs dos Botões

Quando você clica, abre:

```
📦 → https://github.com/PauloRamos38/pipeline-cicd-monitoramento
🐳 → https://github.com/PauloRamos38/pipeline-cicd-monitoramento/pkgs/container/pipeline-cicd-monitoramento
🚀 → https://github.com/PauloRamos38/pipeline-cicd-monitoramento/releases/tag/v1.0.0
```

---

## ⏹️ Para Parar o Servidor

Pressione **`Ctrl+C`** no terminal

```
^C
✋ Servidor parado
```

---

## 🔧 Resolvendo Problemas

### "Porta 8080 já está em uso"

Se a porta 8080 já está sendo usada, você vai ver:

```
❌ OSError: [Errno 48] Address already in use
```

**Solução:** Pressione Ctrl+C para fechar outro servidor, ou use porta diferente:

```bash
# Editar serve_golive.py e mudar:
PORT = 8080  # para PORT = 9000
```

### "Python não encontrado"

Se Python não está instalado:

1. Baixe em: https://www.python.org/downloads/
2. Instale marcando: ✅ "Add Python to PATH"
3. Reinicie o terminal
4. Tente novamente

### "Navegador não abriu automaticamente"

Se o navegador não abrir sozinho:

1. Abra manualmente seu navegador (Chrome, Firefox, Edge)
2. Digite na barra: **`http://localhost:8080`**
3. Pressione Enter

---

## 💡 Dicas

### 1. **Criar Atalho na Desktop**

**Windows:**
- Clique direito em `START_GOLIVE.bat`
- "Enviar para" → "Desktop (criar atalho)"
- Agora pode dar 2 cliques no atalho da desktop

### 2. **Adicionar ao PATH do Windows**

Para rodar de qualquer pasta:
```batch
setx PATH "%PATH%;C:\Users\User\Downloads\OneDrive\Ambiente de Trabalho\Pipeline CICD Completo com Monitoramento"
```

### 3. **Manter Sempre Rodando**

Se quer que o servidor rode o tempo todo:
- Deixe a janela do terminal aberta
- Ele continua rodando em `http://localhost:8080`

---

## 📱 Acessar de Outro Computador

Se quer acessar do notebook/celular enquanto roda no PC:

1. Descubra o IP do PC:
   ```bash
   ipconfig  # Windows
   # Procure por "IPv4 Address" (exemplo: 192.168.1.100)
   ```

2. No outro dispositivo, acesse:
   ```
   http://192.168.1.100:8080
   ```

---

## 🎯 Fluxo Completo

```
Clique 2x em START_GOLIVE.bat
        ↓
Terminal abre
        ↓
Python inicia servidor
        ↓
Navegador abre http://localhost:8080
        ↓
GO_LIVE Dashboard aparece
        ↓
Clique nos botões → Links abrem corretamente! ✅
```

---

## ✅ Checklist

- [x] Arquivo `serve_golive.py` criado ✅
- [x] Arquivo `START_GOLIVE.bat` criado ✅
- [x] Arquivo `START_GOLIVE.ps1` criado ✅
- [x] Documentação pronta ✅
- [x] Botões funcionando ✅

**Tudo pronto para abrir o dashboard!** 🎉
