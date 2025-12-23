from django.urls import path
from . import views

urlpatterns = [
    path('', views.processos_list, name='processos_list'),
    path('processos/create/', views.processos_create, name='processos_create'),
    path('processos/<int:processo_id>/ranking/', views.processo_ranking, name='processo_ranking'),
    path('processos/<int:processo_id>/candidato/create-form/', views.candidato_create_form, name='candidato_create_form'),
    path('processos/<int:processo_id>/candidato/create/', views.candidato_create, name='candidato_create'),
    path('candidato/<int:candidato_id>/update/', views.candidato_update, name='candidato_update'),
    path('ranking/<int:ranking_id>/update-tier/', views.update_ranking_tier, name='update_ranking_tier'),
    
    # URLs de Critérios
    path('processos/<int:processo_id>/criterios/', views.criterios_list_modal, name='criterios_list_modal'),
    path('processos/<int:processo_id>/criterio/create-form/', views.criterio_create_form, name='criterio_create_form'),
    path('processos/<int:processo_id>/criterio/create/', views.criterio_create, name='criterio_create'),
    path('criterio/<int:criterio_id>/edit-form/', views.criterio_edit_form, name='criterio_edit_form'),
    path('criterio/<int:criterio_id>/update/', views.criterio_update, name='criterio_update'),
    path('criterio/<int:criterio_id>/delete/', views.criterio_delete, name='criterio_delete'),
    
    # URLs de Avaliação
    path('ranking/<int:ranking_id>/avaliar/', views.avaliar_candidato_modal, name='avaliar_candidato_modal'),
    path('ranking/<int:ranking_id>/criterio/<int:criterio_id>/salvar/', views.salvar_avaliacao, name='salvar_avaliacao'),
    path('ranking/<int:ranking_id>/observacoes/', views.salvar_observacoes, name='salvar_observacoes'),
]
