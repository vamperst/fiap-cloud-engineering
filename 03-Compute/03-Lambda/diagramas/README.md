# Diagramas das fases (Excalidraw)

Diagramas de arquitetura das 3 fases da demo, com **ícones oficiais** da AWS
(Architecture Icons) e do Terraform. Cada fase tem o fonte editável
`.excalidraw` e o `.png` usado no README.

| Fase | Fonte editável | Imagem |
|------|----------------|--------|
| 1 | `fase-1.excalidraw` | `fase-1.png` |
| 2 | `fase-2.excalidraw` | `fase-2.png` |
| 3 | `fase-3.excalidraw` | `fase-3.png` |

Para editar: abra o `.excalidraw` em [excalidraw.com](https://excalidraw.com)
(menu → Open) ou no plugin Excalidraw do VS Code.

## Regenerar os diagramas

Os `.excalidraw` são gerados por script (layout determinístico, sem
sobreposição). Para regerar após editar `gerar.py`:

```bash
cd /workspaces/fiap-cloud-engineering/03-Compute/03-Lambda/diagramas
python3 gerar.py todas
```

Os ícones em `icones/` são os SVGs oficiais (AWS + Terraform) e suas versões
PNG (rasterizadas com `rsvg-convert`), embutidas nos diagramas.
