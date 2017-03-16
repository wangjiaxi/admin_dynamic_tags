# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('alias', models.CharField(verbose_name='Alias', max_length=100)),
            ],
            options={
                'verbose_name': 'Dynamic Tag',
                'verbose_name_plural': 'Dynamic Tags',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.CharField(verbose_name='Object Id', max_length=100)),
                ('content_type', models.ForeignKey(verbose_name='Model Type', to='contenttypes.ContentType', related_name='admin_tags_tag_content_type')),
                ('d_tag', models.ForeignKey(verbose_name='Dynamic Tag', to='admin_tags.DynamicTag', related_name='admin_tags_tag_d_tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='TagBind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('d_tag', models.ForeignKey(verbose_name='Dynamic Tag', to='admin_tags.DynamicTag', related_name='admin_tags_tagbind_d_tag')),
                ('model', models.ForeignKey(help_text='What model would use this tag?', verbose_name='Model', related_name='admin_tags_tagbind_model', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Tag Bind',
                'verbose_name_plural': 'Tag Bind',
            },
        ),
        migrations.CreateModel(
            name='TagItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('key', models.CharField(verbose_name='Key', max_length=100)),
                ('d_tag', models.ForeignKey(verbose_name='Dynamic Tag', to='admin_tags.DynamicTag', related_name='admin_tags_tagitem_d_tag')),
            ],
            options={
                'verbose_name': 'Tag Item',
                'verbose_name_plural': 'Tag Items',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='value',
            field=smart_selects.db_fields.ChainedManyToManyField(blank=True, to='admin_tags.TagItem', verbose_name='Value', chained_model_field='d_tag', chained_field='d_tag'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('content_type', 'object_id', 'd_tag')]),
        ),
    ]
