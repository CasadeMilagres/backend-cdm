import os
import django
import firebase_admin
from firebase_admin import credentials, firestore
from google.api_core.exceptions import GoogleAPICallError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import GcLancamentoSemanal, ConfiguracaoSistema

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_dados_gc_paginado():
    print("Limpando lançamentos anteriores de GC...")
    GcLancamentoSemanal.objects.all().delete()

    print("Iniciando migração em lotes dos Lançamentos de GC...")
    colecao = db.collection('gc_semanal_gc').order_by('__name__')
    
    tamanho_lote = 50
    ultimo_doc = None
    total_migrados = 0

    while True:
        query = colecao.limit(tamanho_lote)
        if ultimo_doc:
            query = query.start_after(ultimo_doc)

        docs = list(query.get())
        if not docs:
            break

        for doc in docs:
            d = doc.to_dict()
            data_raw = d.get('dataGc') or '2026-01-01'
            if len(data_raw) > 10:
                data_raw = data_raw[:10]

            GcLancamentoSemanal.objects.create(
                grupoId=str(d.get('grupoId', '')),
                lider=str(d.get('lider', 'Sem Líder'))[:150],
                bairro=str(d.get('bairro', ''))[:100],
                dataGc=data_raw,
                horario=str(d.get('horario', ''))[:50],
                statusGc=d.get('statusGc', 'Ocorreu'),
                motivoNaoOcorreu=d.get('motivoNaoOcorreu', ''),
                membros=int(d.get('membros') or 0),
                membrosPresentesIds=d.get('membrosPresentesIds', []),
                visitantes=int(d.get('visitantes') or 0),
                oferta=float(d.get('oferta') or 0.0),
                observacao=d.get('observacao', ''),
                teveOracaoCura=d.get('teveOracaoCura', ''),
                qtdCurados=int(d.get('qtdCurados') or 0),
                testemunhoCura=d.get('testemunhoCura', ''),
                imagemUrl=d.get('imagemUrl'),
                usuarioResponsavel=str(d.get('usuarioResponsavel', 'Admin'))[:150]
            )
            total_migrados += 1

        ultimo_doc = docs[-1]
        print(f"-> Lote processado. Total até agora: {total_migrados} registros.")

    print(f"✅ {total_migrados} Lançamentos Semanais migrados com sucesso!")

    # Migrar configurações de template WhatsApp
    try:
        doc_zap = db.collection('configuracoes_sistema').document('whatsapp_gc').get()
        if doc_zap.exists:
            ConfiguracaoSistema.objects.update_or_create(
                chave='whatsapp_gc',
                defaults={'valor': doc_zap.to_dict()}
            )
            print("✅ Configurações de WhatsApp migradas!")
    except Exception as e:
        print(f"Aviso ao migrar config de zap: {e}")

migrar_dados_gc_paginado()