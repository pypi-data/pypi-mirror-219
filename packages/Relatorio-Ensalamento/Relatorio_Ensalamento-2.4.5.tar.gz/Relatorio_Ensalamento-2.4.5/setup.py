from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name = 'Relatorio_Ensalamento',
    version = '2.4.5',
    author = 'Matheus Henrique Rosa',
    author_email = 'm.rosa1@pucpr.br',
    packages = ['Relatorio_Ensalamento','Sugestao','Unificar_XML'],
    description = 'Conversor utilizado para a geração do relatorio ensalamento',
    long_description = readme,
    license = 'MIT',
    keywords = 'conversor relatorio ensalamento',
)

