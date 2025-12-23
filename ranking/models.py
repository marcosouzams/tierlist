from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone


class Candidato(models.Model):
    """Model para armazenar informações dos candidatos"""
    
    nome = models.CharField(
        max_length=200,
        verbose_name='Nome Completo',
        help_text='Nome completo do candidato'
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name='E-mail',
        help_text='E-mail do candidato'
    )
    telefone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefone deve estar no formato: '+999999999'. Até 15 dígitos permitidos."
    )
    telefone = models.CharField(
        validators=[telefone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Telefone',
        help_text='Telefone de contato'
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        verbose_name='LinkedIn',
        help_text='URL do perfil no LinkedIn'
    )
    curriculo = models.FileField(
        upload_to='curriculos/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Currículo',
        help_text='Arquivo do currículo (PDF, DOC, DOCX)'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Observações gerais sobre o candidato'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ProcessoSeletivo(models.Model):
    """Model para os processos seletivos"""
    
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título do processo seletivo'
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição detalhada do processo seletivo'
    )
    vaga = models.CharField(
        max_length=200,
        verbose_name='Vaga',
        help_text='Nome da vaga'
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Departamento',
        help_text='Departamento da vaga'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name='Status'
    )
    data_inicio = models.DateField(
        verbose_name='Data de Início',
        help_text='Data de início do processo seletivo'
    )
    data_fim = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data de Fim',
        help_text='Data prevista para encerramento'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Processo Seletivo'
        verbose_name_plural = 'Processos Seletivos'
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.titulo} - {self.vaga}"

    @property
    def esta_ativo(self):
        """Verifica se o processo seletivo está ativo"""
        return self.status in ['aberto', 'em_andamento']


class Criterio(models.Model):
    """Model para critérios de avaliação personalizados por processo seletivo"""
    
    processo_seletivo = models.ForeignKey(
        ProcessoSeletivo,
        on_delete=models.CASCADE,
        related_name='criterios',
        verbose_name='Processo Seletivo'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Critério',
        help_text='Ex: Comunicação, Técnica, Criatividade, etc.'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
        help_text='Descrição detalhada do critério'
    )
    peso = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(0.01), MaxValueValidator(10.00)],
        verbose_name='Peso',
        help_text='Peso do critério no cálculo final (0.01 a 10.00)'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem de exibição do critério'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Critério de Avaliação'
        verbose_name_plural = 'Critérios de Avaliação'
        ordering = ['processo_seletivo', 'ordem', 'nome']
        unique_together = ['processo_seletivo', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.processo_seletivo.titulo}"


class RankingCandidato(models.Model):
    """Model que liga candidato ao processo seletivo e armazena o tier/rank"""
    
    TIER_CHOICES = [
        ('S', 'Tier S - Excepcional'),
        ('A', 'Tier A - Excelente'),
        ('B', 'Tier B - Bom'),
        ('C', 'Tier C - Regular'),
        ('D', 'Tier D - Abaixo da Média'),
        ('F', 'Tier F - Inadequado'),
    ]
    
    candidato = models.ForeignKey(
        Candidato,
        on_delete=models.CASCADE,
        related_name='rankings',
        verbose_name='Candidato'
    )
    processo_seletivo = models.ForeignKey(
        ProcessoSeletivo,
        on_delete=models.CASCADE,
        related_name='rankings',
        verbose_name='Processo Seletivo'
    )
    tier = models.CharField(
        max_length=1,
        choices=TIER_CHOICES,
        blank=True,
        null=True,
        verbose_name='Tier',
        help_text='Classificação do candidato no processo seletivo'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem do candidato dentro do seu tier'
    )
    observacoes_gerais = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações Gerais',
        help_text='Observações gerais sobre o desempenho do candidato'
    )
    data_avaliacao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data da Avaliação',
        help_text='Data em que o candidato foi avaliado'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Ranking de Candidato'
        verbose_name_plural = 'Rankings de Candidatos'
        unique_together = ['candidato', 'processo_seletivo']
        ordering = ['tier', 'ordem', '-data_avaliacao']

    def __str__(self):
        tier_display = f"Tier {self.tier}" if self.tier else "Sem classificação"
        return f"{self.candidato.nome} - {self.processo_seletivo.titulo} ({tier_display})"

    def save(self, *args, **kwargs):
        """Atualiza a data de avaliação quando um tier é atribuído"""
        if self.tier and not self.data_avaliacao:
            self.data_avaliacao = timezone.now()
        super().save(*args, **kwargs)
    
    def calcular_media_criterios(self):
        """Calcula a média ponderada das avaliações dos critérios"""
        avaliacoes = self.avaliacoes_criterios.all()
        if not avaliacoes.exists():
            return None
        
        soma_ponderada = sum(
            avaliacao.nota * avaliacao.criterio.peso 
            for avaliacao in avaliacoes
        )
        soma_pesos = sum(avaliacao.criterio.peso for avaliacao in avaliacoes)
        
        if soma_pesos == 0:
            return None
        
        return round(soma_ponderada / soma_pesos, 2)


class AvaliacaoCriterio(models.Model):
    """Model para avaliar candidatos em critérios específicos"""
    
    ranking = models.ForeignKey(
        RankingCandidato,
        on_delete=models.CASCADE,
        related_name='avaliacoes_criterios',
        verbose_name='Ranking'
    )
    criterio = models.ForeignKey(
        Criterio,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name='Critério'
    )
    nota = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(10.00)],
        verbose_name='Nota',
        help_text='Nota de 0 a 10'
    )
    anotacao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Anotação',
        help_text='Comentários sobre a avaliação neste critério'
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Avaliação de Critério'
        verbose_name_plural = 'Avaliações de Critérios'
        unique_together = ['ranking', 'criterio']
        ordering = ['criterio__ordem', 'criterio__nome']

    def __str__(self):
        return f"{self.ranking.candidato.nome} - {self.criterio.nome}: {self.nota}"

    def clean(self):
        """Validação para garantir que o critério pertence ao processo seletivo correto"""
        from django.core.exceptions import ValidationError
        if self.criterio.processo_seletivo != self.ranking.processo_seletivo:
            raise ValidationError(
                'O critério deve pertencer ao mesmo processo seletivo do ranking.'
            )
