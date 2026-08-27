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


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('nome')
    serializer_class = UsuarioSerializer


class GrupoConexaoViewSet(viewsets.ModelViewSet):
    queryset = GrupoConexao.objects.all().order_by('lider')
    serializer_class = GrupoConexaoSerializer