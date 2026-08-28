import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_ensino():
    print("Iniciando migração do Módulo IDE...")
    
    # 1. Modulos
    for doc in db.collection('ide_modulos').stream():
        d = doc.to_dict()
        IdeModulo.objects.update_or_create(
            id=doc.id if doc.id.isdigit() else None,
            defaults={
                'nome': d.get('nome', ''),
                'duracaoNum': int(d.get('duracaoNum') or 1),
                'duracaoTipo': d.get('duracaoTipo', 'Semanas'),
                'perguntas': d.get('perguntas', []),
                'limiteFaltas': int(d.get('limiteFaltas') or 3),
                'gradeCurricular': d.get('gradeCurricular', [])
            }
        )
    print("✅ Módulos migrados!")

    # 2. Formularios
    for doc in db.collection('ide_formularios').stream():
        d = doc.to_dict()
        IdeFormulario.objects.create(
            moduloId=str(d.get('moduloId', '')),
            titulo=d.get('titulo', ''),
            ciclo=d.get('ciclo', ''),
            bannerUrl=d.get('bannerUrl'),
            linkWhatsapp=d.get('linkWhatsapp'),
            status=d.get('status', 'Aberto'),
            perguntas=d.get('perguntas', [])
        )
    print("✅ Formulários de Matrícula migrados!")

    # 3. Turmas
    for doc in db.collection('ide_turmas').stream():
        d = doc.to_dict()
        IdeTurma.objects.create(
            nome=d.get('nome', ''),
            codigoUnico=d.get('codigoUnico', ''),
            moduloId=str(d.get('moduloId', '')),
            moduloNome=d.get('moduloNome', ''),
            ciclo=d.get('ciclo', ''),
            professor=d.get('professor', ''),
            status=d.get('status', 'Ativa'),
            isEspera=bool(d.get('isEspera', False)),
            alunos=d.get('alunos', []),
            removidos=d.get('removidos', []),
            abonosReprovacao=d.get('abonosReprovacao', []),
            whatsappGrupo=d.get('whatsappGrupo', '')
        )
    print("✅ Turmas e Listas de Alunos migradas!")

    # 4. Inscrições
    count_insc = 0
    for doc in db.collection('ide_inscricoes').stream():
        d = doc.to_dict()
        IdeInscricao.objects.create(
            formularioId=str(d.get('formularioId', '')),
            moduloId=str(d.get('moduloId', '')),
            moduloNome=d.get('moduloNome', ''),
            alunoId=str(d.get('alunoId', '')),
            alunoNome=d.get('alunoNome', ''),
            celular=d.get('celular', ''),
            email=d.get('email', ''),
            lider=d.get('lider', ''),
            gc=d.get('gc', ''),
            sexo=d.get('sexo', ''),
            dataNascimento=d.get('dataNascimento', ''),
            estadoCivil=d.get('estadoCivil', ''),
            respostas=d.get('respostas', {})
        )
        count_insc += 1
    print(f"✅ {count_insc} Inscrições migradas!")

    # 5. Salas (Diários de Classe)
    for doc in db.collection('ide_salas').stream():
        d = doc.to_dict()
        IdeSala.objects.create(
            turmaId=str(d.get('turmaId', '')),
            turmaNome=d.get('turmaNome', ''),
            moduloId=str(d.get('moduloId', '')),
            tema=d.get('tema', ''),
            data=str(d.get('data', '')),
            diaSemana=d.get('diaSemana', ''),
            horarioInicio=d.get('horarioInicio', ''),
            horarioFim=d.get('horarioFim', ''),
            status=d.get('status', 'Agendada'),
            presencas=d.get('presencas', {}),
            justificativas=d.get('justificativas', {}),
            exercicioAtivo=bool(d.get('exercicioAtivo', False)),
            exercicioPerguntas=d.get('exercicioPerguntas', []),
            notasExercicio=d.get('notasExercicio', {}),
            respostasExercicio=d.get('respostasExercicio', {})
        )
    print("✅ Diários de Sala de Aula e Frequências migrados!")

migrar_ensino()