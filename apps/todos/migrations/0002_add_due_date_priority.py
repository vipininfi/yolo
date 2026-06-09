from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="due_date",
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="todo",
            name="priority",
            field=models.PositiveSmallIntegerField(choices=[(1, "High"), (2, "Normal"), (3, "Low")], default=2),
        ),
    ]
