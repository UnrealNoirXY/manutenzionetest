from django.contrib import admin
from django.urls import path
from core import views as core_views
from tickets import views as tickets_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),

    # Dashboard per i ruoli
    path('dashboard/superadmin/', core_views.dashboard_superadmin, name='dashboard_superadmin'),
    path('dashboard/receptionist/', core_views.dashboard_receptionist, name='dashboard_receptionist'),
    path('dashboard/maintainer/', core_views.dashboard_maintainer, name='dashboard_maintainer'),

    # Ticket
    path('ticket/nuovo/', tickets_views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/', tickets_views.ticket_detail, name='ticket_detail'),
]

# Media file in sviluppo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
