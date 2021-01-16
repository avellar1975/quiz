from django.shortcuts import render, redirect
from quizz.quiz.models import Pergunta, Aluno, Resposta
from quizz.quiz.forms import AlunoForm
from django.utils.timezone import now
from django.db.models import Sum


def indice(requisicao):
    if requisicao.method == 'POST':
        # Verificar se já existe um usuário com o EMAIL
        email = requisicao.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            # Cadastrar o aluno novo
            form = AlunoForm(requisicao.POST)
            if form.is_valid():
                aluno = form.save()
                requisicao.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            contexto = {'form': form}
            return render(requisicao, 'quiz/indice.html', contexto)
        else:
            requisicao.session['aluno_id'] = aluno.id
            aluno_id = requisicao.session['aluno_id']
            # Verificar se já respondeu alguma pergunta
            if Resposta.objects.filter(aluno_id=aluno_id):
                return redirect('/classificacao')
            return redirect('/perguntas/1')
    else:
        # se não for validado
        return render(requisicao, 'quiz/indice.html')


def perguntas(requisicao, id_pergunta):
    aluno_id = requisicao.session['aluno_id']
    try:
        pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[id_pergunta - 1]
    except IndexError:
        return redirect(f'/classificacao')
    else:
        contexto = {'id_pergunta': id_pergunta, 'pergunta': pergunta}
        if requisicao.method == 'POST':
            alternativa_escolhida = int(requisicao.POST['alternativa'])

            if alternativa_escolhida == pergunta.alternativa_correta:
                try:
                    primeira = Resposta.objects.filter(pergunta=pergunta).order_by('criacao')[0]
                except IndexError:
                    pontos = 100
                else:
                    tempo_primeira = primeira.criacao
                    diferenca = now() - tempo_primeira
                    pontos = 100 - int(diferenca.total_seconds())
                    pontos = max(pontos, 1)

                Resposta(aluno_id=aluno_id, pergunta=pergunta, pontos=pontos).save()
                return redirect(f'/perguntas/{id_pergunta + 1}')
            else:
                contexto['alternativa_escolhida'] = alternativa_escolhida

        return render(requisicao, 'quiz/perguntas.html', contexto)


def classificacao(requisicao):
    aluno_id = requisicao.session['aluno_id']
    dct = Resposta.objects.filter(aluno_id=aluno_id).aggregate(Sum('pontos'))
    pontos_do_aluno = dct['pontos__sum']
    alunos_pontos_maior = Resposta.objects.values('aluno').annotate(Sum('pontos')).filter(
        pontos__sum__gt=pontos_do_aluno).count()
    primeiros_5 = Resposta.objects.values('aluno', 'aluno__nome').annotate(
        Sum('pontos')).order_by('-pontos__sum')[:5]
    contexto = {'pontos': pontos_do_aluno, 'posicao': alunos_pontos_maior + 1,
                'ranking': primeiros_5}
    return render(requisicao, 'quiz/classificacao.html', contexto)
