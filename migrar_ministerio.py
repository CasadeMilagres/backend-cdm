import os
import django
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def formatar_data(val):
    if not val:
        return None
    if hasattr(val, 'strftime'):
        return val.strftime('%Y-%m-%d')
    val_str = str(val).strip()
    if '/' in val_str:
        partes = val_str.split('/')
        if len(partes) == 3:
            return f"{partes[2]}-{partes[1].zfill(2)}-{partes[0].zfill(2)}"
    return val_str[:10]

def migrar_ministerio():
    print("🚀 Limpando tabelas antigas e reiniciando migração...")
    EscalaMinisterio.objects.all().delete()
    Voluntario.objects.all().delete()
    EventoMinisterio.objects.all().delete()
    Ministerio.objects.all().delete()

    min_map = {}
    evento_map = {}
    vol_map = {}

    # 1. MINISTÉRIOS
    print("Importando Ministérios...")
    for doc in db.collection('ministerios').stream():
        d = doc.to_dict()
        novo_min = Ministerio.objects.create(
            nome=d.get('nome', 'Sem Nome'),
            lideres=d.get('lideres', []),
            funcoes=d.get('funcoes', [])
        )
        min_map[doc.id] = str(novo_min.id)

    # 2. EVENTOS
    print("Importando Eventos...")
    for doc in db.collection('eventos_ministerio').stream():
        d = doc.to_dict()
        novo_ev = EventoMinisterio.objects.create(nome=d.get('nome', 'Sem Nome'))
        evento_map[doc.id] = str(novo_ev.id)

    # 3. VOLUNTÁRIOS
    print("Importando Voluntários...")
    for doc in db.collection('voluntarios').stream():
        d = doc.to_dict()
        min_antigos = d.get('ministerios', [])
        min_novos = [min_map[m] for m in min_antigos if m in min_map]

        novo_vol = Voluntario.objects.create(
            cadastroId=d.get('cadastroId', ''),
            nome=d.get('nome', 'Sem Nome'),
            telefone=d.get('telefone', '')[:20] if d.get('telefone') else '',
            email=d.get('email', '') if (d.get('email') and '@' in d.get('email')) else None,
            sexo=d.get('sexo', ''),
            liderGc=d.get('liderGc', ''),
            ministerios=min_novos
        )
        vol_map[doc.id] = str(novo_vol.id)

    # 4. ESCALAS
    print("Importando Escalas...")
    escalas_count = 0
    for doc in db.collection('escalas_ministerio').stream():
        d = doc.to_dict()
        data_formatada = formatar_data(d.get('data'))
        if not data_formatada:
            continue

        min_id_novo = min_map.get(d.get('ministerioId', ''), str(d.get('ministerioId', '')))
        ev_id_novo = evento_map.get(d.get('eventoId', ''), str(d.get('eventoId', '')))

        escalados_novos = []
        for esc in d.get('escalados', []):
            vol_id_novo = vol_map.get(esc.get('voluntarioId', ''), str(esc.get('voluntarioId', '')))
            escalados_novos.append({
                "voluntarioId": vol_id_novo,
                "nome": esc.get('nome', ''),
                "telefone": esc.get('telefone', ''),
                "funcao": esc.get('funcao', ''),
                "status": esc.get('status', 'Pendente')
            })

        EscalaMinisterio.objects.create(
            ministerioId=min_id_novo,
            ministerioNome=d.get('ministerioNome', ''),
            data=data_formatada,
            eventoId=ev_id_novo,
            evento=d.get('evento', ''),
            escalados=escalados_novos
        )
        escalas_count += 1

    print(f"\n✅ Migração Finalizada com Sucesso!")
    print(f"   - {len(min_map)} Ministérios")
    print(f"   - {len(evento_map)} Eventos")
    print(f"   - {len(vol_map)} Voluntários")
    print(f"   - {escalas_count} Escalas importadas!")

if __name__ == '__main__':
    migrar_ministerio()