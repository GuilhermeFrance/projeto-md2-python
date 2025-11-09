# 🚀 Guia de Setup - PathFinder Adventure

## ⚠️ Problema: Python não está no PATH

Se você está recebendo erro "python não é reconhecido", siga estes passos:

### Opção 1: Instalar Python via Microsoft Store (Recomendado)

1. Abra a **Microsoft Store**
2. Procure por "Python"
3. Clique em "Python 3.11" (ou a versão mais recente)
4. Clique em "Obter" para instalar
5. Feche e reabra o PowerShell

### Opção 2: Instalar Python via python.org

1. Visite: https://www.python.org/downloads/
2. Clique em "Download Python 3.11" (ou versão recente)
3. **IMPORTANTE**: Na instalação, marque a opção "Add Python to PATH"
4. Conclua a instalação
5. Reabra o PowerShell

### Opção 3: Usando py.exe (Se Python já estiver instalado)

Se Python estiver instalado mas não no PATH:

```powershell
# Vá para o diretório do projeto
cd "c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure"

# Instale as dependências
py -m pip install -r requirements.txt

# Execute o jogo
py main.py
```

## ✅ Verificar se Python está instalado corretamente

```powershell
# Teste um destes comandos
python --version
py --version
python3 --version
```

Se algum deles retornar uma versão (ex: "Python 3.11.2"), está funcionando!

## 🎮 Executando o Jogo

Após instalar Python e as dependências:

```powershell
cd "c:\Users\ribei\Documents\Dev\Projects\md2\pathfinder_adventure"
python main.py
# ou
py main.py
```

## 📦 Dependências Necessárias

- **pygame** - Para renderização gráfica
- **networkx** - Para manipulação de grafos
- **numpy** - Para cálculos matemáticos

Estas serão instaladas automaticamente com:
```powershell
pip install -r requirements.txt
# ou
py -m pip install -r requirements.txt
```

## 🆘 Ajuda Adicional

Se ainda tiver problemas, tente:

1. Reiniciar o computador após instalar Python
2. Usar PowerShell como administrador
3. Instalar uma versão específica: `pip install pygame==2.5.2 networkx==3.2 numpy==1.24.3`

---

**Precisa de mais ajuda? Abra uma issue ou consulte a documentação do Python!**
