from django.forms import ModelForm
from quizz.quiz.models import Aluno


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'email']
