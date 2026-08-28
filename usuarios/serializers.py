from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CadastroGeral, GrupoConexao, FormularioAvulso

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

class FormularioAvulsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormularioAvulso
        fields = '__all__'