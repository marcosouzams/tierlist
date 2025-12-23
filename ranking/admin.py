from django.contrib import admin
from .models import Candidato, ProcessoSeletivo, Criterio, RankingCandidato, AvaliacaoCriterio


class CriterioInline(admin.TabularInline):
    """Inline para critérios dentro do ProcessoSeletivo"""
    model = Criterio
    extra = 1
    fields = ['nome', 'descricao', 'peso', 'ordem']


class AvaliacaoCriterioInline(admin.TabularInline):
    """Inline para avaliações de critérios dentro do RankingCandidato"""
    model = AvaliacaoCriterio
    extra = 0
    fields = ['criterio', 'nota', 'anotacao']
    readonly_fields = ['criterio']
    
    def get_queryset(self, request):
        """Filtra critérios do processo seletivo correto"""
        qs = super().get_queryset(request)
        return qs.select_related('criterio', 'ranking')


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['nome', 'email', 'telefone']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Redes e Documentos', {
            'fields': ('linkedin', 'curriculo')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProcessoSeletivo)
class ProcessoSeletivoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'vaga', 'departamento', 'status', 'data_inicio', 'data_fim']
    list_filter = ['status', 'departamento', 'data_inicio']
    search_fields = ['titulo', 'vaga', 'departamento', 'descricao']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [CriterioInline]
    
    fieldsets = (
        ('Informações do Processo', {
            'fields': ('titulo', 'vaga', 'departamento', 'descricao')
        }),
        ('Status e Datas', {
            'fields': ('status', 'data_inicio', 'data_fim')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Criterio)
class CriterioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'processo_seletivo', 'peso', 'ordem']
    list_filter = ['processo_seletivo']
    search_fields = ['nome', 'descricao', 'processo_seletivo__titulo']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações do Critério', {
            'fields': ('processo_seletivo', 'nome', 'descricao')
        }),
        ('Configurações', {
            'fields': ('peso', 'ordem')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RankingCandidato)
class RankingCandidatoAdmin(admin.ModelAdmin):
    list_display = ['candidato', 'processo_seletivo', 'tier', 'get_media_criterios', 'data_avaliacao']
    list_filter = ['tier', 'processo_seletivo', 'data_avaliacao']
    search_fields = ['candidato__nome', 'processo_seletivo__titulo', 'observacoes_gerais']
    readonly_fields = ['criado_em', 'atualizado_em', 'get_media_criterios']
    inlines = [AvaliacaoCriterioInline]
    
    fieldsets = (
        ('Candidato e Processo', {
            'fields': ('candidato', 'processo_seletivo')
        }),
        ('Avaliação', {
            'fields': ('tier', 'data_avaliacao', 'get_media_criterios')
        }),
        ('Observações', {
            'fields': ('observacoes_gerais',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_media_criterios(self, obj):
        """Exibe a média dos critérios"""
        media = obj.calcular_media_criterios()
        return f"{media:.2f}" if media is not None else "Sem avaliações"
    get_media_criterios.short_description = 'Média dos Critérios'


@admin.register(AvaliacaoCriterio)
class AvaliacaoCriterioAdmin(admin.ModelAdmin):
    list_display = ['get_candidato', 'criterio', 'nota', 'get_processo']
    list_filter = ['criterio__processo_seletivo', 'criterio', 'nota']
    search_fields = ['ranking__candidato__nome', 'criterio__nome', 'anotacao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Avaliação', {
            'fields': ('ranking', 'criterio', 'nota')
        }),
        ('Anotações', {
            'fields': ('anotacao',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_candidato(self, obj):
        """Retorna o nome do candidato"""
        return obj.ranking.candidato.nome
    get_candidato.short_description = 'Candidato'
    get_candidato.admin_order_field = 'ranking__candidato__nome'
    
    def get_processo(self, obj):
        """Retorna o título do processo seletivo"""
        return obj.ranking.processo_seletivo.titulo
    get_processo.short_description = 'Processo Seletivo'
    get_processo.admin_order_field = 'ranking__processo_seletivo__titulo'
