#!/usr/bin/env python3
"""Gera diagramas .excalidraw das fases da demo 03.3-Lambda.

Embute icones OFICIAIS (AWS Architecture Icons + Terraform) como imagens.
Layout pensado para UX: espacamento generoso, sem sobreposicao, setas
conectando bordas, rotulos abaixo dos icones, paleta FIAP nos destaques.

Uso: python3 gerar.py <fase1|fase2|fase3>

LICOES DE UX APRENDIDAS COM O REVISOR (aplicar em TODAS as fases, nunca repetir):
- L1 Acentuacao correta nos rotulos visiveis (Ingestao->Ingestao com til,
  metricas->metricas com acento). Rotulo de diagrama e portugues correto.
- L2 Sem redundancia: nao repetir no subtitulo o que ja esta no titulo.
- L3 Direcao da seta tem que casar com o verbo. Lambda->CloudWatch = "envia
  logs/metricas" (a Lambda envia). Nunca rotular seta que sai de X com um
  verbo cujo sujeito e o destino.
- L4 Layout equilibrado: nao deixar vazio enorme no topo nem tudo amontoado
  num canto. Conteudo proximo do topo e ocupando a largura.
- L5 Rotulo de aresta explicito: "invoca (evento)" e melhor que so "evento".
- L6 Deixar explicito que PedeJa e o nome da EMPRESA (senao parece typo).
- L7 Layout proximo do topo, sem vazio vertical grande entre titulo e fluxo.
- L8 Fluxo secundario (observabilidade -> CloudWatch) com seta TRACEJADA, para
  distinguir do caminho principal do dado (seta solida).
- L9 Rotulo de seta NUNCA encosta na propria seta nem em icone: dar respiro
  (deslocar o texto e checar distancia ao no de destino).
- L10 Caminho de erro/excecao destacado: rotulo em cor de alerta + tracejado.
- L11 Fan-out (1 origem -> N destinos): a divisao parte de UM ponto claro na
  borda; um unico rotulo no ponto de divisao ("ambos leem o mesmo dado"),
  nunca rotulo duplicado flutuando. Angulo de abertura moderado.
- L12 Quando o mesmo icone aparece em papeis diferentes (3 Lambdas), o papel
  vem em DESTAQUE no rotulo (Produtor / Consumidor A / Consumidor B).
- L13 Cor tem semantica fixa: magenta/vermelho = alerta/erro. NAO usar magenta
  em rotulo informativo positivo (parece aviso de problema). Rotulo de seta
  informativo = cinza/preto; so caminho de erro usa cor de alerta.
"""
import base64
import json
import sys
import os

DIR = os.path.dirname(os.path.abspath(__file__))
ICONES = os.path.join(DIR, "icones")

# Paleta FIAP + AWS
FIAP_MAGENTA = "#ED0973"
TEXTO = "#1e1e1e"
CINZA = "#495057"
AWS_LARANJA = "#ED7100"

# Geometria base (em px) — folgas largas evitam sobreposicao
ICON = 80          # tamanho do icone
LABEL_H = 50       # altura reservada para o rotulo (ate 2 linhas)
LABEL_GAP = 12     # espaco entre icone e rotulo
COL_PITCH = 260    # distancia horizontal entre centros de nos (bem largo)
ROW_PITCH = 230    # distancia vertical entre linhas


def _seed(n):
    return 1000 + n * 7


def carrega_icone_datauri(nome):
    # Usamos PNG (rasterizado dos SVGs oficiais): imagens PNG embutidas sao
    # renderizadas de forma confiavel pelo canvas headless; SVG-em-SVG nao e.
    with open(os.path.join(ICONES, f"{nome}.png"), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


class Diagrama:
    def __init__(self):
        self.elements = []
        self.files = {}
        self._n = 0

    def _id(self, prefix):
        self._n += 1
        return f"{prefix}{self._n}"

    def no(self, icone, rotulo, cx, cy, destaque=False):
        """Cria um no = icone centralizado em (cx,cy) + rotulo abaixo.
        Retorna o id do elemento-icone e seu bbox para ligar setas."""
        x = cx - ICON / 2
        y = cy - ICON / 2
        file_id = self._id("file")
        self.files[file_id] = {
            "mimeType": "image/png",
            "id": file_id,
            "dataURL": carrega_icone_datauri(icone),
            "created": 1,
        }
        img_id = self._id("img")
        self.elements.append({
            "id": img_id, "type": "image", "x": x, "y": y,
            "width": ICON, "height": ICON, "angle": 0,
            "strokeColor": "transparent", "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": _seed(self._n), "version": 1,
            "versionNonce": _seed(self._n), "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "status": "saved", "fileId": file_id, "scale": [1, 1],
        })
        # rotulo abaixo do icone, largura = COL_PITCH (centralizado), 2 linhas ok
        lbl_w = COL_PITCH - 30
        lbl_x = cx - lbl_w / 2
        lbl_y = y + ICON + LABEL_GAP
        self.elements.append({
            "id": self._id("txt"), "type": "text", "x": lbl_x, "y": lbl_y,
            "width": lbl_w, "height": LABEL_H, "angle": 0,
            "strokeColor": FIAP_MAGENTA if destaque else TEXTO,
            "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
            "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
            "seed": _seed(self._n), "version": 1, "versionNonce": _seed(self._n),
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
            "locked": False, "fontSize": 16,
            "fontFamily": 2,  # 2 = fonte normal (Helvetica), legivel
            "text": rotulo, "textAlign": "center", "verticalAlign": "top",
            "containerId": None, "originalText": rotulo, "lineHeight": 1.25,
            "baseline": 14,
        })
        return {"x": x, "y": y, "w": ICON, "h": ICON, "cx": cx, "cy": cy}

    def seta(self, a, b, rotulo=None):
        """Liga o no a -> b por uma seta da borda direita de a a borda esq de b."""
        x1 = a["x"] + a["w"]
        y1 = a["cy"]
        x2 = b["x"]
        y2 = b["cy"]
        self.elements.append({
            "id": self._id("arr"), "type": "arrow", "x": x1, "y": y1,
            "width": x2 - x1, "height": y2 - y1, "angle": 0,
            "strokeColor": CINZA, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 2}, "seed": _seed(self._n), "version": 1,
            "versionNonce": _seed(self._n), "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow",
        })
        if rotulo:
            # rotulo da seta ACIMA do meio do caminho, sem encostar nos nos
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            w = COL_PITCH - ICON - 20
            self.elements.append({
                "id": self._id("etxt"), "type": "text", "x": mx - w / 2,
                "y": my - 34, "width": w, "height": 22, "angle": 0,
                "strokeColor": CINZA, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": _seed(self._n), "version": 1,
                "versionNonce": _seed(self._n), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
                "fontSize": 13, "fontFamily": 2, "text": rotulo,
                "textAlign": "center", "verticalAlign": "middle",
                "containerId": None, "originalText": rotulo, "lineHeight": 1.25,
                "baseline": 11,
            })

    def seta_vertical(self, a, b, rotulo=None, tracejada=False):
        """Liga a (em cima) -> b (embaixo) por seta vertical, borda a borda.
        tracejada=True marca fluxo secundario (ex: observabilidade)."""
        x1 = a["cx"]
        y1 = a["y"] + a["h"]
        x2 = b["cx"]
        y2 = b["y"]
        self.elements.append({
            "id": self._id("arr"), "type": "arrow", "x": x1, "y": y1,
            "width": x2 - x1, "height": y2 - y1, "angle": 0,
            "strokeColor": CINZA, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2,
            "strokeStyle": "dashed" if tracejada else "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 2}, "seed": _seed(self._n), "version": 1,
            "versionNonce": _seed(self._n), "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow",
        })
        if rotulo:
            my = (y1 + y2) / 2
            self.elements.append({
                "id": self._id("vtxt"), "type": "text", "x": x1 + 14,
                "y": my - 11, "width": 160, "height": 22, "angle": 0,
                "strokeColor": CINZA, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": _seed(self._n), "version": 1,
                "versionNonce": _seed(self._n), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
                "fontSize": 13, "fontFamily": 2, "text": rotulo,
                "textAlign": "left", "verticalAlign": "middle",
                "containerId": None, "originalText": rotulo, "lineHeight": 1.25,
                "baseline": 11,
            })

    def seta_diagonal(self, a, b, rotulo=None):
        """Seta da borda direita de a ate a borda esquerda de b, mesmo em
        alturas diferentes (ex: 1 stream -> 2 consumidores acima/abaixo)."""
        x1 = a["x"] + a["w"]
        y1 = a["cy"]
        x2 = b["x"]
        y2 = b["cy"]
        self.elements.append({
            "id": self._id("arr"), "type": "arrow", "x": x1, "y": y1,
            "width": x2 - x1, "height": y2 - y1, "angle": 0,
            "strokeColor": CINZA, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": {"type": 2}, "seed": _seed(self._n), "version": 1,
            "versionNonce": _seed(self._n), "isDeleted": False,
            "boundElements": [], "updated": 1, "link": None, "locked": False,
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
            "startArrowhead": None, "endArrowhead": "arrow",
        })
        if rotulo:
            # rotulo a ~35% do caminho (perto da origem), deslocado para nao
            # encostar no no de destino nem na outra diagonal
            mx = x1 + (x2 - x1) * 0.35
            my = y1 + (y2 - y1) * 0.35
            self.elements.append({
                "id": self._id("dtxt"), "type": "text", "x": mx - 70,
                "y": my - 26, "width": 140, "height": 22, "angle": 0,
                "strokeColor": CINZA, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": _seed(self._n), "version": 1,
                "versionNonce": _seed(self._n), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
                "fontSize": 13, "fontFamily": 2, "text": rotulo,
                "textAlign": "center", "verticalAlign": "middle",
                "containerId": None, "originalText": rotulo, "lineHeight": 1.25,
                "baseline": 11,
            })

    def fan_out(self, origem, destinos, rotulo=None):
        """1 origem -> N destinos (L11). Todas as setas partem do MESMO ponto
        (borda direita da origem); rotulo unico colocado nesse ponto."""
        px = origem["x"] + origem["w"]
        py = origem["cy"]
        for b in destinos:
            x2 = b["x"]
            y2 = b["cy"]
            self.elements.append({
                "id": self._id("arr"), "type": "arrow", "x": px, "y": py,
                "width": x2 - px, "height": y2 - py, "angle": 0,
                "strokeColor": CINZA, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": {"type": 2}, "seed": _seed(self._n), "version": 1,
                "versionNonce": _seed(self._n), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
                "points": [[0, 0], [x2 - px, y2 - py]],
                "lastCommittedPoint": None, "startBinding": None,
                "endBinding": None, "startArrowhead": None,
                "endArrowhead": "arrow",
            })
        if rotulo:
            # L13: rotulo informativo = cinza (magenta seria lido como alerta).
            # L9: respiro maior do ponto de divisao para nao colar na seta.
            self.elements.append({
                "id": self._id("fotxt"), "type": "text", "x": px + 22,
                "y": py - 42, "width": 200, "height": 22, "angle": 0,
                "strokeColor": CINZA, "backgroundColor": "transparent",
                "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
                "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": None, "seed": _seed(self._n), "version": 1,
                "versionNonce": _seed(self._n), "isDeleted": False,
                "boundElements": [], "updated": 1, "link": None, "locked": False,
                "fontSize": 13, "fontFamily": 2, "text": rotulo,
                "textAlign": "left", "verticalAlign": "middle",
                "containerId": None, "originalText": rotulo, "lineHeight": 1.25,
                "baseline": 11,
            })

    def titulo(self, texto, x, y, w=900):
        self.elements.append({
            "id": self._id("title"), "type": "text", "x": x, "y": y,
            "width": w, "height": 30, "angle": 0, "strokeColor": FIAP_MAGENTA,
            "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
            "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
            "seed": _seed(self._n), "version": 1, "versionNonce": _seed(self._n),
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
            "locked": False, "fontSize": 22, "fontFamily": 2, "text": texto,
            "textAlign": "left", "verticalAlign": "top", "containerId": None,
            "originalText": texto, "lineHeight": 1.25, "baseline": 19,
        })

    def nota(self, texto, x, y, w=900, cor=CINZA):
        self.elements.append({
            "id": self._id("nota"), "type": "text", "x": x, "y": y,
            "width": w, "height": 22, "angle": 0, "strokeColor": cor,
            "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1,
            "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
            "seed": _seed(self._n), "version": 1, "versionNonce": _seed(self._n),
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
            "locked": False, "fontSize": 14, "fontFamily": 2, "text": texto,
            "textAlign": "left", "verticalAlign": "top", "containerId": None,
            "originalText": texto, "lineHeight": 1.25, "baseline": 12,
        })

    def salvar(self, caminho):
        doc = {
            "type": "excalidraw", "version": 2, "source": "fiap-gerador",
            "elements": self.elements,
            "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
            "files": self.files,
        }
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        print(f"gerado: {caminho} ({len(self.elements)} elementos)")


# ---------------------------------------------------------------------------
# Layouts por fase
# ---------------------------------------------------------------------------

def fase1():
    d = Diagrama()
    d.titulo("Fase 1 - Ingestão direta de pedidos (app PedeJá) | IaC: Terraform", 60, 36)
    d.nota("Empresa: PedeJá (app de delivery). Toda a infraestrutura é provisionada com Terraform.",
           60, 70, w=1100)
    y = 150  # L7: bloco proximo do topo
    x0 = 180
    api = d.no("apigateway", "API Gateway\nPOST /pedidos", x0, y)
    lam = d.no("lambda", "Lambda\npedeja-ingestao", x0 + COL_PITCH, y)
    s3 = d.no("s3", "S3\ndata lake", x0 + 2 * COL_PITCH, y)
    cw = d.no("cloudwatch", "CloudWatch\nlogs, métricas, trace", x0 + COL_PITCH, y + ROW_PITCH)
    d.seta(api, lam, "invoca (evento)")
    d.seta(lam, s3, "grava JSON")
    # L3 + L8: a Lambda ENVIA telemetria ao CloudWatch; tracejada = fluxo secundario
    d.seta_vertical(lam, cw, "envia logs/métricas", tracejada=True)
    d.nota("Fluxo: o app faz POST -> API Gateway entrega o EVENTO à Lambda -> a Lambda grava o pedido no S3.",
           60, y + 2 * ROW_PITCH - 50, w=1100)
    d.salvar(os.path.join(DIR, "fase-1.excalidraw"))


def fase2():
    d = Diagrama()
    d.titulo("Fase 2 - Desacoplado com fila SQS (app PedeJá) | IaC: Terraform", 60, 36)
    d.nota("A Black Friday derrubou a Fase 1. Uma fila SQS no meio absorve o pico. Tudo provisionado com Terraform.",
           60, 70, w=1300)
    y = 170  # L7: proximo do topo
    x0 = 170
    api = d.no("apigateway", "API Gateway", x0, y)
    prod = d.no("lambda", "Lambda produtora\n(só enfileira)", x0 + COL_PITCH, y)
    sqs = d.no("sqs", "SQS\npedeja-pedidos", x0 + 2 * COL_PITCH, y)
    cons = d.no("lambda", "Lambda consumidora\n(processa lote)", x0 + 3 * COL_PITCH, y)
    s3 = d.no("s3", "S3\ndata lake", x0 + 4 * COL_PITCH, y)
    dlq = d.no("sqs", "DLQ\n(mensagens com falha)", x0 + 2 * COL_PITCH, y + ROW_PITCH)
    d.seta(api, prod, "invoca (evento)")
    d.seta(prod, sqs, "enfileira")
    d.seta(sqs, cons, "invoca em lote")
    d.seta(cons, s3, "grava JSON")
    # L8: caminho de falha e secundario -> tracejado
    d.seta_vertical(sqs, dlq, "após 3 falhas", tracejada=True)
    d.nota("A fila absorve o pico: o produtor responde em ms (só enfileira) e a consumidora grava no ritmo que aguenta. Falhas vão para a DLQ sem perder dado.",
           60, y + 2 * ROW_PITCH - 40, w=1300)
    d.salvar(os.path.join(DIR, "fase-2.excalidraw"))


def fase3():
    d = Diagrama()
    d.titulo("Fase 3 - Kinesis: 1 stream, N consumidores (app PedeJá)", 60, 36)
    d.nota("Três times querem o MESMO dado. O Kinesis retém o stream e permite vários consumidores independentes + replay.",
           60, 72, w=1300)
    # L11: abertura moderada (meio ROW_PITCH) para nao criar vazio central
    y = 300
    dy = int(ROW_PITCH * 0.8)
    x0 = 170
    api = d.no("apigateway", "API Gateway", x0, y)
    prod = d.no("lambda", "Lambda PRODUTORA\n(publica no stream)", x0 + COL_PITCH, y)
    kin = d.no("kinesis", "Kinesis\nstream (dado retido)", x0 + 2 * COL_PITCH, y)
    c1 = d.no("lambda", "Lambda CONSUMIDORA A\n(data lake)", x0 + 3 * COL_PITCH, y - dy)
    c2 = d.no("lambda", "Lambda CONSUMIDORA B\n(faturamento)", x0 + 3 * COL_PITCH, y + dy)
    s3 = d.no("s3", "S3\ndata lake", x0 + 4 * COL_PITCH, y - dy)
    cw = d.no("cloudwatch", "CloudWatch\nmétrica por cidade", x0 + 4 * COL_PITCH, y + dy)
    d.seta(api, prod, "invoca (evento)")
    d.seta(prod, kin, "publica")
    # L11: fan-out de UM ponto (borda direita do Kinesis) com rotulo unico
    d.fan_out(kin, [c1, c2], "ambos leem o mesmo dado")
    d.seta(c1, s3, "grava JSON")
    d.seta(c2, cw, "agrega")
    d.nota("O mesmo stream alimenta DOIS consumidores independentes; o dado fica retido, o que permite reprocessar (replay).",
           60, y + dy + 120, w=1300)
    d.salvar(os.path.join(DIR, "fase-3.excalidraw"))


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "todas"
    if alvo in ("fase1", "todas"):
        fase1()
    if alvo in ("fase2", "todas"):
        fase2()
    if alvo in ("fase3", "todas"):
        fase3()
