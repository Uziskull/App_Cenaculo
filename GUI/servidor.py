from flask import jsonify
from modelos import Proposta, Utilizador
import requests

class DB:
    url = None
    headers = None

    def __init__(self, url="localhost:5000"):
        self.url = url
        self.headers = {'Informacao-Dramatica': 'mama que eh de uva'}

    def ver_todas_propostas(self):
        """Retorna uma lista de todas as propostas."""
        r = requests.get(self.url + '/propostas', headers=self.headers)
        return [Proposta(p.id, p.description, p.order, None)
            for p in r.json()]
    
    def ver_todas_propostas_e_votos(self):
        """Retorna uma lista de todas as propostas existentes,
        assim como os votos atuais de cada uma."""
        r = requests.get(self.url + '/propostas/votos', headers=self.headers)
        return [Proposta(p.id, p.description, p.order, tuple(p.sim, p.nao, p.abster))
            for p in r.json()]
    
    def ver_proposta_ativa(self):
        """Retorna a proposta atualmente aberta a votos, caso exista."""
        r = requests.get(self.url + '/propostas/ativa', headers=self.headers)
        if r.status_code == 204:
            return None
        p = r.json()
        return Proposta(p.id, p.description, p.order, None)
    
    def criar_proposta(self, description: str):
        """Cria uma nova proposta, com a descrição dada.
        Retorna essa mesma proposta."""
        r = requests.post(self.url + '/propostas', headers=self.headers,
            data=jsonify({"description": description}))
        if r.status_code != 201:
            raise Exception(r.text)
        p = r.json()
        return Proposta(p.id, p.description, p.order, None)
    
    def atualizar_votos_proposta(self, proposta: Proposta):
        """Atualiza os votos desta proposta para os votos atuais.
        Retorna a mesma proposta, com os votos atualizados."""
        r = requests.get(self.url + '/propostas/' + proposta.id + '/votos',
            headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
        p = r.json()
        proposta.votos = (p.sim, p.nao, p.abster)
        return proposta
    
    def alterar_proposta(self, proposta: Proposta):
        """Altera a ordem e/ou descrição da proposta no servidor,
        caso tenham sido alteradas."""
        r = requests.patch(self.url + '/propostas/' + proposta.id,
            headers=self.headers, data=jsonify(proposta))
        if r.status_code != 200:
            raise Exception(r.text)
    
    def apagar_proposta(self, proposta: Proposta):
        """Apaga uma proposta da lista."""
        r = requests.delete(self.url + '/propostas/' + proposta.id,
            headers=self.headers)
        if r.status_code != 204:
            raise Exception(r.text)
    
    def abrir_votos_proposta(self, proposta: Proposta):
        """Abre uma proposta a votos, permitindo utilizadores votarem nela.
        Retorna erro se a proposta já estiver aberta a votos."""
        r = requests.post(self.url + '/propostas/' + proposta.id + '/abrir',
            headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
    
    def fechar_votos_proposta(self, proposta: Proposta):
        """Fecha a altura de votação de uma proposta.
        Retorna erro se a proposta não estiver aberta para votação."""
        r = requests.post(self.url + '/propostas/' + proposta.id + '/fechar',
            headers=self.headers)
        if r.status_code != 200:
            raise Exception(r.text)
    
    # -----------------------------------
    
    def ver_utilizadores(self):
        """Retorna uma lista de todos os utilizadores."""
        r = requests.get(self.url + '/utilizadores', headers=self.headers)
        return [Utilizador(u.token, u.email) for u in r.json()]
    
    def adicionar_utilizadores(self, emails: list):
        """Adiciona todos os utilizadores na lista de emails dada.
        Retorna erro se algum email já esteja a ser utilizado."""
        r = requests.post(self.url + '/utilizadores', headers=self.headers,
            data=jsonify(emails))
        if r.status_code != 200:
            raise Exception(r.text)
        return [Utilizador(u.token, u.email) for u in r.json()]
    
    def remover_utilizador(self, utilizador: Utilizador):
        """Remove um utilizador que já exista."""
        r = requests.delete(self.url + '/utilizadores/' + utilizador.id,
            headers=self.headers)
        if r.status_code != 204:
            raise Exception(r.text)

class TestDB:
    pass