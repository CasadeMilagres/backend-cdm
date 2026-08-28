from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CadastroGeral, FormularioAvulso
from .models import GcLancamentoSemanal, ConfiguracaoSistema, GrupoConexao
from .models import IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush

class CadastroGeralSerializer(serializers.ModelSerializer):
    class Meta:
        model = CadastroGeral
        fields = '__all__'

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'perfis', 'modulos', 'admin_modulos', 'lider_modulos']

class GrupoConexaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoConexao
        fields = '__all__'

class GcLancamentoSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GcLancamentoSemanal
        fields = '__all__'

class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'

class FormularioAvulsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioAvulso
        fields = '__all__'

class IdeModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeModulo
        fields = '__all__'

class IdeFormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeFormulario
        fields = '__all__'

class IdeTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeTurma
        fields = '__all__'

class IdeInscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeInscricao
        fields = '__all__'

class IdeSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeSala
        fields = '__all__'

class FilaNotificacaoPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilaNotificacaoPush
        fields = '__all__'