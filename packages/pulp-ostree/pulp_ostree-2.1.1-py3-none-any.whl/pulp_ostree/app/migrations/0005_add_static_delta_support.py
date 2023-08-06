# Generated by Django 3.2.18 on 2023-03-29 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0102_add_domain_relations'),
        ('ostree', '0004_add_include_exclude_refs'),
    ]

    operations = [
        migrations.AddField(
            model_name='ostreerepository',
            name='compute_delta',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='OstreeContent',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='ostree_ostreecontent', serialize=False, to='core.content')),
                ('relative_path', models.TextField()),
                ('digest', models.CharField(max_length=64)),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
                'unique_together': {('relative_path', 'digest')},
            },
            bases=('core.content',),
        ),
    ]
