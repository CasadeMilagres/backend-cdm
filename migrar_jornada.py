import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import JornadaCadastro, ConfiguracaoSistema

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_jornada():
    print("🚀 Iniciando migração da Jornada Casa de Milagres...")
    
    JornadaCadastro.objects.all().delete()

    # 1. Configurações
    doc_conf = db.collection('configuracoes').document('jornada').get()
    if doc_conf.exists:
        ConfiguracaoSistema.objects.update_or_create(
            chave='jornada',
            defaults={'valor': doc_conf.to_dict()}
        )
        print("   ✓ Configurações de automação e mensagens importadas.")

    # 2. Cadastros da Jornada
    docs = db.collection('jornada_cadastros').stream()
    cadastros = []
    for doc in docs:
        d = doc.to_dict()
        data_cadastro = d.get('dataCadastro') or d.get('dataConclusao')
        
        cadastros.append(JornadaCadastro(
            id=doc.id,  # Mantemos o ID para os links públicos antigos funcionarem
            cadastroId=d.get('cadastroId', ''),
            nome=d.get('nome', 'Sem Nome'),
            celular=str(d.get('celular', ''))[:50],
            etapa=int(d.get('etapa', 0)),
            exportado=bool(d.get('exportado', False)),
            cobrancaAtivada=bool(d.get('cobrancaAtivada', False)),
            cobrancaEnviosCount=int(d.get('cobrancaEnviosCount', 0)),
            historicoMensagens=d.get('historicoMensagens', []),
            cursosConcluidos=d.get('cursosConcluidos', []),
            jornadaConcluida=bool(d.get('jornadaConcluida', False))
        ))
    
    JornadaCadastro.objects.bulk_create(cadastros, batch_size=500)
    print(f"🎉 Migração Finalizada! {len(cadastros)} alunos na Jornada importados.")

if __name__ == '__main__':
    migrar_jornada()