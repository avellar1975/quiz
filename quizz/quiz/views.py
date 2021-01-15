from django.shortcuts import render, redirect
from quizz.quiz.models import Pergunta, Aluno
from quizz.quiz.forms import AlunoForm


def indice(requisicao):
    if requisicao.method == 'POST':
        # verificar se já existe um usuário com o EMAIL
        email = requisicao.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            # VALIDAR O FORMULARIO E SALVAR NO DB
            form = AlunoForm(requisicao.POST)
            if form.is_valid():
                aluno = form.save()
                requisicao.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            contexto = {'form': form}
            return render(requisicao, 'quiz/indice.html', contexto)
        else:
            requisicao.session['aluno_id'] = aluno.id
            return redirect('/perguntas/1')
    else:
        # se não for validado
        return render(requisicao, 'quiz/indice.html')

def perguntas(requisicao, id_pergunta):
    aluno_id = requisicao.session['aluno_id']
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[id_pergunta - 1]
    contexto = {'id_pergunta': id_pergunta, 'pergunta': pergunta}
    return render(requisicao, 'quiz/perguntas.html', contexto)


def classificacao(requisicao):
    return render(requisicao, 'quiz/classificacao.html')
