import os
import django
import firebase_admin
from firebase_admin import credentials, firestore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from usuarios.models import Usuario, ConfiguracaoSistema

cred = credentials.Certificate('firebase-key.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def migrar_usuarios_e_config():
    print("Migrando Usuários do Sistema...")
    docs_users = db.collection('usuarios_sistema').stream()
    count_users = 0
    
    for doc in docs_users:
        d = doc.to_dict()
        
        # Pega o email (ou o login, caso o email esteja vazio)
        login_str = str(d.get('login', '')).strip().lower()
        email_real = str(d.get('email', login_str)).strip().lower()
        
        email_usar = email_real if email_real else login_str
        
        if not email_usar:
            continue
        
        # Ignora as contas padrão de admin
        if email_usar == 'admin' or email_usar == 'adm' or 'admin@' in email_usar:
            continue

        # Usando 'email' em vez de 'username' e os nomes de coluna em snake_case
        user, created = Usuario.objects.get_or_create(email=email_usar, defaults={
            'nome': d.get('nome', 'Sem Nome'),
            'celular': d.get('telefone', ''),
            'modulos': d.get('modulos', []),
            'acessos': d.get('acessos', []),
            'admin_modulos': d.get('adminModulos', []),
            'lider_modulos': d.get('liderModulos', []),
            'perfis': d.get('perfis', []),
            'exige_troca_senha': d.get('exigeTrocaSenha', True)
        })

        if created:
            # Aplica a senha padrão criptografada
            user.set_password('123456')
            user.exige_troca_senha = True
            user.save()
            count_users += 1
        else:
            # Atualiza se já existir
            user.modulos = d.get('modulos', user.modulos)
            user.acessos = d.get('acessos', user.acessos)
            user.admin_modulos = d.get('adminModulos', user.admin_modulos)
            user.lider_modulos = d.get('liderModulos', user.lider_modulos)
            user.perfis = d.get('perfis', user.perfis)
            user.save()

    print(f"✅ {count_users} novos usuários importados. (Senha provisória: 123456)")

    print("Migrando Mensagem Padrão de Aniversário...")
    try:
        doc_niver = db.collection('configuracoes_gerais').document('push_aniversario').get()
        if doc_niver.exists:
            ConfiguracaoSistema.objects.update_or_create(
                chave='push_aniversario',
                defaults={'valor': doc_niver.to_dict()}
            )
            print("✅ Mensagem de Aniversário migrada com sucesso!")
        else:
            print("⚠️ Mensagem de aniversário não estava configurada no Firebase.")
    except Exception as e:
        print(f"Erro ao migrar mensagem de aniversário: {e}")

migrar_usuarios_e_config()