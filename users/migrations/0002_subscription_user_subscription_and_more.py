from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'subscription',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='subscription',
            field=models.ManyToManyField(through='users.Subscription', to='users.user'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscribed_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_user', to='users.user'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='users.user'),
        ),
    ]

