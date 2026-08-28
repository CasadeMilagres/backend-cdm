import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import FormularioAvulso

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_formularios():
    print("Limpando formulários avulsos antigos no banco de dados...")
    FormularioAvulso.objects.all().delete()

    print("Iniciando busca de Formulários Avulsos no Firebase...")
    docs = db.collection('formularios_avulsos').stream()
    
    contador = 0
    for doc in docs:
        dados = doc.to_dict()
        
        # Cria o formulário no PostgreSQL
        FormularioAvulso.objects.create(
            titulo=str(dados.get('titulo', 'Sem Título'))[:255],
            bannerUrl=dados.get('bannerUrl', None),
            configuracaoCampos=dados.get('configuracaoCampos', {}),
            perguntasCustomizadas=dados.get('perguntasCustomizadas', []),
            criadoPor=str(dados.get('criadoPor', 'Admin'))[:150]
        )
        contador += 1
        print(f"- Importado: {dados.get('titulo')}")
        
    print(f"✅ {contador} Formulário(s) migrado(s) com sucesso!")

migrar_formularios()