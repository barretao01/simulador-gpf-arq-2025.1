import tkinter as tk
from tkinter import ttk, Canvas

# Regras estendidas de GPF, basicamente diz onde cada segmento pode dar gpdf no outro
REGRAS_GPF = [
    ("CS", "SS"),
    ("CS", "DS"),
    ("CS", "ES"),
    ("SS", "DS"),
    ("SS", "ES"),
    ("DS", "ES")
]

def calcular_endereco_fisico(segmento_hex, offset_hex):
    return int(segmento_hex, 16) * 16 + int(offset_hex, 16)
#converte a parada pra hex e calcula o endereço fisico da parada 
def calcular_intervalos():
    intervalos = {}
    for reg, var in reg_values.items():
        #dicionario do python para armazenar os valores 
        base = int(var.get(), 16) * 16
        topo = base + 0xFFFF
        intervalos[reg] = (base, topo)
    return intervalos
#calula os intevalos certinho na faixa de 64kb
def identificar_segmento(endereco, intervalos):
    for nome, (inicio, fim) in intervalos.items():
        if inicio <= endereco <= fim: # trivial ne mermao 
            return nome
    return "FORA"

def gpf_ocorre(origem, endereco_real, intervalos):
    base_origem = int(reg_values[origem].get(), 16) * 16
    fim_origem = base_origem + 0xFFFF
    for destino, (base_destino, fim_destino) in intervalos.items():
        if destino == origem:
            continue
        if (origem, destino) in REGRAS_GPF:
            if base_destino >= base_origem and base_destino <= fim_origem:
                if endereco_real >= base_destino and endereco_real <= fim_destino:
                    return True, destino
    return False, None
#seguinte, aqui ele vai verificar se o segmento invade o outro e se ta nas regras de gpf tlgd
def desenhar_mapa(canvas, intervalos, acesso, destino_invadido=None):
#apartir daqui o negocio foge um pouco do python de fato e fica muito lado do canvas
    canvas.delete("all")
    canvas.configure(bg="black")
    largura = 180
    altura_total = 500
    margem = 20

    segmentos = sorted(intervalos.items(), key=lambda x: x[1][0])
    min_addr = segmentos[0][1][0]
    max_addr = segmentos[-1][1][1]
    escala = (altura_total - 2 * margem) / (max_addr - min_addr)

    canvas.create_rectangle(60, margem, largura, altura_total - margem, outline="white", width=2)
    canvas.create_text((60 + largura) // 2, margem - 10, text="MEMORIA", fill="white", font=("Courier", 14, "bold"))

    cores = {
        "CS": "cyan",
        "SS": "red",
        "DS": "orange",
        "ES": "green"
    }

    for nome, (inicio, fim) in segmentos:
        y1 = margem + (inicio - min_addr) * escala
        y2 = margem + (fim - min_addr) * escala

        cor = cores.get(nome, "gray")
        meio_y = (y1 + y2) / 2

        fill_segment = "#222222" if nome == destino_invadido else ""
        canvas.create_rectangle(60, y1, largura, y2, outline=cor, width=2, fill=fill_segment)

        canvas.create_line(60, y1, largura, y1, fill=cor, width=1)  # linha interna
        canvas.create_line(60, y2, largura, y2, fill=cor, width=1)  # linha interna

        canvas.create_line(largura, y1, largura + 20, y1, fill=cor, width=2)
        canvas.create_text(largura + 25, y1 - 5, anchor="w", fill=cor, font=("Courier", 10, "bold"), text=f"{hex(inicio)[2:].upper()}")
        canvas.create_text(largura + 25, meio_y, anchor="w", fill=cor, font=("Courier", 12, "bold"), text=nome)
        canvas.create_line(largura, y2, largura + 20, y2, fill=cor, width=2)
        canvas.create_text(largura + 25, y2 + 5, anchor="w", fill=cor, font=("Courier", 10, "bold"), text=f"{hex(fim)[2:].upper()}")

    if acesso is not None:
        y = margem + (acesso - min_addr) * escala
        canvas.create_line(60, y, largura, y, fill="white", dash=(3, 2), width=2)
        canvas.create_text(55, y, anchor="e", text=f"\u2192 {hex(acesso)}", fill="white", font=("Courier", 10))

def simular():
    origem = origem_var.get()
    destino_logico = destino_var.get()
    offset_hex = offset_var.get()

    try:
        seg_base_hex = reg_values[destino_logico].get()
        endereco_fisico = calcular_endereco_fisico(seg_base_hex, offset_hex)
    except:
        resultado_var.set("\u274C Erro: valores inv\u00e1lidos")
        return

    intervalos = calcular_intervalos()
    segmento_real = identificar_segmento(endereco_fisico, intervalos)

    base_origem = int(reg_values[origem].get(), 16) * 16
    fim_origem = base_origem + 0xFFFF

    texto = f"Endere\u00e7o f\u00edsico: {hex(endereco_fisico)}\n"
    texto += f"Segmento onde o endere\u00e7o cai: {segmento_real}\n"
    texto += f"Faixa do {origem}: {hex(base_origem)} a {hex(fim_origem)}\n"

    for nome, (inicio, fim) in intervalos.items():
        texto += f"{nome}: {hex(inicio)} a {hex(fim)}\n"

    ocorreu_gpf, destino_invadido = gpf_ocorre(origem, endereco_fisico, intervalos)

    if segmento_real == "FORA":
        texto += "\n\u26A0\uFE0F GPF: Endere\u00e7o fora da mem\u00f3ria!"
    elif ocorreu_gpf:
        texto += f"\n\u274C GPF: {origem} invadiu {destino_invadido}\n"
        texto += f"Motivo: a base de {destino_invadido} est\u00e1 dentro da faixa de 64KB de {origem}, e o acesso ({hex(endereco_fisico)}) caiu dentro dessa regi\u00e3o."
    else:
        texto += f"\n\u2705 Acesso permitido: {origem} \u2192 {segmento_real}"

    resultado_var.set(texto)
    desenhar_mapa(mapa_canvas, intervalos, endereco_fisico, destino_invadido if ocorreu_gpf else None)

# Interface
root = tk.Tk()
root.title("Simulador de GPF - Vers\u00e3o Final")
root.geometry("800x680")
#formatacao do tamanho inicial da mini interface

main_frame = ttk.Frame(root, padding=12)
main_frame.pack(fill="both", expand=True)

left_frame = ttk.Frame(main_frame)
left_frame.pack(side="left", fill="y")

right_frame = ttk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

ttk.Label(left_frame, text="Segmento de origem (quem acessa):").grid(row=0, column=0, sticky="w")
origem_var = tk.StringVar(value="CS")
ttk.Combobox(left_frame, textvariable=origem_var, values=["CS", "SS", "DS", "ES"], width=10).grid(row=0, column=1)
# cria o botão alternavel apara selecionar os segmentos nessa ordem ai que eu jogueui 
reg_values = {}
row = 1
for reg in ["CS", "SS", "DS", "ES"]:
    ttk.Label(left_frame, text=f"Valor de {reg} (hex):").grid(row=row, column=0, sticky="w")
    reg_values[reg] = tk.StringVar(value="0000")
    ttk.Entry(left_frame, textvariable=reg_values[reg], width=10).grid(row=row, column=1)
    row += 1
# inicia o valor que cada base de endereço como 0000 para ser alterado 
ttk.Label(left_frame, text="Segmento de destino (usado no c\u00e1lculo):").grid(row=row, column=0, sticky="w")
destino_var = tk.StringVar(value="DS")
ttk.Combobox(left_frame, textvariable=destino_var, values=["CS", "SS", "DS", "ES"], width=10).grid(row=row, column=1)
row += 1
# mesmo esquema do primero soq agora eh o de saida
ttk.Label(left_frame, text="Offset (hex):").grid(row=row, column=0, sticky="w")
offset_var = tk.StringVar(value="0000")
ttk.Entry(left_frame, textvariable=offset_var, width=10).grid(row=row, column=1)
row += 1
# mesmo esquema das bases do segmento soq agora eh pra escolher o valor do offset
ttk.Button(left_frame, text="Simular", command=simular).grid(row=row, column=0, columnspan=2, pady=10)
row += 1
#botao de simular 
resultado_var = tk.StringVar()
ttk.Label(left_frame, textvariable=resultado_var, foreground="white", background="black", justify="left", wraplength=360).grid(row=row, column=0, columnspan=2)
#resultado da parada toda, se da gpf ou nao, enfim 
mapa_canvas = Canvas(right_frame, width=400, height=520, bg="black")
mapa_canvas.pack(padx=10, pady=10)

root.mainloop()
