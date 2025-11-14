from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_business_alter_task_creator_alter_task_reciver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='reciver',
            new_name='receiver',
        ),
    ]
