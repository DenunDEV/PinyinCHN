from pypinyin import pinyin, Style, lazy_pinyin
from typing import Dict

class ConversorPinyin:

    @staticmethod
    def converter_com_tons(texto: str) -> str:
        if not texto or not isinstance(texto, str):
            return ""
        
        resultado = pinyin(texto, style=Style.TONE)
        return " ".join([silaba[0] for silaba in resultado])
    
    @staticmethod
    def converter_sem_tons(texto: str) -> str:
        if not texto or not isinstance(texto, str):
            return ""
        
        return " ".join(lazy_pinyin(texto))
    
    @classmethod
    def converter_completo(cls, texto: str) -> Dict[str, str]:
        return {
            'com_tons': cls.converter_com_tons(texto),
            'sem_tons': cls.converter_sem_tons(texto)
        }