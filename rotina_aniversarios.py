import os
import django
import re
from datetime import datetime, date

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

# Nomes corrigidos: CadastroGeral e FilaNotificacaoPush
from usuarios.models import ConfiguracaoSistema, CadastroGeral, FilaNotificacaoPush

def disparar_aniversariantes_do_dia():
    print("🎂 Iniciando varredura de aniversariantes do dia...")
    
    hoje = datetime.now()
    dia_hoje = hoje.day
    mes_hoje = hoje.month

    # 1. Puxa a mensagem padrão configurada no banco
    mensagem_template = "Feliz aniversário! Que Deus abençoe poderosamente a sua vida e renove suas forças neste novo ciclo."
    try:
        config = ConfiguracaoSistema.objects.get(chave='push_aniversario')
        if config.valor and 'texto' in config.valor:
            mensagem_template = config.valor['texto']
    except ConfiguracaoSistema.DoesNotExist:
        pass

    # 2. Puxa todos os cadastros ativos
    cadastros = CadastroGeral.objects.all()
    aniversariantes_encontrados = 0

    # 3. Filtra quem faz aniversário hoje (Lê tanto objetos de Data quanto Strings)
    for c in cadastros:
        data_bruta = getattr(c, 'dataNascimento', None) or getattr(c, 'nascimento', None) or getattr(c, 'dataNasc', None)
        
        if not data_bruta:
            continue

        dia_cad = None
        mes_cad = None

        # Se for um formato de data/hora oficial do Python
        if isinstance(data_bruta, (date, datetime)):
            dia_cad = data_bruta.day
            mes_cad = data_bruta.month
        
        # Se ainda for uma String solta vinda de migração
        elif isinstance(data_bruta, str):
            data_sem_tempo = data_bruta.split('T')[0].split(' ')[0]
            numeros = re.findall(r'\d+', data_sem_tempo)
            
            if numeros and len(numeros) >= 2:
                if len(numeros[0]) == 4:
                    mes_cad = int(numeros[1])
                    dia_cad = int(numeros[2])
                else:
                    dia_cad = int(numeros[0])
                    mes_cad = int(numeros[1])

        # Se bateu o dia e o mês, é aniversariante!
        if dia_cad == dia_hoje and mes_cad == mes_hoje:
            aniversariantes_encontrados += 1
            nome_aluno = c.nome or 'Amigo(a)'
            primeiro_nome = nome_aluno.split(' ')[0]

            titulo = f"Feliz Aniversário, {primeiro_nome}! 🎂"
            
            # Substitui a variável {nome} caso exista na mensagem personalizada
            mensagem_final = mensagem_template.replace('{nome}', primeiro_nome)

            # 4. Checa se já enviou hoje
            ja_enviado = FilaNotificacaoPush.objects.filter(
                tipo='aniversario',
                usuarioAlvoId=str(c.id),
                dataCriacao__date=hoje.date()
            ).exists()

            if not ja_enviado:
                FilaNotificacaoPush.objects.create(
                    tipo='aniversario',
                    usuarioAlvoId=str(c.id),
                    titulo=titulo,
                    mensagem=mensagem_final,
                    status='pendente'
                )
                print(f"   ✓ Push gerado para: {nome_aluno} ({dia_cad:02d}/{mes_cad:02d})")

    print(f"\n🎉 Varredura concluída! {aniversariantes_encontrados} aniversariantes encontrados hoje.")

if __name__ == '__main__':
    disparar_aniversariantes_do_dia()