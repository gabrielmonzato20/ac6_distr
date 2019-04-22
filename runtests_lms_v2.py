import requests
import unittest

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        r = requests.get('http://localhost:5002/alunos')
        self.assertEqual(type(r.json()),type([]))

    def test_001_adiciona_alunos(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5002/alunos')
        achei_fernando = False
        achei_roberto = False
        for aluno in r_lista.json():
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'mario','id':20})
        r_id = requests.get('http://localhost:5002/alunos/20')
        self.assertEqual(r_id.json()['nome'],'mario')


    
    def test_003_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_004_adiciona_e_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/alunos',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/alunos/28')
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_005_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/alunos',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5002/alunos/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/alunos/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5002/alunos/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_006_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/alunos/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        r = requests.get('http://localhost:5002/alunos/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        r = requests.delete('http://localhost:5002/alunos/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')

    def test_007_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_008_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    

    
    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_100b_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/alunos',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)

    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5002/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')

    def test_102_professores_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'mario','id':20})
        r_lista = requests.get('http://localhost:5002/professores/20')
        self.assertEqual(r_lista.json()['nome'],'mario')


    
    def test_103_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_104_adiciona_e_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5002/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_107_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'bond','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'james','id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5002/professores',json={'nome':'maximus','id':7})
        self.assertEqual(r.status_code,200)
        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_109_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/professores',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)

    def test_200_disciplinas_retorna_lista(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.get('http://localhost:5002/disciplinas')
        self.assertEqual(type(r.json()),type([]))
        self.assertEqual(len(r.json()),0)
    
    def test_200b_nao_confundir_disciplina_e_pessoas(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/disciplinas')
        self.assertEqual(len(r_lista.json()),0)

    def test_201_adiciona_disciplinas(self):
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        r = requests.post('http://localhost:5002/disciplinas',json={'id':101,'nome':'distribuidos','status':12,'plano_ensino':'clientes e servidores','carga_horaria':10})
        r_lista = requests.get('http://localhost:5002/disciplinas')
        achei_dados = False
        achei_distribuidos = False
        for disciplina in r_lista.json():
            if 'dados' in disciplina['nome']:
                achei_dados = True
            if 'distri' in disciplina['nome']:
                achei_distribuidos = True
        if not achei_dados:
            self.fail('disciplina estrutura de dados nao apareceu na lista de disciplinas')
        if not achei_distribuidos:
            self.fail('disciplina distribuidos nao apareceu na lista de disciplinas')

    def test_202_disciplinas_por_id(self):
        r = requests.post('http://localhost:5002/disciplinas',json={'id':103,'nome':'matematica','status':12,'plano_ensino':'funcoes e calculo','carga_horaria':15})
        r_lista = requests.get('http://localhost:5002/disciplinas/103')
        self.assertEqual(r_lista.json()['nome'],'matematica')
        self.assertEqual(r_lista.json()['plano_ensino'],'funcoes e calculo')
        self.assertEqual(r_lista.json()['carga_horaria'],15)
        self.assertEqual(r_lista.json()['status'],12)



    
    def test_203_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/disciplinas',json={'id':104,'nome':'lp2','status':12,'plano_ensino':'dicionarios e classes','carga_horaria':15})
        r_lista = requests.get('http://localhost:5002/disciplinas')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/disciplinas')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_204_adiciona_e_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        r = requests.post('http://localhost:5002/disciplinas',json={'id':101,'nome':'distribuidos','status':12,'plano_ensino':'clientes e servidores','carga_horaria':10})
        r_lista = requests.get('http://localhost:5002/disciplinas')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/disciplinas/100')
        r_lista = requests.get('http://localhost:5002/disciplinas')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_205_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        r_antes = requests.get('http://localhost:5002/disciplinas/100')
        self.assertEqual(r_antes.json()['nome'],'estruturas de dados')
        requests.put('http://localhost:5002/disciplinas/100', json={'nome':'algoritmos'})
        r_depois = requests.get('http://localhost:5002/disciplinas/100')
        self.assertEqual(r_depois.json()['nome'],'algoritmos')

    def test_206_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/disciplinas/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'disciplina nao encontrada')
        r = requests.get('http://localhost:5002/disciplinas/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'disciplina nao encontrada')
        r = requests.delete('http://localhost:5002/disciplinas/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'disciplina nao encontrada')

    def test_207_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'distribuidos','status':12,'plano_ensino':'clientes e servidores','carga_horaria':10})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_208_post_com_campos_faltando(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/disciplinas',json={         'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/disciplinas',json={'id':101,                             'status':12,'plano_ensino':'dados','carga_horaria':15})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/disciplinas',json={'id':102,'nome':'estruturas de dados','status':12,                       'carga_horaria':15})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/disciplinas',json={'id':103,'nome':'estruturas de dados','status':12,'plano_ensino':'dados'})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
    
    def test_300_ofertadas_retorna_lista(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.get('http://localhost:5002/ofertadas')
        self.assertEqual(type(r.json()),type([]))
        self.assertEqual(len(r.json()),0)
    
    def test_300b_nao_confundir_ofertada_e_outras_entidades(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/alunos',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'nome':'roberto','id':2})
        r = requests.post('http://localhost:5002/disciplinas',json={'id':100,'nome':'estruturas de dados','status':12,'plano_ensino':'dados','carga_horaria':15})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertEqual(len(r_lista.json()),0)

    def test_301_adiciona_ofertadas(self):
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13'})
        r = requests.post('http://localhost:5002/ofertadas',json={'id':101,'ano':2019,'semestre':1,'turma':'ADS3','data':'2019-04-13'})
        r_lista = requests.get('http://localhost:5002/ofertadas')
        achei_ads = False
        achei_si = False
        for ofertada in r_lista.json():
            if 'SI' in ofertada['turma']:
                achei_si = True
            if 'ADS' in ofertada['turma']:
                achei_ads = True
        if not achei_ads:
            self.fail('ofertada de ads nao apareceu na lista de ofertadas')
        if not achei_si:
            self.fail('ofertada de si nao apareceu na lista de ofertadas')

    def test_302_disciplinas_por_id(self):
        r = requests.post('http://localhost:5002/ofertadas',json={'id':110,'ano':2010,'semestre':1,'turma':'ADS2','data':'2010-04-20'})
        r_lista = requests.get('http://localhost:5002/ofertadas/110')
        self.assertEqual(r_lista.json()['turma'],'ADS2')
        self.assertEqual(r_lista.json()['data'],'2010-04-20')
        self.assertEqual(r_lista.json()['ano'],2010)
        self.assertEqual(r_lista.json()['semestre'],1)



    
    def test_303_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5002/ofertadas',json={'id':110,'ano':2010,'semestre':2,'turma':'GTI2','data':'2010-04-20'})
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/ofertadas')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_304_adiciona_e_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13'})
        r = requests.post('http://localhost:5002/ofertadas',json={'id':1,'ano':2019,'semestre':1,'turma':'ADS3','data':'2019-11-13'})
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/ofertadas/100')
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_305_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':1,'ano':2019,'semestre':1,'turma':'ADS3','data':'2019-11-13'})
        r_antes = requests.get('http://localhost:5002/ofertadas/1')
        self.assertEqual(r_antes.json()['turma'],'ADS3')
        requests.put('http://localhost:5002/ofertadas/1', json={'turma':'ADS2'})
        r_depois = requests.get('http://localhost:5002/ofertadas/1')
        self.assertEqual(r_depois.json()['turma'],'ADS2')

    def test_306_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/ofertadas/10',json={'ano':2019,'data':'2019-11-13'})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'ofertada nao encontrada')
        r = requests.get('http://localhost:5002/ofertadas/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'ofertada nao encontrada')
        r = requests.delete('http://localhost:5002/ofertadas/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'ofertada nao encontrada')

    def test_307_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13'})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2011,'semestre':1,'turma':'ADS3','data':'2011-11-23'})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_308_post_com_campos_faltando(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13'})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={         'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13'})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/ofertadas',json={'id':101,           'semestre':1,'turma':'SI3','data':'2019-04-13'})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/ofertadas',json={'id':102,'ano':2019,             'turma':'SI3','data':'2019-04-13'})
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        r = requests.post('http://localhost:5002/ofertadas',json={'id':103,'ano':2019,'semestre':1,'turma':'SI3'                    })
        self.assertEqual(r.status_code,400)
        self.assertTrue('erro' in r.json())
        self.assertEqual(r.json()['erro'],'data faltando')
        
        
    def test_309_professor_deve_ser_valido_ao_criar_ofertada(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13','id_professor':500})
        self.assertEqual(r.status_code,400)
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertTrue(len(r_lista.json()) == 0)
        requests.post('http://localhost:5002/professores',json={'nome':'lucas','id':500})
        r = requests.post('http://localhost:5002/ofertadas',json={'id':100,'ano':2019,'semestre':1,'turma':'SI3','data':'2019-04-13','id_professor':500})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/ofertadas')
        self.assertTrue(len(r_lista.json()) == 1)
        



        


        





    

    


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
