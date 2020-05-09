# IDSBODL UI
## Installation 
- Configure database information in `idsbodl_ui/settings.py`. 
- `python manage.py inspectdb > web/models.py`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- Configure `web/admin.py`

