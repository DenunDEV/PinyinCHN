# por favor instale as dependências antes de rodar: 
# pip install pypinyin  e  deep-translator

import tkinter as tk
from tkinter import ttk, messagebox                                     # exibir mensagens de alerta e erro
from core import ConversorPinyin, TradutorChines      # Conversão e tradução pasta core
import socket                                                                                    # Verificação de conexão
import requests                                                                               # Teste a acessibilidade do Google Translate
from datetime import datetime                                               # Horário de início e logs de diagnóstico

print("nihao! Bem vindo ao DnG Project")
print("Isto é um conversor de texto chinês para pinyin e tradução em português.")
print("Caso de dicas e melhorias, por favor visite meu perfil no github! bai bai")
print(f"\n🕒 Iniciando app às {datetime.now().strftime('%H:%M:%S')}")


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
        
        # Inicia tradutor - RENOMEADO para evitar conflito com método converter()
        self.conversor_pinyin = ConversorPinyin()
        self.tradutor_chines = TradutorChines()
        
        # Variável para logs
        self.logs = []
        
        self._criar_widgets()
        self._verificar_conexao()
    
    def _verificar_conexao(self):
        """Verifica se há conexão com a internet antes de iniciar."""
        print("\n📡Verificando conexão com a internet...")
        
        try:
            # Conect - Google DNS (rápido e confiável)
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print("✅ Conexão com internet: OK")
            self.logs.append("✅ Internet: Conectado")
            
            # acessando Google Translate
            response = requests.get("https://translate.google.com", timeout=5)
            if response.status_code == 200:
                print("✅ Google Translate: Acessível")
                self.logs.append("✅ Google Translate: Online")
            else:
                print(f"⚠️  Google Translate: Status {response.status_code}")
                self.logs.append(f"⚠️  Google Translate: Status {response.status_code}")
                
        except socket.timeout:
            print("❌ Erro: Timeout ao verificar conexão")
            self.logs.append("❌ Internet: Timeout")
            messagebox.showwarning(
                "⚠️ Conexão Lenta",
                "A conexão com a internet está lenta ou instável.\n"
                "A tradução pode demorar ou falhar."
            )
        except Exception as e:
            print(f"❌ Erro ao verificar conexão: {str(e)}")
            self.logs.append(f"❌ Internet: {str(e)}")
            messagebox.showwarning(
                "⚠️ Sem Conexão",
                "Não foi possível verificar a conexão com a internet.\n"
                "A tradução online não funcionará.\n\n"
                f"Erro: {str(e)}"
            )
    
    # Criação dos widgets da interface
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
        
        # Botão Diagnóstico
        self.botao_diagnostico = tk.Button(
            frame_botoes,
            text="🔧 Diagnóstico",
            command=self.mostrar_diagnostico,
            font=("Segoe UI", 11),
            bg="#ffb703",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.botao_diagnostico.pack(side="left", padx=10)
        
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
        
        # Bind Enter para converter | Permite usar Enter para converter, melhorando a usabilidade
        self.root.bind("<Return>", lambda e: self.converter())
        self.root.bind("<KP_Enter>", lambda e: self.converter())
    
    def converter(self):
        texto = self.entrada.get("1.0", "end-1c").strip() 
        
        if not texto:
            messagebox.showwarning("⚠️ Atenção!", "Digite algum texto em chinês, por favor.")
            return
        
        try:
            # Mensagem de carregamento
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", "⏳ Processando...\n\nVerificando conexão...")
            self.resultado.config(state="disabled")
            self.root.update()
            
            # Verificar conexão antes de traduzir
            if not self._testar_conexao_rapida():
                self.resultado.config(state="normal")
                self.resultado.insert("end", "\n⚠️  Conexão instável ou lenta.")
                self.resultado.config(state="disabled")
                self.root.update()
            
            # Converte com e sem entonação (usando módulo core)
            self.resultado.config(state="normal")
            self.resultado.insert("end", "\n🔤 Convertendo pinyin...")
            self.resultado.config(state="disabled")
            self.root.update()
            
            inicio_pinyin = datetime.now()
            pinyin_resultado = self.conversor_pinyin.converter_completo(texto)
            tempo_pinyin = (datetime.now() - inicio_pinyin).total_seconds()
            
            self.resultado.config(state="normal")
            self.resultado.insert("end", f"\n✅ Pinyin convertido em {tempo_pinyin:.2f}s")
            self.resultado.config(state="disabled")
            self.root.update()
            
            pinyin_com_tons = pinyin_resultado['com_tons']
            pinyin_sem_tons = pinyin_resultado['sem_tons']
            
            # Traduzir para português (usando módulo core)
            self.resultado.config(state="normal")
            self.resultado.insert("end", "\n🌐 Traduzindo para português...")
            self.resultado.config(state="disabled")
            self.root.update()
            
            inicio_traducao = datetime.now()
            traducao_pt = self.tradutor_chines.traduzir_com_fallback(
                texto,
                fallback=None  # Não usar fallback automático para ver o erro real
            )
            tempo_traducao = (datetime.now() - inicio_traducao).total_seconds()
            
            if traducao_pt is None:
                # Capturar erro específico
                import traceback
                erro_detalhado = traceback.format_exc()
                
                self.resultado.config(state="normal")
                self.resultado.delete("1.0", "end")
                self.resultado.insert("1.0", 
                    f"❌ ERRO NA TRADUÇÃO\n\n"
                    f"Tempo de tentativa: {tempo_traducao:.2f}s\n\n"
                    f"O pinyin foi convertido com sucesso:\n"
                    f"🔤 Pinyin (entonação): {pinyin_com_tons}\n"
                    f"⌨️  Pinyin (sem entonação): {pinyin_sem_tons}\n\n"
                    f"⚠️  Mas a tradução falhou. Possíveis causas:\n"
                    f"   • Conexão lenta ou instável\n"
                    f"   • Servidor do Google Translate indisponível\n"
                    f"   • Muitas requisições seguidas (limite atingido)\n"
                    f"   • Firewall/Antivírus bloqueando\n\n"
                    f"💡 Dica: Clique em '🔧 Diagnóstico' para mais informações."
                )
                self.resultado.config(state="disabled")
                
                self.logs.append(f"❌ Tradução falhou após {tempo_traducao:.2f}s")
                return
            
            self.resultado.config(state="normal")
            self.resultado.insert("end", f"\n✅ Tradução concluída em {tempo_traducao:.2f}s")
            self.resultado.config(state="disabled")
            self.root.update()
            
            # Formata resultado com espaçamento generoso (legibilidade)
            resultado_formatado = (
                f"🇨🇳 Chinês:\n{texto}\n\n"
                f"🔤 Pinyin (entonação):\n{pinyin_com_tons}\n\n"
                f"⌨️  Pinyin (sem entonação):\n{pinyin_sem_tons}\n\n"
                f"🇧🇷 Português:\n{traducao_pt}\n\n"
                f"⏱️  Tempo total: {tempo_pinyin + tempo_traducao:.2f}s"
            )
            
            # Exibe resultado
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", resultado_formatado)
            self.resultado.config(state="disabled")
            
            # Habilita botão copiar
            self.botao_copiar.config(state="normal")
            
            # Registrar log
            self.logs.append(f"✅ '{texto}' traduzido em {tempo_pinyin + tempo_traducao:.2f}s")
            
        except Exception as e:     # Captura erros de tradução ou conversão
            import traceback
            erro_completo = traceback.format_exc()
            
            print(f"\n❌ ERRO DETALHADO:\n{erro_completo}")
            
            messagebox.showerror(
                "❌ Erro",
                f"Erro ao processar:\n{str(e)}\n\n"
                f"Verifique:\n"
                f"• Sua conexão com a internet\n"
                f"• Se o firewall/antivírus não está bloqueando\n"
                f"• Tente novamente em alguns segundos"
            )
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", "end")
            self.resultado.insert("1.0", f"❌ Erro: {str(e)}\n\nDetalhes no console.")
            self.resultado.config(state="disabled")
            
            self.logs.append(f"❌ Erro: {str(e)}")
    
    def _testar_conexao_rapida(self):  # 
        # Testa rapidamente se há conexão com a internet.
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except:
            return False
    
    def mostrar_diagnostico(self):
        # Mostra janela com diagnóstico detalhado.
        janela = tk.Toplevel(self.root)
        janela.title("🔧 Diagnóstico do Sistema")
        janela.geometry("600x500")
        janela.configure(bg="#f8f9fa")
        
        # Título
        tk.Label(
            janela,
            text="🔧 Diagnóstico do Sistema",
            font=("Segoe UI", 16, "bold"),
            fg=self.cor_secundaria,
            bg="#f8f9fa",
            pady=15
        ).pack()
        
        # Área de texto
        texto_diagnostico = tk.Text(
            janela,
            height=20,
            font=("Consolas", 10),
            bg="#edf2f4",
            fg="#2b2d42",
            relief="solid",
            borderwidth=1,
            wrap="word"
        )
        texto_diagnostico.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Coletar informações de diagnóstico
        diagnostico = []
        diagnostico.append("=" * 50)
        diagnostico.append("DIAGNÓSTICO DO SISTEMA - PinyinCHN")
        diagnostico.append("=" * 50)
        diagnostico.append(f"\n📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        diagnostico.append("\n" + "=" * 50)
        diagnostico.append("1. CONEXÃO COM INTERNET")
        diagnostico.append("=" * 50)
        
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            diagnostico.append("✅ DNS Google (8.8.8.8): CONECTADO")
        except socket.timeout:
            diagnostico.append("❌ DNS Google (8.8.8.8): TIMEOUT")
        except Exception as e:
            diagnostico.append(f"❌ DNS Google (8.8.8.8): {str(e)}")
        
        try:
            response = requests.get("https://www.google.com", timeout=5)
            diagnostico.append(f"✅ Google.com: ONLINE (Status {response.status_code})")
        except requests.exceptions.Timeout:
            diagnostico.append("❌ Google.com: TIMEOUT")
        except Exception as e:
            diagnostico.append(f"❌ Google.com: {str(e)}")
        
        try:
            response = requests.get("https://translate.google.com", timeout=5)
            diagnostico.append(f"✅ Google Translate: ONLINE (Status {response.status_code})")
        except requests.exceptions.Timeout:
            diagnostico.append("❌ Google Translate: TIMEOUT")
        except Exception as e:
            diagnostico.append(f"❌ Google Translate: {str(e)}")
        
        diagnostico.append("\n" + "=" * 50)
        diagnostico.append("2. BIBLIOTECAS")
        diagnostico.append("=" * 50)
        
        try:
            import pypinyin
            diagnostico.append(f"✅ pypinyin: {pypinyin.__version__}")
        except Exception as e:
            diagnostico.append(f"❌ pypinyin: {str(e)}")
        
        try:
            import deep_translator
            diagnostico.append(f"✅ deep-translator: {deep_translator.__version__}")
        except Exception as e:
            diagnostico.append(f"❌ deep-translator: {str(e)}")
        
        diagnostico.append("\n" + "=" * 50)
        diagnostico.append("3. HISTÓRICO DE OPERAÇÕES")
        diagnostico.append("=" * 50)
        
        if self.logs:
            for i, log in enumerate(self.logs[-10:], 1):  # Últimos 10 logs
                diagnostico.append(f"{i}. {log}")
        else:
            diagnostico.append("Nenhuma operação registrada ainda.")
        
        diagnostico.append("\n" + "=" * 50)
        diagnostico.append("4. DICAS PARA RESOLVER PROBLEMAS")
        diagnostico.append("=" * 50)
        diagnostico.append(

            """
• Se estiver com VPN, tente desativar temporariamente
• Verifique se o firewall/antivírus não está bloqueando o Python
• Tente reiniciar o roteador/modem
• Se usar rede corporativa/escolar, pode haver bloqueio
• O Google Translate tem limite de requisições por IP
• Tente esperar 1-2 minutos entre traduções seguidas
            """
        )
        
        diagnostico.append("\n" + "=" * 50)
        diagnostico.append("FIM DO DIAGNÓSTICO")
        diagnostico.append("=" * 50)
        
        # Exibir diagnóstico
        texto_diagnostico.insert("1.0", "\n".join(diagnostico))
        texto_diagnostico.config(state="disabled")
        
        # Botão fechar
        tk.Button(
            janela,
            text="Fechar",
            command=janela.destroy,
            font=("Segoe UI", 11, "bold"),
            bg=self.cor_secundaria,
            fg="white",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        ).pack(pady=10)
    
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