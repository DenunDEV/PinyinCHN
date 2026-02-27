# Autor: DeNun
# PinyinCHN — Conversor Didático Chinês ⇄ Pinyin ⇄ PT-BR
# Propósito: Ferramenta didática para aprendizado de chinês com foco em
#            clareza, simplicidade e experiência do estudante.
# ============================================================================

# Interface gráfica e utilitários
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import socket
import requests
from datetime import datetime

# Módulos do projeto
from core import ConversorPinyin, TradutorChines

# ============================================================================
# Mensagens de entrada

print("=" * 70)
print("Nihao! Bem vindo ao Meu Projeto Pinyin")
print("=" * 70)
print("  Isto é um conversor de chinês para pinyin e tradução em português.")
print("Caso tenha dicas e melhorias, por favor visite meu perfil no GitHub!")
print(f"\n                                            Iniciando app às {datetime.now().strftime('%H:%M:%S')}")
print("=" * 70)

# ============================================================================
class ConversorPinyinApp:
    # Inicializador
    
    def __init__(self, root):
        self.root = root
        self._configurar_janela()
        self._definir_cores()
        self._inicializar_componentes()
        self._criar_widgets()
        self._verificar_conexao()
    
    def _configurar_janela(self):
        self.root.title("PinyinCHN")
        self.root.geometry("960x740")
        self.root.resizable(True, True)
        self.root.configure(bg="#f8f9fa")
    
    def _definir_cores(self):
        self.cor_destaque = "#e63946"      # Vermelho vibrante (ação principal)
        self.cor_secundaria = "#457b9d"    # Azul suave (títulos)
        self.cor_fundo_campo = "#ffffff"   # Branco (campos de entrada)
        self.cor_borda = "#a8dadc"         # Azul claro (bordas)
        self.cor_historico = "#a29bfe"     # Roxo suave (histórico)
    
    def _inicializar_componentes(self):
        self.conversor_pinyin = ConversorPinyin()
        self.tradutor_chines = TradutorChines()
        
        self.logs = []
        self.historico = self._carregar_historico()
    
    # ------------------------------------------------------------------------
    # Criação e configuração dos widgets da interface
    
    def _criar_widgets(self):
        self._criar_cabecalho()
        self._criar_campo_entrada()
        self._criar_botoes_principais()
        self._criar_area_resultado()
        self._configurar_atalhos_teclado()
    
    def _criar_cabecalho(self):
        frame_header = tk.Frame(self.root, bg="#f8f9fa", pady=15)
        frame_header.pack(fill="x")
        
        titulo = tk.Label(
            frame_header,
            text="PinyinCHN",
            font=("Segoe UI", 18, "bold"),
            fg=self.cor_secundaria,
            bg="#f8f9fa"
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            frame_header,
            text="Digite em chinês para ver pinyin + tradução PT-BR",
            font=("Segoe UI", 10),
            fg="#6c757d",
            bg="#f8f9fa"
        )
        subtitulo.pack()
    
    def _criar_campo_entrada(self):
        frame_entrada = tk.Frame(self.root, bg="#f8f9fa", padx=25, pady=15)
        frame_entrada.pack(fill="x")
        
        tk.Label(
            frame_entrada,
            text="Texto em chinês:",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg="#1d3557"
        ).pack(anchor="w", pady=(0, 5))
        
        self.entrada = tk.Text(
            frame_entrada,
            height=3,
            font=("Microsoft YaHei", 14),
            bg=self.cor_fundo_campo,
            fg="#333333",
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightcolor=self.cor_borda
        )
        self.entrada.pack(fill="x", padx=5)
        self.entrada.focus_set()
        
        tk.Label(
            frame_entrada,
            text="Exemplo: 我爱你 ｜ 今天天气很好 ｜ 谢谢 ｜ 你叫什么名字",
            font=("Segoe UI", 9),
            fg="#6c757d",
            bg="#f8f9fa"
        ).pack(anchor="w", pady=(8, 0))
    
    def _criar_botoes_principais(self):
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
            padx=22,
            pady=10,
            cursor="hand2",
            activebackground="#c1121f",
            activeforeground="white"
        )
        self.botao_converter.pack(side="left", padx=(40, 8))
        
        # Botão Copiar
        self.botao_copiar = tk.Button(
            frame_botoes,
            text="📋 Copiar resultado",
            command=self.copiar_resultado,
            font=("Segoe UI", 11),
            bg="#4cc9f0",
            fg="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.botao_copiar.pack(side="left", padx=8)
        
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
        self.botao_limpar.pack(side="left", padx=8)
        
        # Botão Histórico
        self.botao_historico = tk.Button(
            frame_botoes,
            text="📚 Histórico",
            command=self.mostrar_historico,
            font=("Segoe UI", 11),
            bg=self.cor_historico,
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.botao_historico.pack(side="left", padx=8)
        
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
        self.botao_diagnostico.pack(side="left", padx=8)
    
    def _criar_area_resultado(self):
        frame_resultado = tk.Frame(self.root, bg="#f8f9fa", padx=25, pady=12)
        frame_resultado.pack(fill="both", expand=True)
        
        tk.Label(
            frame_resultado,
            text="Resultado:",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg="#1d3557"
        ).pack(anchor="w", pady=(0, 5))
        
        self.resultado = tk.Text(
            frame_resultado,
            height=11,
            font=("Microsoft YaHei", 13),
            bg="#edf2f4",
            fg="#2b2d42",
            relief="solid",
            borderwidth=1,
            wrap="word",
            state="disabled"
        )
        self.resultado.pack(fill="both", expand=True, padx=5)
        
        scrollbar = ttk.Scrollbar(self.resultado, command=self.resultado.yview)
        scrollbar.pack(side="right", fill="y")
        self.resultado.config(yscrollcommand=scrollbar.set)
    
    def _configurar_atalhos_teclado(self):
        self.root.bind("<Return>", lambda e: self.converter())
        self.root.bind("<KP_Enter>", lambda e: self.converter())
    
    # ------------------------------------------------------------------------
    # Conversão e tradução principal
    
    def converter(self):
        texto = self.entrada.get("1.0", "end-1c").strip()
        
        if not texto:
            messagebox.showwarning("⚠️ Atenção!", "Digite algum texto em chinês, por favor.")
            return
        
        try:
            # Etapa 1: Mensagem de carregamento
            self._exibir_mensagem_carregamento()
            
            # Etapa 2: Verificar conexão
            if not self._testar_conexao_rapida():
                self._adicionar_mensagem_resultado("\n⚠️  Conexão instável ou lenta.")
            
            # Etapa 3: Converter pinyin
            self._adicionar_mensagem_resultado("\n🔤 Convertendo pinyin...")
            inicio_pinyin = datetime.now()
            
            pinyin_resultado = self.conversor_pinyin.converter_completo(texto)
            tempo_pinyin = (datetime.now() - inicio_pinyin).total_seconds()
            
            self._adicionar_mensagem_resultado(f"\n✅ Pinyin convertido em {tempo_pinyin:.2f}s")
            
            pinyin_com_tons = pinyin_resultado['com_tons']
            pinyin_sem_tons = pinyin_resultado['sem_tons']
            
            # Etapa 4: Traduzir para português
            self._adicionar_mensagem_resultado("\n🌐 Traduzindo para português...")
            inicio_traducao = datetime.now()
            
            traducao_pt = self.tradutor_chines.traduzir_com_fallback(
                texto,
                fallback="[Sem tradução - verifique conexão]"
            )
            tempo_traducao = (datetime.now() - inicio_traducao).total_seconds()
            
            self._adicionar_mensagem_resultado(f"\n✅ Tradução concluída em {tempo_traducao:.2f}s")
            
            # Etapa 5: Formatar e exibir resultado final
            resultado_formatado = (
                f"🇨🇳 Chinês:\n{texto}\n\n"
                f"🔤 Pinyin (entonação):\n{pinyin_com_tons}\n\n"
                f"⌨️  Pinyin (sem entonação):\n{pinyin_sem_tons}\n\n"
                f"🇧🇷 Português:\n{traducao_pt}\n\n"
                f"⏱️  Tempo total: {tempo_pinyin + tempo_traducao:.2f}s"
            )
            
            self._exibir_resultado(resultado_formatado)
            self.botao_copiar.config(state="normal")
            
            # Etapa 6: Salvar no histórico
            self.adicionar_ao_historico(
                texto=texto,
                pinyin_tons=pinyin_com_tons,
                pinyin_sem_tons=pinyin_sem_tons,
                traducao=traducao_pt
            )
            
            self.logs.append(f"✅ '{texto[:30]}...' traduzido em {tempo_pinyin + tempo_traducao:.2f}s")
            
        except Exception as e:
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
            self._exibir_resultado(f"❌ Erro: {str(e)}\n\nDetalhes no console.")
            self.logs.append(f"❌ Erro: {str(e)}")
    
    def _exibir_mensagem_carregamento(self):
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", "⏳ Processando...\n\nVerificando conexão...")
        self.resultado.config(state="disabled")
        self.root.update()
    
    def _adicionar_mensagem_resultado(self, mensagem):
        self.resultado.config(state="normal")
        self.resultado.insert("end", mensagem)
        self.resultado.config(state="disabled")
        self.root.update()
    
    def _exibir_resultado(self, texto):
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.config(state="disabled")
    
    # ------------------------------------------------------------------------
    # Organização de histórico de conversões
    
    def _carregar_historico(self):
        try:
            if os.path.exists("historico.json"):
                with open("historico.json", "r", encoding="utf-8") as f:
                    historico = json.load(f)
                    return historico[-50:] if isinstance(historico, list) else []
            return []
        except Exception as e:
            print(f"⚠️  Erro ao carregar histórico: {e}")
            self.logs.append(f"⚠️  Erro ao carregar histórico: {e}")
            return []
    
    def _salvar_historico(self):
        try:
            historico_para_salvar = self.historico[-50:]
            with open("historico.json", "w", encoding="utf-8") as f:
                json.dump(historico_para_salvar, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Erro ao salvar histórico: {e}")
            self.logs.append(f"⚠️  Erro ao salvar histórico: {e}")
    
    def adicionar_ao_historico(self, texto, pinyin_tons, pinyin_sem_tons, traducao):
        entrada = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chinês": texto,
            "pinyin_tons": pinyin_tons,
            "pinyin_sem_tons": pinyin_sem_tons,
            "português": traducao
        }
        self.historico.append(entrada)
        self._salvar_historico()
        self.logs.append(f"📚 Histórico: '{texto[:20]}...' salvo")
    
    def mostrar_historico(self):
        if not self.historico:
            messagebox.showinfo("📚 Histórico", "Nenhuma conversão salva ainda.")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("📚 Histórico de Conversões")
        janela.geometry("720x580")
        janela.configure(bg="#f8f9fa")
        
        # Título
        tk.Label(
            janela,
            text="📚 Histórico de Conversões (últimas 30)",
            font=("Segoe UI", 16, "bold"),
            fg=self.cor_secundaria,
            bg="#f8f9fa",
            pady=15
        ).pack()
        
        # Frame da lista
        frame_lista = tk.Frame(janela, bg="#f8f9fa", padx=20, pady=10)
        frame_lista.pack(fill="both", expand=True)
        
        # Treeview para exibir histórico
        colunas = ("data", "chinês", "pinyin", "português")
        tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=18)
        
        tree.heading("data", text="Data/Hora")
        tree.heading("chinês", text="Chinês")
        tree.heading("pinyin", text="Pinyin (tons)")
        tree.heading("português", text="Português")
        
        tree.column("data", width=150, anchor="w")
        tree.column("chinês", width=90, anchor="center")
        tree.column("pinyin", width=190, anchor="w")
        tree.column("português", width=210, anchor="w")
        
        # Adicionar entradas (mais recente primeiro)
        for entrada in reversed(self.historico[-30:]):
            tree.insert("", "end", values=(
                entrada["data"],
                entrada["chinês"],
                entrada["pinyin_tons"],
                entrada["português"]
            ))
        
        tree.pack(fill="both", expand=True, side="left")
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.config(yscrollcommand=scrollbar.set)
        
        # Botões inferiores
        frame_botoes = tk.Frame(janela, bg="#f8f9fa", pady=15)
        frame_botoes.pack(fill="x")
        
        # Botão Copiar
        def copiar_selecionado():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showwarning("⚠️ Atenção", "Selecione uma entrada primeiro.")
                return
            
            item = tree.item(selecionado[0])
            valores = item["values"]
            texto_completo = (
                f"🇨🇳 {valores[1]}\n"
                f"🔤 {valores[2]}\n"
                f"🇧🇷 {valores[3]}"
            )
            
            janela.clipboard_clear()
            janela.clipboard_append(texto_completo)
            messagebox.showinfo("✅ Copiado", "Entrada copiada para a área de transferência!")
        
        tk.Button(
            frame_botoes,
            text="📋 Copiar Selecionado",
            command=copiar_selecionado,
            font=("Segoe UI", 11),
            bg="#4cc9f0",
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side="left", padx=20)
        
        # Botão Limpar
        def limpar_historico():
            if messagebox.askyesno("⚠️ Confirmar", "Deseja apagar todo o histórico?"):
                self.historico.clear()
                self._salvar_historico()
                janela.destroy()
                self.mostrar_historico()
                self.logs.append("🗑️ Histórico limpo pelo usuário")
        
        tk.Button(
            frame_botoes,
            text="🗑️ Limpar Histórico",
            command=limpar_historico,
            font=("Segoe UI", 11),
            bg=self.cor_destaque,
            fg="white",
            relief="flat",
            padx=20,
            pady=10
        ).pack(side="left", padx=20)
        
        # Botão Fechar
        tk.Button(
            frame_botoes,
            text="Fechar",
            command=janela.destroy,
            font=("Segoe UI", 11, "bold"),
            bg="#6c757d",
            fg="white",
            relief="flat",
            padx=30,
            pady=10
        ).pack(side="right", padx=20)
    
    # ------------------------------------------------------------------------
    # Diagnóstico de conexão e sistema

    def _verificar_conexao(self):
        print("\n Verificando conexão com a internet...")
        
        try:
            # Corrigido: removidos espaços extras nas URLs
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print(" Conexão com internet: OK")
            self.logs.append(" Internet: Conectado")
            
            response = requests.get("https://translate.google.com", timeout=5)
            if response.status_code == 200:
                print(" Google Translate: Acessível")
                self.logs.append(" Google Translate: Online")
            else:
                print(f" Google Translate: Status {response.status_code}")
                self.logs.append(f" Google Translate: Status {response.status_code}")
                
        except socket.timeout:
            print(" Erro: Timeout ao verificar conexão")
            self.logs.append(" Internet: Timeout")
            messagebox.showwarning(
                " Conexão Lenta",
                " A conexão com a internet está lenta ou instável.\n"
                " A tradução pode demorar ou falhar."
            )
        except Exception as e:
            print(f" Erro ao verificar conexão: {str(e)}")
            self.logs.append(f" Internet: {str(e)}")
            messagebox.showwarning(
                " Sem Conexão",
                " Não foi possível verificar a conexão com a internet.\n"
                " A tradução online não funcionará.\n\n"
                f" Erro: {str(e)}"
            )
    
    def _testar_conexao_rapida(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except:
            return False
    
    def mostrar_diagnostico(self):
        janela = tk.Toplevel(self.root)
        janela.title("🔧 Diagnóstico do Sistema")
        janela.geometry("650x600")
        janela.configure(bg="#f8f9fa")
        
        tk.Label(
            janela,
            text="🔧 Diagnóstico do Sistema",
            font=("Segoe UI", 16, "bold"),
            fg=self.cor_secundaria,
            bg="#f8f9fa",
            pady=15
        ).pack()
        
        texto_diagnostico = tk.Text(
            janela,
            height=25,
            font=("Consolas", 10),
            bg="#edf2f4",
            fg="#2b2d42",
            relief="solid",
            borderwidth=1,
            wrap="word"
        )
        texto_diagnostico.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Coletar informações
        diagnostico = []
        diagnostico.append("=" * 60)
        diagnostico.append("DIAGNÓSTICO DO SISTEMA - PinyinCHN")
        diagnostico.append("=" * 60)
        diagnostico.append(f"\nData/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        diagnostico.append("\n" + "=" * 60)
        diagnostico.append("1. CONEXÃO COM INTERNET")
        diagnostico.append("=" * 60)
        
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            diagnostico.append("DNS Google (8.8.8.8): CONECTADO")
        except Exception as e:
            diagnostico.append(f"DNS Google (8.8.8.8): {str(e)}")
        
        try:
            response = requests.get("https://www.google.com", timeout=5)
            diagnostico.append(f"Google.com: ONLINE (Status {response.status_code})")
        except Exception as e:
            diagnostico.append(f"Google.com: {str(e)}")
        
        try:
            response = requests.get("https://translate.google.com", timeout=5)
            diagnostico.append(f"Google Translate: ONLINE (Status {response.status_code})")
        except Exception as e:
            diagnostico.append(f"Google Translate: {str(e)}")
        
        diagnostico.append("\n" + "=" * 60)
        diagnostico.append("2. BIBLIOTECAS")
        diagnostico.append("=" * 60)
        
        try:
            import pypinyin
            diagnostico.append(f"pypinyin: {pypinyin.__version__}")
        except Exception as e:
            diagnostico.append(f"pypinyin: {str(e)}")
        
        try:
            import deep_translator
            diagnostico.append(f"deep-translator: {deep_translator.__version__}")
        except Exception as e:
            diagnostico.append(f"deep-translator: {str(e)}")
        
        diagnostico.append("\n" + "=" * 60)
        diagnostico.append("3. HISTÓRICO DE OPERAÇÕES")
        diagnostico.append("=" * 60)
        
        if self.logs:
            for i, log in enumerate(self.logs[-15:], 1):
                diagnostico.append(f"{i:2d}. {log}")
        else:
            diagnostico.append("Nenhuma operação registrada ainda.")
        
        diagnostico.append("\n" + "=" * 60)
        diagnostico.append("4. DICAS PARA RESOLVER PROBLEMAS")
        diagnostico.append("=" * 60)
        diagnostico.append("""
• Se estiver com VPN, tente desativar temporariamente
• Verifique se o firewall/antivírus não está bloqueando o Python
• Tente reiniciar o roteador/modem
• Se usar rede corporativa/escolar, pode haver bloqueio
• O Google Translate tem limite de requisições por IP
• Tente esperar 1-2 minutos entre traduções seguidas
""")
        diagnostico.append("\n" + "=" * 60)
        diagnostico.append("FIM DO DIAGNÓSTICO")
        diagnostico.append("=" * 60)
        
        texto_diagnostico.insert("1.0", "\n".join(diagnostico))
        texto_diagnostico.config(state="disabled")
        
        tk.Button(
            janela,
            text="Fechar",
            command=janela.destroy,
            font=("Segoe UI", 11, "bold"),
            bg=self.cor_secundaria,
            fg="white",
            relief="flat",
            padx=30,
            pady=10
        ).pack(pady=15)
    
    # ------------------------------------------------------------------------
    # UTILITÁRIOS
    
    def copiar_resultado(self):
        resultado = self.resultado.get("1.0", "end-1c").strip()
        if resultado:
            self.root.clipboard_clear()
            self.root.clipboard_append(resultado)
            self.root.update()
            messagebox.showinfo("✅ Copiado", "Resultado copiado para a área de transferência!")
    
    def limpar(self):
        self.entrada.delete("1.0", "end")
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.config(state="disabled")
        self.botao_copiar.config(state="disabled")
        self.entrada.focus_set()


# ============================================================================
# Execução do aplicativo

if __name__ == "__main__":
    print("\n ...Iniciando interface gráfica...")
    root = tk.Tk()
    app = ConversorPinyinApp(root)
    print("\n                   Interface carregada com sucesso!")
    print("\n                           DICAS RÁPIDAS:\n")
    print("         • Digite chinês e pressione ENTER para converter")
    print("         • Clique em 'Histórico' para revisar frases estudadas")
    print("         • Use 'Copiar' para salvar resultados em anotações")
    print("\n" + "=" * 70)
    print()
    
    root.mainloop()
    
    print("\n App encerrado. Bai Bai!\n")