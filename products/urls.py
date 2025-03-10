from django.urls import path
from .views import *

urlpatterns = [
    path('update-tasks/', trigger_background_tasks, name='update_tasks'),
    path('products/', list_products, name='list_products'),
    path('orders/', list_orders, name='list_orders'),
    path('terminate-task/<str:task_name>/', terminate_task, name='terminate_task'),
    path('start-task/', StartRecurringTaskView.as_view(), name='start_task'),
    path('list-tasks/', ListRecurringTasksView.as_view(), name='list_tasks'),
    path('cancel-task/', CancelRecurringTaskView.as_view(), name='cancel_task'),
]
