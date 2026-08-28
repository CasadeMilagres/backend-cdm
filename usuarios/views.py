from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
# Aqui importamos todos os modelos que criamos no models.py
from .models import CadastroGeral, GrupoConexao
# E aqui os serializadores
from .serializers import CadastroGeralSerializer, UsuarioSerializer, GrupoConexaoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CadastroGeral, GrupoConexao, FormularioAvulso
from .serializers import CadastroGeralSerializer, UsuarioSerializer, GrupoConexaoSerializer, FormularioAvulsoSerializer
from .models import IdeModulo, IdeFormulario, IdeTurma, IdeInscricao, IdeSala, FilaNotificacaoPush
from .serializers import (
    IdeModuloSerializer, IdeFormularioSerializer, IdeTurmaSerializer,
    IdeInscricaoSerializer, IdeSalaSerializer, FilaNotificacaoPushSerializer
)

Usuario = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    """
    Retorna os dados do usuário logado para o contexto do React.
    """
    user = request.user
    dados = {
        "id": user.id,
        "login": user.email,
        "nome": user.nome,
        "celular": user.celular,
        "perfis": user.perfis,
        "acessos": user.acessos,
        "modulos": user.modulos,
        "adminModulos": user.admin_modulos,
        "liderModulos": user.lider_modulos,
        "exigeTrocaSenha": user.exige_troca_senha,
        "isGlobalAdmin": user.is_superuser 
    }
    return Response(dados)


class CadastroGeralViewSet(viewsets.ModelViewSet):
    queryset = CadastroGeral.objects.all().order_by('-dataCadastro')
    serializer_class = CadastroGeralSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome', 'celular', 'email', 'bairro', 'lider']
    permission_classes = [AllowAny] 

class FormularioAvulsoViewSet(viewsets.ModelViewSet):
    queryset = FormularioAvulso.objects.all().order_by('-dataCriacao')
    serializer_class = FormularioAvulsoSerializer
    permission_classes = [AllowAny]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('nome')
    serializer_class = UsuarioSerializer


class GrupoConexaoViewSet(viewsets.ModelViewSet):
    queryset = GrupoConexao.objects.all().order_by('lider')
    serializer_class = GrupoConexaoSerializer

class IdeModuloViewSet(viewsets.ModelViewSet):
    queryset = IdeModulo.objects.all().order_by('nome')
    serializer_class = IdeModuloSerializer
    permission_classes = [AllowAny]

class IdeFormularioViewSet(viewsets.ModelViewSet):
    queryset = IdeFormulario.objects.all().order_by('-dataCriacao')
    serializer_class = IdeFormularioSerializer
    permission_classes = [AllowAny]

class IdeTurmaViewSet(viewsets.ModelViewSet):
    queryset = IdeTurma.objects.all().order_by('nome')
    serializer_class = IdeTurmaSerializer
    permission_classes = [AllowAny]

class IdeInscricaoViewSet(viewsets.ModelViewSet):
    queryset = IdeInscricao.objects.all().order_by('-dataInscricao')
    serializer_class = IdeInscricaoSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['alunoNome', 'moduloNome', 'celular']

class IdeSalaViewSet(viewsets.ModelViewSet):
    queryset = IdeSala.objects.all().order_by('-data')
    serializer_class = IdeSalaSerializer
    permission_classes = [AllowAny]

class FilaNotificacaoPushViewSet(viewsets.ModelViewSet):
    queryset = FilaNotificacaoPush.objects.all().order_by('-dataDisparo')
    serializer_class = FilaNotificacaoPushSerializer
    permission_classes = [AllowAny]