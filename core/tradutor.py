from deep_translator import GoogleTranslator
from typing import Optional

class TradutorChines:
    
    def __init__(self, idioma_origem: str = 'zh-CN', idioma_destino: str = 'pt'):
        self.idioma_origem = idioma_origem
        self.idioma_destino = idioma_destino
        self.tradutor = GoogleTranslator(
            source=idioma_origem,
            target=idioma_destino
        )
    
    def traduzir(self, texto: str) -> Optional[str]:
        if not texto or not isinstance(texto, str):
            return None
        
        try:
            return self.tradutor.translate(texto)
        except Exception as e:
            return None
    
    def traduzir_com_fallback(self, texto: str, fallback: str = "[Erro na tradução]") -> str:
        resultado = self.traduzir(texto)
        return resultado if resultado is not None else fallback