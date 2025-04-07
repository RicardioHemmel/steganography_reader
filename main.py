import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import zlib

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def extrair_mensagem(imagem_caminho):
    try:
        img = Image.open(imagem_caminho)
        img = img.convert("RGB")
        pixels = img.load()

        largura, altura = img.size
        bits = ''
        for y in range(altura):
            for x in range(largura):
                _, _, b = pixels[x, y]
                bits += str(b & 1)

        # Convertendo os bits em bytes
        bytes_extraidos = bytearray()
        for i in range(0, len(bits), 8):
            byte_bin = bits[i:i+8]
            if byte_bin == '00000000':  # delimitador de fim
                break
            bytes_extraidos.append(int(byte_bin, 2))

        # Tenta descompactar com zlib
        mensagem = zlib.decompress(bytes_extraidos).decode('utf-8')
        return mensagem

    except Exception as e:
        raise RuntimeError(f"Erro ao extrair mensagem: {e}")

class LeitorMensagemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Leitor de Mensagens Ocultas")
        self.geometry("600x450")
        self.mensagem_extraida = ""

        ctk.CTkLabel(self, text="Leitor de Mensagens Ocultas em PNG", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        ctk.CTkButton(self, text="Selecionar Imagem PNG", command=self.selecionar_imagem).pack(pady=10)

        self.text_resultado = ctk.CTkTextbox(self, height=220, width=550, state="disabled", wrap="word")
        self.text_resultado.pack(padx=20, pady=10, fill="both", expand=True)

        self.botao_salvar = ctk.CTkButton(self, text="Salvar como .TXT", command=self.salvar_txt, state="disabled")
        self.botao_salvar.pack(pady=10)

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens PNG", "*.png")])
        if not caminho:
            return

        try:
            mensagem = extrair_mensagem(caminho)

            if not mensagem:
                messagebox.showwarning("Aviso", "Nenhuma mensagem oculta encontrada na imagem.")
                return

            self.mensagem_extraida = mensagem
            self.text_resultado.configure(state="normal")
            self.text_resultado.delete("1.0", "end")
            self.text_resultado.insert("1.0", mensagem)
            self.text_resultado.configure(state="disabled")

            self.botao_salvar.configure(state="normal")
            messagebox.showinfo("Sucesso", "Mensagem extraída com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def salvar_txt(self):
        if not self.mensagem_extraida:
            messagebox.showwarning("Aviso", "Nenhuma mensagem extraída para salvar.")
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
        if not caminho:
            return

        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(self.mensagem_extraida)
            messagebox.showinfo("Salvo", f"Mensagem salva em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo:\n{e}")

# Execução da interface
if __name__ == "__main__":
    app = LeitorMensagemApp()
    app.mainloop()