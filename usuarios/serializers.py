from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CadastroGeral, FormularioAvulso
from .models import GcLancamentoSemanal, ConfiguracaoSistema, GrupoConexao
from .models import IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush
from .models import Ministerio, Voluntario, EventoMinisterio, EscalaMinisterio
from .models import JornadaCadastro, ConfiguracaoSistema
from .models import MidiaBanner, MidiaPregacao
from .models import IdeModuloAula, MinisterioLider, MinisterioFuncao
from .models import IdeModuloPergunta, IdeFormularioPergunta
from .models import IdeTurmaAluno
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

class FormularioAvulsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioAvulso
        fields = '__all__'

class IdeModuloSerializer(serializers.ModelSerializer):
    gradeCurricular = serializers.SerializerMethodField()
    perguntas = serializers.SerializerMethodField()

    class Meta:
        model = IdeModulo
        fields = '__all__'

    def get_gradeCurricular(self, obj):
        return [{"tema": a.tema} for a in obj.aulas.all()]

    def get_perguntas(self, obj):
        return [p.texto for p in obj.perguntas_rel.all()]

    def create(self, validated_data):
        request = self.context.get('request')
        grade_data = request.data.get('gradeCurricular', []) if request else []
        modulo = super().create(validated_data)
        for aula in grade_data:
            IdeModuloAula.objects.create(
                modulo=modulo, tema=aula.get('tema', 'Nova Aula'), exercicioPerguntas=aula.get('exercicioPerguntas', [])
            )
        return modulo

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and 'gradeCurricular' in request.data:
            grade_data = request.data.get('gradeCurricular', [])
            instance.aulas.all().delete()
            for aula in grade_data:
                IdeModuloAula.objects.create(
                    modulo=instance, tema=aula.get('tema', 'Nova Aula'), exercicioPerguntas=aula.get('exercicioPerguntas', [])
                )
        return super().update(instance, validated_data)

class IdeFormularioSerializer(serializers.ModelSerializer):
    perguntas = serializers.SerializerMethodField()

    class Meta:
        model = IdeFormulario
        fields = '__all__'

    def get_perguntas(self, obj):
        return [p.texto for p in obj.perguntas_rel.all()]

class IdeInscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeInscricao
        fields = '__all__'

class FilaNotificacaoPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilaNotificacaoPush
        fields = '__all__'

class MinisterioSerializer(serializers.ModelSerializer):
    lideres = serializers.SerializerMethodField()
    funcoes = serializers.SerializerMethodField()

    class Meta:
        model = Ministerio
        fields = '__all__'

    def get_lideres(self, obj):
        return [l.nome for l in obj.lideres_rel.all()]

    def get_funcoes(self, obj):
        return [{"id": str(f.id), "nome": f.nome, "voluntarios": f.voluntarios} for f in obj.funcoes_rel.all()]

    def create(self, validated_data):
        request = self.context.get('request')
        minis = super().create(validated_data)
        if request:
            for l in request.data.get('lideres', []):
                MinisterioLider.objects.create(ministerio=minis, nome=l)
            for f in request.data.get('funcoes', []):
                MinisterioFuncao.objects.create(ministerio=minis, nome=f.get('nome', 'Função'), voluntarios=f.get('voluntarios', []))
        return minis

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request:
            if 'lideres' in request.data:
                instance.lideres_rel.all().delete()
                for l in request.data.get('lideres', []):
                    MinisterioLider.objects.create(ministerio=instance, nome=l)
            if 'funcoes' in request.data:
                instance.funcoes_rel.all().delete()
                for f in request.data.get('funcoes', []):
                    MinisterioFuncao.objects.create(ministerio=instance, nome=f.get('nome', 'Função'), voluntarios=f.get('voluntarios', []))
        return super().update(instance, validated_data)

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

class MidiaBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiaBanner
        fields = '__all__'

class MidiaPregacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiaPregacao
        fields = '__all__'

class IdeTurmaSerializer(serializers.ModelSerializer):
    alunos = serializers.SerializerMethodField()

    class Meta:
        model = IdeTurma
        fields = '__all__'

    def get_alunos(self, obj):
        return [{"inscricaoId": a.inscricaoId, "alunoId": a.inscricaoId, "alunoNome": a.alunoNome, "celular": a.celular} for a in obj.alunos_rel.all()]

    def create(self, validated_data):
        request = self.context.get('request')
        turma = super().create(validated_data)
        if request and 'alunos' in request.data:
            for a in request.data['alunos']:
                IdeTurmaAluno.objects.create(turma=turma, inscricaoId=a.get('inscricaoId'), alunoNome=a.get('alunoNome'), celular=a.get('celular'))
        return turma

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and 'alunos' in request.data:
            instance.alunos_rel.all().delete()
            for a in request.data['alunos']:
                IdeTurmaAluno.objects.create(turma=instance, inscricaoId=a.get('inscricaoId'), alunoNome=a.get('alunoNome'), celular=a.get('celular'))
        return super().update(instance, validated_data)

class IdeSalaSerializer(serializers.ModelSerializer):
    turmaId = serializers.SerializerMethodField()
    turmaNome = serializers.SerializerMethodField()

    class Meta:
        model = IdeSala
        fields = '__all__'

    def get_turmaId(self, obj):
        return str(obj.turma.id) if obj.turma else None

    def get_turmaNome(self, obj):
        return obj.turma.nome if obj.turma else None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and 'turmaId' in request.data:
            from .models import IdeTurma
            turma = IdeTurma.objects.filter(id=request.data['turmaId']).first()
            validated_data['turma'] = turma
        return super().create(validated_data)