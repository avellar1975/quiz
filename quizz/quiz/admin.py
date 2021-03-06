from django.contrib import admin
from quizz.quiz.models import Pergunta, Aluno, Resposta

# Register your models here.


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ['id', 'enunciado', 'disponivel']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'nome', 'criacao']


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ['id', 'aluno', 'pergunta', 'pontos', 'criacao']
