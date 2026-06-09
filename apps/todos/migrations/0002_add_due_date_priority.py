from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="todo",
            name="priority",
            field=models.CharField(
                max_length=10,
                choices=[
                    ("low", "Low"),
                    ("medium", "Medium"),
                    ("high", "High"),
                ],
                default="medium",
                null=True,
                blank=True,
            ),
            preserve_default=False,
        ),
    ]
