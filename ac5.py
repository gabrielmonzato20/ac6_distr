from flask import Flask,jsonify,request

app = Flask(__name__)
alunos = []
professorres = []
disciplinas = []
ofertadas = []
@app.route('/alunos')
def retorna_alunos():
    return jsonify(alunos)
@app.route('/alunos', methods=['POST'])
def add_aluno():
    new = request.json
    if 'nome' not in new.keys():
        return jsonify({'erro':'aluno sem nome'}),400
    for aluno in alunos:
        if aluno['id'] == new['id']:
            return jsonify({'erro':'id ja utilizada'}),400
   
    alunos.append(request.json)
    return jsonify(alunos),200
 
@app.route('/alunos/<int:id>')
def retorna_aluno_id(id):
    for aluno in alunos:
        if aluno['id'] == id:
            return  jsonify(aluno) 
    return jsonify({'erro':'aluno nao encontrado',}),400
@app.route('/reseta',methods=['POST'])
def reseta_():
    alunos.clear()
    professorres.clear()
    disciplinas.clear()
    ofertadas.clear()
    return jsonify({'ok':'resetado com sucesso'}),200
@app.route('/alunos/<int:id>',methods=['DELETE'])
def delete_aluno(id):
    for index,aluno in enumerate(alunos):
        if aluno['id'] == id:
           del alunos[index]
           return
    return jsonify({'erro':'aluno nao encontrado'}),400
@app.route("/alunos/<int:id>",methods=['PUT'])
def edita(id):
    dados = request.json
    if  'nome' not in dados.keys():
        return jsonify({'erro':'aluno sem nome'}),400
    for aluno in alunos:
        if aluno['id'] == id:
            aluno['nome'] = dados['nome']
            return jsonify(alunos)
  
    return jsonify({'erro':'aluno nao encontrado',}),400
@app.route("/professores",methods=['GET'])
def professor_show():
    return jsonify(professorres)
@app.route("/professores",methods=['POST'])
def add_prof():
    prof=request.json
    if 'nome' in prof.keys():
        for professor in professorres:
            if professor['id'] == prof['id']:
                return jsonify({'erro':'id ja utilizada'}),400
        professorres.append(prof)
        return jsonify({}),200
    else:
        return jsonify({'erro':'professor sem nome'}),400             
@app.route('/professores/<int:id>')
def retorna_professor(id):
    for professor in professorres:
        if professor['id'] == id:
            return jsonify(professor)
    return jsonify({'erro':'professor nao encontrado'}),400
@app.route('/professores/<int:id>',methods=['DELETE'])
def delete_prof(id):

    for index,prof in enumerate(professorres):
        if prof['id'] == id :
            del professorres[index]
            return 
    return jsonify({'erro':'professor nao encontrado'}),400
@app.route('/professores/<int:id>',methods=['PUT'])
def edita_prof(id):
    g = request.json
    if 'nome' in g.keys():
        for professor in professorres:
            if professor['id'] == id:
                professor['nome'] = g['nome']
                return jsonify(professor)
        return jsonify({'erro':'professor nao encontrado'}),400
    else:
        return jsonify({'erro':'professor sem nome'}),400
@app.route('/disciplinas',methods=['GET'])
def diciplinas_retorno():
    return jsonify( disciplinas)
@app.route('/disciplinas',methods=['POST'])
def add_diciplinas():
    dados = request.json
    if 'nome' not in dados.keys() or 'id' not in dados.keys() or 'carga_horaria' not in dados.keys() or 'plano_ensino' not in dados.keys() or 'status' not in dados.keys():
        return jsonify({'erro':'diciplina sem nome'}),400
    for disciplina in disciplinas:
        if disciplina['id'] == dados['id']:
            return jsonify({'erro':'id ja utilizada'}),400
    
    else:
        disciplinas.append(dados)
        return jsonify(),200
@app.route('/disciplinas/<int:id>',methods=['GET'])
def diciplina_id(id):
    for diciplina in disciplinas:
        if diciplina['id'] == id:
            return  jsonify(diciplina)
    return jsonify({'erro':'disciplina nao encontrada'}),400
@app.route('/disciplinas/<int:id>',methods=['DELETE'])
def delete_diciplina(id):
    for index,diciplina in enumerate(disciplinas):
        if diciplina['id'] == id:
            del disciplinas[index]
            return 'Diciplina deletada com sucesso'
    return jsonify({'erro':'disciplina nao encontrada'}),400
@app.route('/disciplinas/<int:id>',methods=['PUT'])
def edita_diciplina(id):
    dados=request.json
    for diciplina in disciplinas:
        if diciplina['id'] == id:
            if 'nome' in dados.keys():
                diciplina['nome'] = dados['nome']
            if 'status' in dados.keys():
                disciplina['status'] = dados['status']
            if 'plano_ensino' in dados.keys():
                disciplina['plano_ensino'] = dados['plano_ensino']
            if 'carga_horaria' in dados.keys():
                disciplina['carga_horaria'] = dados['carga_horaria']
        return 'Diciplina Atualizada com sucesso'
    return jsonify({'erro':'disciplina nao encontrada'}),400
@app.route("/ofertadas",methods=['GET'])
def retrona_ofertada():
    return jsonify(ofertadas)
@app.route('/ofertadas',methods=['POST'])
def add_ofertada():
    dados = request.json

    if 'id_professor' in dados.keys():
        professor_valido = False
        ok_add = True
        for professor in professorres:
            if professor['id'] == dados['id_professor']:
                professor_valido = True
        if professor_valido == False:
            return jsonify({'erro' : 'id professor invalido'}),400
    print(len(dados.keys()))
    if len(dados.keys()) >=5:
        for ofertada in ofertadas:
            if ofertada['id'] == dados['id']:
                return jsonify({'erro':'id ja utilizada'}),400
        ofertadas.append(dados)
        return jsonify(),200
    else:
        return jsonify({'erro':'data faltando'}),400
@app.route('/ofertadas/<int:id>',methods=['GET'])
def retorna_id_disp(id):
    for ofertada in ofertadas:
        if ofertada['id'] == id:
            return jsonify( ofertada)
    return jsonify({'erro':'ofertada nao encontrada'}),400 
@app.route('/ofertadas/<int:id>',methods=['DELETE'])
def deleta_ofertada(id):
    for index,ofertada in enumerate(ofertadas):
        if ofertada['id'] == id:
            del ofertadas[index]
            return jsonify(),200
    return jsonify({'erro':'ofertada nao encontrada'}),400 
@app.route('/ofertadas/<int:id>',methods=['PUT'])
def edita_ofertada(id):
    dados = request.json
    for ofertada in ofertadas:
        if ofertada['id'] == id:
            if 'ano' in dados.keys():
                ofertada['ano'] =dados['ano']
            if 'semestre' in dados.keys():
                ofertada['semestre'] = dados['semestre']
            if 'turma' in dados.keys():
                ofertada['turma'] = dados['turma']
            if 'data' in dados.keys():
                ofertada['data'] = dados['data']
            if 'id_professor' in dados.keys():
                ofertada['id_professor']=dados['id_professor']
            return jsonify(),200
    return jsonify({'erro':'ofertada nao encontrada'}),400

         
if __name__ == '__main__':
    app.run(port=5002,debug=True,host='localhost')
