from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CadastroGeral, FormularioAvulso
from .models import GcLancamentoSemanal, ConfiguracaoSistema, GrupoConexao
from .models import IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush
from .models import Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio
from .models import JornadaCadastro, ConfiguracaoSistema
from .models import (
    ProdutoComercial, ClienteComercial, VendaComercial,
    PendenciaComercial, EntradaEstoqueComercial, ContaPagarComercial
)

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

class MinisterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministerio
        fields = '__all__'

class VoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntario
        fields = '__all__'

class EventoMinisterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoMinisterio
        fields = '__all__'

class EscalaMinisterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalaMinisterio
        fields = '__all__'

class ProdutoComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoComercial
        fields = '__all__'

class ClienteComercialSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    telefone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    class Meta:
        model = ClienteComercial
        fields = '__all__'

class VendaComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaComercial
        fields = '__all__'

class PendenciaComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendenciaComercial
        fields = '__all__'

class EntradaEstoqueComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaEstoqueComercial
        fields = '__all__'

class ContaPagarComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaPagarComercial
        fields = '__all__'

class JornadaCadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = JornadaCadastro
        fields = '__all__'

class ConfiguracaoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoSistema
        fields = '__all__'