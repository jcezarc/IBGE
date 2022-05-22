import sys
import re
import requests

URL_API = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'


class FrequenciaNome:
    def __init__(self, nome: str):
        self.nome = nome
        dados = requests.get(
            URL_API.format(nome=nome)
        ).json() # ex.: [{'periodo': ..., 'frequencia': ...}]
        self.periodos = {}
        if not dados:
            return
        for valores in dados[0]['res']:
            self.inclui_periodo(**valores)  
    
    def inclui_periodo(self, periodo: str, frequencia :int):
        """
        A api do IBGE devolve o `período` assim '[1940,1950['
        """
        faixa = [int(a) for a in re.findall(r'\d+', periodo)]
        if len(faixa) != 2:
            return 'Período inválido'
        for ano in range(*faixa):
            self.periodos[ano] = frequencia
        self.media = sum(self.periodos.values()) / len(self.periodos)

    def anos_mais_comuns(self) -> list:
        return [a for a, f in self.periodos.items() if f > self.media]

    def anos_menos_comuns(self) -> list:
        return [a for a, f in self.periodos.items() if f < self.media]

    def exibe_grafico(self):
        import matplotlib.pyplot as plt
        anos = list(self.periodos.keys())
        freq = list(self.periodos.values())
        plt.title(self.nome)
        plt.bar(anos, freq)
        plt.show()


if len(sys.argv) > 1:
    nome = sys.argv[1]
else:
    nome = input('Qual o nome? ')
freq = FrequenciaNome(nome)
# print('Anos mais comuns:\n\t', freq.anos_mais_comuns())
# print('Anos menos comuns:\n\t', freq.anos_menos_comuns())
freq.exibe_grafico()
