import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

# Altere "ministerios" se você tiver nomeado o app de outra forma
from usuarios.models import Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_ministerio():
    print("🚀 Iniciando migração do módulo Ministério...")

    min_map = {}
    evento_map = {}
    vol_map = {}

    # 1. MIGRAR MINISTÉRIOS
    print("Migrando Ministérios...")
    docs_min = db.collection('ministerios').stream()
    for doc in docs_min:
        d = doc.to_dict()
        novo_min = Ministerio.objects.create(
            nome=d.get('nome', 'Sem Nome'),
            lideres=d.get('lideres', []),
            funcoes=d.get('funcoes', [])
        )
        # Salva o mapeamento: ID velho -> ID novo
        min_map[doc.id] = str(novo_min.id)

    # 2. MIGRAR EVENTOS
    print("Migrando Eventos...")
    docs_ev = db.collection('eventos_ministerio').stream()
    for doc in docs_ev:
        d = doc.to_dict()
        novo_ev = EventoMinisterio.objects.create(
            nome=d.get('nome', 'Sem Nome')
        )
        evento_map[doc.id] = str(novo_ev.id)

    # 3. MIGRAR VOLUNTÁRIOS
    print("Migrando Voluntários...")
    docs_vol = db.collection('voluntarios').stream()
    for doc in docs_vol:
        d = doc.to_dict()
        
        # Atualiza a lista de IDs de ministérios com os novos IDs do Postgres
        min_antigos = d.get('ministerios', [])
        min_novos = [min_map[m] for m in min_antigos if m in min_map]

        novo_vol = Voluntario.objects.create(
            cadastroId=d.get('cadastroId', ''),
            nome=d.get('nome', 'Sem Nome'),
            telefone=d.get('telefone', ''),
            email=d.get('email', ''),
            sexo=d.get('sexo', ''),
            liderGc=d.get('liderGc', ''),
            ministerios=min_novos
        )
        vol_map[doc.id] = str(novo_vol.id)

    # 4. MIGRAR ESCALAS
    print("Migrando Escalas...")
    docs_esc = db.collection('escalas_ministerio').stream()
    for doc in docs_esc:
        d = doc.to_dict()
        
        min_id_antigo = d.get('ministerioId', '')
        min_id_novo = min_map.get(min_id_antigo, min_id_antigo)

        ev_id_antigo = d.get('eventoId', '')
        ev_id_novo = evento_map.get(ev_id_antigo, ev_id_antigo)

        # Atualiza os IDs dos voluntários dentro da lista de escalados
        escalados_antigos = d.get('escalados', [])
        escalados_novos = []
        for esc in escalados_antigos:
            vol_id_antigo = esc.get('voluntarioId', '')
            vol_id_novo = vol_map.get(vol_id_antigo, vol_id_antigo)
            
            escalados_novos.append({
                "voluntarioId": vol_id_novo,
                "nome": esc.get('nome', ''),
                "telefone": esc.get('telefone', ''),
                "funcao": esc.get('funcao', ''),
                "status": esc.get('status', 'Pendente')
            })

        data_escala = d.get('data')
        if not data_escala:
            continue

        EscalaMinisterio.objects.create(
            ministerioId=min_id_novo,
            ministerioNome=d.get('ministerioNome', ''),
            data=data_escala,
            eventoId=ev_id_novo,
            evento=d.get('evento', ''),
            escalados=escalados_novos
        )

    print(f"\n✅ Migração Concluída com Sucesso!")
    print(f"   - {len(min_map)} Ministérios")
    print(f"   - {len(evento_map)} Eventos")
    print(f"   - {len(vol_map)} Voluntários")
    print("   - Escalas importadas corretamente!")

if __name__ == '__main__':
    migrar_ministerio()