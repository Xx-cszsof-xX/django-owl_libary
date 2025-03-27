from django.apps import AppConfig

class MainKiadoConfig(AppConfig):  # Helyes osztálynév
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_kiado'  # Helyes alkalmazásnév

    def ready(self):
        import main_kiado.signals