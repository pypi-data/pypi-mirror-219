# Generated by Django 3.2.8 on 2021-10-14 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ostree', '0002_add_relative_path_uniqueness'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ostreeobject',
            name='commit',
        ),
        migrations.CreateModel(
            name='OstreeCommitObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_commit', to='ostree.ostreecommit')),
                ('obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commit_object', to='ostree.ostreeobject')),
            ],
            options={
                'unique_together': {('commit', 'obj')},
            },
        ),
        migrations.AddField(
            model_name='ostreecommit',
            name='objs',
            field=models.ManyToManyField(related_name='ostree_ostreecommit', through='ostree.OstreeCommitObject', to='ostree.OstreeObject'),
        ),
    ]
