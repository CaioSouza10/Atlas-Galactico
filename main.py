from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt
from rich.align import Align
from rich.traceback import install
install()


class Planeta:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo


class Estrela:
    def __init__(self, nome, temperatura):
        self.nome = nome
        self.temperatura = temperatura
        self.planetas = []

    def adicionar_planetas(self, obj):
        self.planetas.append(obj)

    def calcular_planetas(self):
        return len(self.planetas)
    
    def exibir_sistema(self):
        sistema = Table(title=f':star:NOME DA ESTRELA: {self.nome}:star:', title_justify='center', style='bold blue')
        sistema.add_column('NOME PLANETA', justify='center', style='yellow')
        sistema.add_column('TIPO', justify='center', style='green')
        for p in self.planetas:
            sistema.add_row(p.nome, p.tipo)
        print(Align.center(sistema))
        if self.temperatura > 5000:
            detalhest = f'[red]TEMP: {self.temperatura}K | QUENTE[/]:fire:'
            cor_borda = 'red'
        else:
            detalhest = f'[blue]{self.temperatura}K | FRIO[/]:ice:'
            cor_borda = 'blue'
        resumo = Panel(f'Sistema: {self.nome}\nPlanetas: {self.calcular_planetas()}', title=detalhest, expand=False, border_style=cor_borda)    
        print(Align.center(resumo))
            

galaxia = []

try:
    with open('mapa_estelar.txt', 'r') as arquivo:
        for i in arquivo:
            leitura = i.strip().split(';')
            if not leitura or len(leitura) < 2:
                continue
            primeiro_indice = leitura[0].split(',')
            nome_estrela = primeiro_indice[0]
            temperatura = float(primeiro_indice[1])
            dados_estrela = Estrela(nome_estrela, temperatura)
            segundo_indice = leitura[1]
            detalhes_estrela = segundo_indice.split('|')
            for d in detalhes_estrela:
                detalhes = d.split(',')
                if len(detalhes) == 2:
                    nome_planeta = detalhes[0]
                    tipo_planeta = detalhes[1]
                    dados_planeta = Planeta(nome_planeta, tipo_planeta)
                    dados_estrela.adicionar_planetas(dados_planeta)
            galaxia.append(dados_estrela)
        print(f'[green]{len(galaxia)} dados carregados com sucesso![/]')
except FileNotFoundError:
    print('[red]Não há nada salvo no arquivo no momento![/]')
except Exception as e:
    print(f'[red]Erro ao carregar o arquivo: {e}[/]')


while True:
    estrela_nome = Prompt.ask('Nome da estrela')
    estrela_temperatura = FloatPrompt.ask('Temperatura da estrela')
    if not estrela_nome or not estrela_temperatura:
        print('O campo não pode estar vazio!')
        continue
    estrela_nova = Estrela(estrela_nome,estrela_temperatura)
    while True:
        planeta_nome = Prompt.ask('Nome do planeta').upper().strip()
        planeta_tipo = Prompt.ask('Tipo do planeta').upper().strip()
        if not planeta_nome or not planeta_tipo:
            print('O campo não pode estar vazio!')
            continue
        planeta_novo = Planeta(planeta_nome,planeta_tipo)
        estrela_nova.adicionar_planetas(planeta_novo)
        r = Prompt.ask('Deseja adicionar um novo planeta?[S/N]').upper().strip()
        if r in 'Nn':
            break
    galaxia.append(estrela_nova)    
    pergunta = Prompt.ask('Deseja adicionar uma nova estrela?[S/N]').upper().strip()
    if pergunta in 'Nn':
        break    


for g in galaxia:
    g.exibir_sistema()


try:
    with open('mapa_estelar.txt', 'w') as arquivo:
        for g in galaxia:
            lista_formatada = [f'{i.nome},{i.tipo}' for i in g.planetas]
            dados_formatados = '|'.join(lista_formatada)
            dados_completos = f'{g.nome},{g.temperatura};{dados_formatados}\n'
            arquivo.write(dados_completos)
        print('[green]Dados salvos com sucesso![/]')
except Exception as e:
    print('[red]Erro ao salvar os dados no arquivo![/]')        
except KeyboardInterrupt:
    print('Por favor, preencha todos os campos corretamente!')                