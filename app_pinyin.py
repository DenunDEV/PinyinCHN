# app_pinyin.py
import tkinter as tk
from tkinter import ttk, messagebox
from pypinyin import pinyin, Style, lazy_pinyin
from deep_translator import GoogleTranslator

class ConversorPinyinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PinyinCHN")
        self.root.geometry("650x720")
        self.root.resizable(True, True)
        self.root.configure(bg="#f8f9fa")
        
        
        self.cor_destaque = "#e63946"                                   # Vermelho vibrante para ação principal
        self.cor_secundaria = "#457b9d"                              # Azul suave para texto
        self.cor_fundo_campo = "#ffffff"
        self.cor_borda = "#a8dadc"
        
        # Inicia tradutor
        self.tradutor = GoogleTranslator(source='zh-CN', target='pt')
        
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.root,
            text="PinyinCHN",
            font=("Segoe UI", 18, "bold"),
            fg=self.cor_secundaria,
            bg="#f8f9fa",
            pady=15
        )
        titulo.pack()
        
        # Subtítulo
        subtitulo = tk.Label(
            self.root,
            text="Digite em chinês para ver pinyin + tradução PT-BR",
            font=("Segoe UI", 10),
            fg="#6c757d",
            bg="#f8f9fa"
        )
        subtitulo.pack()
        
        # Frame de entrada
        frame_entrada = tk.Frame(self.root, bg="#f8f9fa", padx=20, pady=15)
        frame_entrada.pack(fill="x")
        
        # Rótulo
        tk.Label(
            frame_entrada,
            text="Texto em chinês:",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg="#1d3557"
        ).pack(anchor="w", pady=(0, 5))
        
        # Campo de entrada
        self.entrada = tk.Text(
            frame_entrada,
            height=3,
            font=("Microsoft YaHei", 14),  # Fonte que suporta caracteres chineses
            bg=self.cor_fundo_campo,
            fg="#333333",
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor=self.cor_borda
        )
        self.entrada.pack(fill="x", padx=5)
        self.entrada.focus_set()
        
        # Dica
        tk.Label(
            frame_entrada,
            text="Exemplo: 我爱你 ｜ 今天天气很好 ｜ 谢谢 ｜ 你叫什么名字",
            font=("Segoe UI", 9),
            fg="#6c757d",
            bg="#f8f9fa"
        ).pack(anchor="w", pady=(5, 0))
        
        # Botões
        frame_botoes = tk.Frame(self.root, bg="#f8f9fa", pady=15)
        frame_botoes.pack(fill="x")
        
        # Botão Converter
        self.botao_converter = tk.Button(
            frame_botoes,
            text="🔄 Converter e Traduzir",
            command=self.converter,
            font=("Segoe UI", 12, "bold"),
            bg=self.cor_destaque,
            fg="white",
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2",
            activebackground="#c1121f",
            activeforeground="white"
        )
        self.botao_converter.pack(side="left", padx=(50, 10))
        
        # Botão Copiar
        self.botao_copiar = tk.Button(
            frame_botoes,
            text="📋 Copiar resultado",
            command=self.copiar_resultado,
            font=("Segoe UI", 11),
            bg="#4cc9f0",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.botao_copiar.pack(side="left", padx=10)
        
        # Botão Limpar
        self.botao_limpar = tk.Button(
            frame_botoes,
            text="🧹 Limpar",
            command=self.limpar,
            font=("Segoe UI", 11),
            bg="#6c757d",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.botao_limpar.pack(side="left", padx=10)
        
        # Resultado
        frame_resultado = tk.Frame(self.root, bg="#f8f9fa", padx=20, pady=10)
        frame_resultado.pack(fill="both", expand=True)
        
        tk.Label(
            frame_resultado,
            text="Resultado:",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg="#1d3557"
        ).pack(anchor="w", pady=(0, 5))
        
        # Área de resultado
        self.resultado = tk.Text(
            frame_resultado,
            height=10,
            font=("Microsoft YaHei", 13),
            bg="#edf2f4",
            fg="#2b2d42",
            relief="solid",
            borderwidth=1,
            wrap="word",
            state="disabled"
        )
        self.resultado.pack(fill="both", expand=True, padx=5)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(self.resultado, command=self.resultado.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultado.config(yscrollcommand=scrollbar.set)
        
        # Bind Enter para converter
        self.root.bind("<Return>", lambda e: self.converter())
        self.root.bind("<KP_Enter>", lambda e: self.converter())
    
    def converter(self):
        texto = self.entrada.get("1.0", "end-1c").strip()
        
        if not texto:
            messagebox.showwarning("⚠️ Atenção!", "Digite algum texto em chinês, por favor.")
            return
        
        try:
            # Mostrar mensagem de carregamento
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", "⏳ Traduzindo... Aguarde um momento.")
            self.resultado.config(state="disabled")
            self.root.update()
            
            # Converte com e sem tons
            pinyin_com_tons = self._converter_com_tons(texto)
            pinyin_sem_tons = self._converter_sem_tons(texto)
            
            # Traduzir para português
            traducao_pt = self._traduzir_portugues(texto)
            
            # Formata resultado com espaçamento generoso (legibilidade)
            resultado_formatado = (
                f"🇨🇳 Chinês:\n{texto}\n\n"
                f"🔤 Pinyin (entonação):\n{pinyin_com_tons}\n\n"
                f"⌨️ Pinyin (sem entonacao):\n{pinyin_sem_tons}\n\n"
                f"🇧🇷 Português:\n{traducao_pt}"
            )
            
            # Exibe resultado
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", resultado_formatado)
            self.resultado.config(state="disabled")
            
            # Habilita botão copiar
            self.botao_copiar.config(state="normal")
            
        except Exception as e:
            messagebox.showerror(
                "❌ Erro",
                f"Erro ao traduzir:\n{str(e)}\n\n"
                "Verifique sua conexão com a internet."
            )
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.config(state="disabled")
    
    def _converter_com_tons(self, texto):
        resultado = pinyin(texto, style=Style.TONE)
        return " ".join([silaba[0] for silaba in resultado])
    
    def _converter_sem_tons(self, texto):
        return " ".join(lazy_pinyin(texto))
    
    def _traduzir_portugues(self, texto):
        """Traduz texto chinês para português."""
        try:
            return self.tradutor.translate(texto)
        except Exception as e:
            return f"[Erro na tradução: {str(e)}]"
    
    def copiar_resultado(self):
        resultado = self.resultado.get("1.0", "end-1c").strip()
        if resultado:
            self.root.clipboard_clear()
            self.root.clipboard_append(resultado)
            self.root.update()  # clipboard
            messagebox.showinfo("✅ Copiado", "Resultado copiado para a área de transferência!")
    
    def limpar(self):
        self.entrada.delete("1.0", "end")
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.config(state="disabled")
        self.botao_copiar.config(state="disabled")
        self.entrada.focus_set()

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorPinyinApp(root)
    root.mainloop()