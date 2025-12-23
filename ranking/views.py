from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from .models import ProcessoSeletivo, Candidato, RankingCandidato, Criterio, AvaliacaoCriterio


def dashboard(request):
    """View para o dashboard principal"""
    
    # Estatísticas
    processos_ativos_count = ProcessoSeletivo.objects.filter(
        status__in=['aberto', 'em_andamento']
    ).count()
    
    candidatos_count = Candidato.objects.count()
    
    # Rankings sem tier atribuído (avaliações pendentes)
    avaliacoes_pendentes = RankingCandidato.objects.filter(
        tier__isnull=True
    ).count()
    
    # Rankings com tier atribuído (completos)
    rankings_completos = RankingCandidato.objects.filter(
        tier__isnull=False
    ).count()
    
    # Processos recentes (últimos 5)
    processos_recentes = ProcessoSeletivo.objects.all()[:5]
    
    context = {
        'processos_ativos_count': processos_ativos_count,
        'candidatos_count': candidatos_count,
        'avaliacoes_pendentes': avaliacoes_pendentes,
        'rankings_completos': rankings_completos,
        'processos_recentes': processos_recentes,
    }
    
    return render(request, 'ranking/dashboard.html', context)


def processos_list(request):
    """View para listar processos seletivos"""
    
    # Filtro de status (se fornecido)
    status_filter = request.GET.get('status')
    
    processos = ProcessoSeletivo.objects.all()
    
    if status_filter:
        processos = processos.filter(status=status_filter)
    
    # Ordenar por data de criação (mais recentes primeiro)
    processos = processos.order_by('-criado_em')
    
    context = {
        'processos': processos,
        'status_filter': status_filter,
    }
    
    return render(request, 'ranking/processos_list.html', context)


def processos_create(request):
    """View para criar novo processo seletivo"""
    
    if request.method == 'POST':
        try:
            # Criar processo seletivo
            processo = ProcessoSeletivo.objects.create(
                titulo=request.POST.get('titulo'),
                vaga=request.POST.get('vaga'),
                departamento=request.POST.get('departamento') or None,
                descricao=request.POST.get('descricao'),
                status=request.POST.get('status', 'aberto'),
                data_inicio=request.POST.get('data_inicio'),
                data_fim=request.POST.get('data_fim') or None,
            )
            
            messages.success(request, f'Processo "{processo.titulo}" criado com sucesso!')
            return redirect('processos_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar processo: {str(e)}')
            return redirect('processos_list')
    
    return redirect('processos_list')


def processo_ranking(request, processo_id):
    """View para exibir o ranking de candidatos de um processo"""
    
    processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
    
    # Buscar todos os rankings do processo
    rankings = RankingCandidato.objects.filter(
        processo_seletivo=processo
    ).select_related('candidato').prefetch_related('avaliacoes_criterios__criterio')
    
    # Buscar critérios do processo
    criterios = Criterio.objects.filter(processo_seletivo=processo).order_by('ordem', 'nome')
    
    # Organizar rankings por tier e adicionar avaliações
    rankings_por_tier = {
        'S': [],
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'F': [],
        'unranked': []
    }
    
    for ranking in rankings:
        # Adicionar avaliações ao ranking
        avaliacoes = {}
        for avaliacao in ranking.avaliacoes_criterios.all():
            avaliacoes[avaliacao.criterio.id] = avaliacao.nota
        
        ranking.avaliacoes_dict = avaliacoes
        
        if ranking.tier:
            rankings_por_tier[ranking.tier].append(ranking)
        else:
            rankings_por_tier['unranked'].append(ranking)
    
    context = {
        'processo': processo,
        'rankings_por_tier': rankings_por_tier,
        'tem_candidatos': rankings.exists(),
        'criterios': criterios,
    }
    
    return render(request, 'ranking/processo_ranking.html', context)


def candidato_create_form(request, processo_id):
    """View HTMX para retornar o formulário de criar candidato"""
    
    processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
    
    context = {
        'processo': processo,
    }
    
    return render(request, 'ranking/partials/candidato_form_modal.html', context)


def candidato_create(request, processo_id):
    """View HTMX para criar candidato"""
    
    if request.method == 'POST':
        processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
        
        try:
            # Criar candidato
            candidato = Candidato.objects.create(
                nome=request.POST.get('nome'),
                email=request.POST.get('email'),
                telefone=request.POST.get('telefone', ''),
                linkedin=request.POST.get('linkedin', ''),
            )
            
            # Criar ranking para este candidato no processo
            RankingCandidato.objects.create(
                candidato=candidato,
                processo_seletivo=processo,
            )
            
            # Retornar resposta vazia e fechar modal
            return render(request, 'ranking/partials/close_modal.html')
            
        except Exception as e:
            context = {
                'processo': processo,
                'error': str(e),
            }
            return render(request, 'ranking/partials/candidato_form_modal.html', context)
    
    return redirect('processo_ranking', processo_id=processo_id)


def update_ranking_tier(request, ranking_id):
    """View para atualizar tier e ordem do ranking"""
    
    if request.method == 'POST':
        ranking = get_object_or_404(RankingCandidato, id=ranking_id)
        
        tier = request.POST.get('tier')
        ordem = request.POST.get('ordem', 0)
        
        # Atualizar tier e ordem
        if tier == 'unranked' or tier == '' or tier is None:
            ranking.tier = None
        else:
            ranking.tier = tier
            
        try:
            ranking.ordem = int(ordem)
        except (ValueError, TypeError):
            ranking.ordem = 0
            
        ranking.save()
        
        from django.http import JsonResponse
        return JsonResponse({
            'success': True,
            'ranking_id': ranking.id,
            'tier': ranking.tier,
            'ordem': ranking.ordem
        })
    
    from django.http import JsonResponse
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=400)


def criterios_list_modal(request, processo_id):
    """View para exibir modal de listagem de critérios"""
    
    processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
    criterios = Criterio.objects.filter(processo_seletivo=processo).order_by('ordem', 'nome')
    
    context = {
        'processo': processo,
        'criterios': criterios,
    }
    
    return render(request, 'ranking/partials/criterios_modal.html', context)


def criterio_create_form(request, processo_id):
    """View para exibir formulário de criação de critério"""
    
    processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
    
    context = {
        'processo': processo,
    }
    
    return render(request, 'ranking/partials/criterio_form.html', context)


def criterio_create(request, processo_id):
    """View para criar critério"""
    
    if request.method == 'POST':
        processo = get_object_or_404(ProcessoSeletivo, id=processo_id)
        
        try:
            # Obter dados do formulário
            nome = request.POST.get('nome', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            peso = request.POST.get('peso', '1.00')
            ordem = request.POST.get('ordem', '0')
            
            # Validação básica
            if not nome:
                raise ValueError("Nome do critério é obrigatório")
            
            # Converter peso e ordem
            try:
                peso = float(peso)
            except (ValueError, TypeError):
                peso = 1.00
                
            try:
                ordem = int(ordem)
            except (ValueError, TypeError):
                ordem = 0
            
            # Criar critério
            criterio = Criterio.objects.create(
                processo_seletivo=processo,
                nome=nome,
                descricao=descricao if descricao else None,
                peso=peso,
                ordem=ordem,
            )
            
            # Retornar modal atualizado
            return criterios_list_modal(request, processo_id)
            
        except Exception as e:
            context = {
                'processo': processo,
                'error': str(e),
            }
            return render(request, 'ranking/partials/criterio_form.html', context)
    
    return redirect('processo_ranking', processo_id=processo_id)


def criterio_edit_form(request, criterio_id):
    """View para exibir formulário de edição de critério"""
    
    criterio = get_object_or_404(Criterio, id=criterio_id)
    
    context = {
        'processo': criterio.processo_seletivo,
        'criterio': criterio,
    }
    
    return render(request, 'ranking/partials/criterio_form.html', context)


def criterio_update(request, criterio_id):
    """View para atualizar critério"""
    
    if request.method == 'POST':
        criterio = get_object_or_404(Criterio, id=criterio_id)
        processo = criterio.processo_seletivo
        
        try:
            # Obter dados do formulário
            nome = request.POST.get('nome', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            peso = request.POST.get('peso', '1.00')
            ordem = request.POST.get('ordem', '0')
            
            # Validação básica
            if not nome:
                raise ValueError("Nome do critério é obrigatório")
            
            # Converter peso e ordem
            try:
                peso = float(peso)
            except (ValueError, TypeError):
                peso = 1.00
                
            try:
                ordem = int(ordem)
            except (ValueError, TypeError):
                ordem = 0
            
            # Atualizar critério
            criterio.nome = nome
            criterio.descricao = descricao if descricao else None
            criterio.peso = peso
            criterio.ordem = ordem
            criterio.save()
            
            # Retornar modal atualizado
            return criterios_list_modal(request, processo.id)
            
        except Exception as e:
            context = {
                'processo': processo,
                'criterio': criterio,
                'error': str(e),
            }
            return render(request, 'ranking/partials/criterio_form.html', context)
    
    return redirect('processo_ranking', processo_id=criterio.processo_seletivo.id)


def criterio_delete(request, criterio_id):
    """View para deletar critério"""
    
    if request.method == 'DELETE':
        criterio = get_object_or_404(Criterio, id=criterio_id)
        criterio.delete()
        
        from django.http import HttpResponse
        return HttpResponse('', status=200)
    
    from django.http import HttpResponse
    return HttpResponse('Method not allowed', status=405)


def avaliar_candidato_modal(request, ranking_id):
    """View para exibir modal de avaliação de candidato"""
    
    ranking = get_object_or_404(RankingCandidato, id=ranking_id)
    processo = ranking.processo_seletivo
    
    # Buscar critérios do processo
    criterios = Criterio.objects.filter(processo_seletivo=processo).order_by('ordem', 'nome')
    
    # Para cada critério, buscar se já existe avaliação
    criterios_com_avaliacao = []
    for criterio in criterios:
        try:
            avaliacao = AvaliacaoCriterio.objects.get(ranking=ranking, criterio=criterio)
        except AvaliacaoCriterio.DoesNotExist:
            avaliacao = None
        
        criterios_com_avaliacao.append({
            'id': criterio.id,
            'nome': criterio.nome,
            'descricao': criterio.descricao,
            'peso': criterio.peso,
            'ordem': criterio.ordem,
            'avaliacao': avaliacao
        })
    
    # Calcular média ponderada
    media_ponderada = ranking.calcular_media_criterios()
    
    context = {
        'ranking': ranking,
        'criterios': criterios_com_avaliacao,
        'media_ponderada': media_ponderada,
    }
    
    return render(request, 'ranking/partials/avaliar_candidato_modal.html', context)


def salvar_avaliacao(request, ranking_id, criterio_id):
    """View para salvar avaliação de um critério"""
    
    if request.method == 'POST':
        ranking = get_object_or_404(RankingCandidato, id=ranking_id)
        criterio = get_object_or_404(Criterio, id=criterio_id)
        
        try:
            nota = request.POST.get('nota', '0')
            anotacao = request.POST.get('anotacao', '').strip()
            
            # Converter nota
            try:
                nota = float(nota)
            except (ValueError, TypeError):
                nota = 0.0
            
            # Validar nota
            if nota < 0 or nota > 10:
                raise ValueError("Nota deve estar entre 0 e 10")
            
            # Criar ou atualizar avaliação
            avaliacao, created = AvaliacaoCriterio.objects.update_or_create(
                ranking=ranking,
                criterio=criterio,
                defaults={
                    'nota': nota,
                    'anotacao': anotacao if anotacao else None,
                }
            )
            
            # Retornar modal atualizado
            return avaliar_candidato_modal(request, ranking_id)
            
        except Exception as e:
            # Em caso de erro, retornar modal com mensagem de erro
            return avaliar_candidato_modal(request, ranking_id)
    
    return redirect('processo_ranking', processo_id=ranking.processo_seletivo.id)


def salvar_observacoes(request, ranking_id):
    """View para salvar observações gerais do candidato"""
    
    if request.method == 'POST':
        ranking = get_object_or_404(RankingCandidato, id=ranking_id)
        
        try:
            observacoes_gerais = request.POST.get('observacoes_gerais', '').strip()
            
            ranking.observacoes_gerais = observacoes_gerais if observacoes_gerais else None
            ranking.save()
            
            # Retornar modal atualizado
            return avaliar_candidato_modal(request, ranking_id)
            
        except Exception as e:
            return avaliar_candidato_modal(request, ranking_id)
    
    return redirect('processo_ranking', processo_id=ranking.processo_seletivo.id)

