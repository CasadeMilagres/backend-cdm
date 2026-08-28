import os
import django
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import (
    ProdutoComercial, ClienteComercial, VendaComercial,
    PendenciaComercial, EntradaEstoqueComercial, ContaPagarComercial
)

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def parse_datetime(val):
    if not val:
        return datetime.now().isoformat()
    if hasattr(val, 'isoformat'):
        return val.isoformat()
    return str(val).strip()

def parse_date(val):
    if not val:
        return None
    if isinstance(val, (datetime, date)):
        return val.strftime('%Y-%m-%d')
    val_str = str(val).strip()
    if 'T' in val_str:
        return val_str.split('T')[0]
    if '/' in val_str:
        p = val_str.split('/')
        if len(p) == 3:
            return f"{p[2]}-{p[1].zfill(2)}-{p[0].zfill(2)}"
    return val_str[:10]

def buscar_colecao_em_lotes(nome_colecao, batch_size=300):
    """Busca documentos paginados para evitar o erro de DeadlineExceeded"""
    col_ref = db.collection(nome_colecao)
    documentos = []
    query = col_ref.order_by('__name__').limit(batch_size)
    
    while True:
        try:
            resultados = list(query.stream(timeout=120.0))
            if not resultados:
                break
            documentos.extend(resultados)
            if len(resultados) < batch_size:
                break
            ultimo_doc = resultados[-1]
            query = col_ref.order_by('__name__').start_after(ultimo_doc).limit(batch_size)
        except Exception as e:
            print(f"      [Aviso] Reconectando lote da coleção {nome_colecao}...")
            break
            
    return documentos

def migrar_comercial():
    print("🚀 Iniciando migração otimizada de Cafeteria e Livraria...")
    
    ProdutoComercial.objects.all().delete()
    ClienteComercial.objects.all().delete()
    VendaComercial.objects.all().delete()
    PendenciaComercial.objects.all().delete()
    EntradaEstoqueComercial.objects.all().delete()
    ContaPagarComercial.objects.all().delete()

    modulos = ['cafeteria', 'livraria']
    
    for mod in modulos:
        print(f"\n--- Processando módulo: {mod.upper()} ---")
        prod_map = {}

        # 1. PRODUTOS
        print("1/6 - Importando Produtos...")
        docs_prod = buscar_colecao_em_lotes(f'produtos_{mod}')
        for doc in docs_prod:
            d = doc.to_dict()
            p = ProdutoComercial.objects.create(
                modulo=mod,
                codigo=int(d.get('codigo') or 0),
                nome=d.get('nome', 'Sem Nome'),
                codigoBarras=d.get('codigoBarras', ''),
                precoCusto=float(d.get('precoCusto') or 0.0),
                precoVenda=float(d.get('precoVenda') or 0.0),
                estoque=int(d.get('estoque') or 0),
                imagemUrl=d.get('imagemUrl', None),
                categoria=d.get('categoria', '')
            )
            prod_map[doc.id] = str(p.id)
        print(f"   ✓ {len(prod_map)} produtos importados.")

        # 2. CLIENTES
        print("2/6 - Importando Clientes...")
        docs_cli = buscar_colecao_em_lotes(f'clientes_{mod}')
        clientes_para_criar = []
        for doc in docs_cli:
            d = doc.to_dict()
            clientes_para_criar.append(ClienteComercial(
                modulo=mod,
                nome=d.get('nome', 'Sem Nome'),
                telefone=str(d.get('telefone', ''))[:50] if d.get('telefone') else '',
                email=d.get('email', '') if (d.get('email') and '@' in str(d.get('email'))) else None
            ))
        ClienteComercial.objects.bulk_create(clientes_para_criar, batch_size=500)
        print(f"   ✓ {len(clientes_para_criar)} clientes importados.")

        # 3. VENDAS
        print("3/6 - Importando Vendas (em lotes)...")
        docs_vendas = buscar_colecao_em_lotes(f'vendas_{mod}')
        vendas_para_criar = []
        for doc in docs_vendas:
            d = doc.to_dict()
            itens_novos = []
            for it in d.get('itens', []):
                item_id_antigo = it.get('id', '')
                item_id_novo = prod_map.get(item_id_antigo, str(item_id_antigo))
                itens_novos.append({
                    "id": item_id_novo,
                    "nome": it.get('nome', ''),
                    "precoVenda": float(it.get('precoVenda') or it.get('precoUnitario') or 0),
                    "precoUnitario": float(it.get('precoUnitario') or it.get('precoVenda') or 0),
                    "quantidade": int(it.get('quantidade') or 1),
                    "subtotal": float(it.get('subtotal') or 0)
                })
            
            dt_venda = parse_datetime(d.get('dataVenda'))
            dt_pend_orig = parse_datetime(d.get('dataPendenciaOriginal')) if d.get('dataPendenciaOriginal') else None

            vendas_para_criar.append(VendaComercial(
                modulo=mod,
                clienteId=d.get('clienteId') or d.get('clienteNome') or 'Venda Avulsa',
                itens=itens_novos,
                valorTotal=float(d.get('valorTotal') or 0),
                formaPagamento=d.get('formaPagamento', 'Dinheiro'),
                pagamentosMult=d.get('pagamentosMult', []),
                vendedor=d.get('vendedor', 'Sistema PDV'),
                dataVenda=dt_venda,
                dataPendenciaOriginal=dt_pend_orig
            ))
        VendaComercial.objects.bulk_create(vendas_para_criar, batch_size=500)
        print(f"   ✓ {len(vendas_para_criar)} vendas importadas.")

        # 4. PENDÊNCIAS
        print("4/6 - Importando Pendências...")
        docs_pend = buscar_colecao_em_lotes(f'pendencias_{mod}')
        pendencias_para_criar = []
        for doc in docs_pend:
            d = doc.to_dict()
            itens_novos = []
            for it in d.get('itens', []):
                item_id_antigo = it.get('id', '')
                item_id_novo = prod_map.get(item_id_antigo, str(item_id_antigo))
                itens_novos.append({
                    "id": item_id_novo,
                    "nome": it.get('nome', ''),
                    "precoVenda": float(it.get('precoVenda') or it.get('precoUnitario') or 0),
                    "quantidade": int(it.get('quantidade') or 1),
                    "subtotal": float(it.get('subtotal') or 0)
                })

            pendencias_para_criar.append(PendenciaComercial(
                modulo=mod,
                clienteId=d.get('clienteId', 'Cliente'),
                itens=itens_novos,
                valorTotal=float(d.get('valorTotal') or 0),
                formaPagamento=d.get('formaPagamento', 'Fiado/Pendente'),
                pagamentosMult=d.get('pagamentosMult', []),
                dataVenda=parse_datetime(d.get('dataVenda')),
                vendedor=d.get('vendedor', 'Sistema PDV'),
                estoqueBaixado=bool(d.get('estoqueBaixado', False))
            ))
        PendenciaComercial.objects.bulk_create(pendencias_para_criar, batch_size=500)
        print(f"   ✓ {len(pendencias_para_criar)} pendências importadas.")

        # 5. ENTRADAS DE ESTOQUE
        print("5/6 - Importando Entradas de Estoque...")
        docs_ent = buscar_colecao_em_lotes(f'entradas_estoque_{mod}')
        entradas_para_criar = []
        for doc in docs_ent:
            d = doc.to_dict()
            entradas_para_criar.append(EntradaEstoqueComercial(
                modulo=mod,
                produtoId=prod_map.get(d.get('produtoId', ''), str(d.get('produtoId', ''))),
                produtoNome=d.get('produtoNome', 'Sem Nome'),
                quantidadeAdicionada=int(d.get('quantidadeAdicionada') or 1),
                usuario=d.get('usuario', 'Sistema'),
                dataEntrada=parse_datetime(d.get('dataEntrada'))
            ))
        EntradaEstoqueComercial.objects.bulk_create(entradas_para_criar, batch_size=500)
        print(f"   ✓ {len(entradas_para_criar)} entradas de estoque importadas.")

        # 6. CONTAS A PAGAR
        print("6/6 - Importando Contas a Pagar...")
        docs_cp = buscar_colecao_em_lotes(f'contas_pagar_{mod}')
        contas_para_criar = []
        for doc in docs_cp:
            d = doc.to_dict()
            contas_para_criar.append(ContaPagarComercial(
                modulo=mod,
                descricao=d.get('descricao', 'Despesa'),
                fornecedor=d.get('fornecedor', ''),
                valor=float(d.get('valor') or 0),
                vencimento=parse_date(d.get('vencimento') or d.get('dataCadastro')),
                status=d.get('status', 'Pendente')
            ))
        ContaPagarComercial.objects.bulk_create(contas_para_criar, batch_size=500)
        print(f"   ✓ {len(contas_para_criar)} contas a pagar importadas.")

    print("\n🎉 MIGRAÇÃO COMERCIAL FINALIZADA COM SUCESSO!")

if __name__ == '__main__':
    migrar_comercial()