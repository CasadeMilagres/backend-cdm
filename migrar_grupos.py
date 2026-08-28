import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import GrupoConexao

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_apenas_grupos():
    print("Limpando Grupos antigos...")
    GrupoConexao.objects.all().delete()
    
    print("Migrando Grupos do Firebase...")
    docs = db.collection('grupos_conexao_gc').stream()
    count = 0
    for doc in docs:
        d = doc.to_dict()
        GrupoConexao.objects.create(
            nome=str(d.get('nome', ''))[:150],
            lider=str(d.get('lider', ''))[:150],
            coLider=str(d.get('coLider', ''))[:150],
            lider_supervisor=str(d.get('liderSupervisor', ''))[:150],
            supervisor=str(d.get('supervisor', ''))[:150],
            coordenador=str(d.get('coordenador', ''))[:150],
            anfitriao=str(d.get('anfitriao', ''))[:150],
            telefoneLider=str(d.get('telefoneLider', ''))[:50],
            telefoneAnfitriao=str(d.get('telefoneAnfitriao', ''))[:50],
            endereco=str(d.get('endereco', ''))[:255],
            numero=str(d.get('numero', ''))[:20],
            bairro=str(d.get('bairro', ''))[:100],
            cep=str(d.get('cep', ''))[:20],
            dia_gc=str(d.get('diaSemana', '') or d.get('dia_gc', ''))[:50],
            horario=str(d.get('horario', ''))[:50],
            generoGc=str(d.get('generoGc', 'Misto'))[:50],
            tipoGc=str(d.get('tipoGc', 'Família'))[:50]
        )
        count += 1
    print(f"✅ {count} Grupos migrados com sucesso!")

migrar_apenas_grupos()