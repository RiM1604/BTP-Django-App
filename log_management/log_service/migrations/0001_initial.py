# Generated by Django 5.0.1 on 2024-10-24 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("service_name", models.CharField(max_length=100)),
                ("log_content", models.TextField()),
                ("log_hash", models.CharField(max_length=66)),
                ("blockchain_tx_hash", models.CharField(max_length=66, null=True)),
                ("is_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["timestamp"], name="log_service_timesta_49f19b_idx"
                    ),
                    models.Index(
                        fields=["service_name"], name="log_service_service_5e77b2_idx"
                    ),
                ],
            },
        ),
    ]
