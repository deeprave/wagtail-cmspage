# Generated for performance optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmspage', '0004_alter_cmsfooterpage_footer_alter_cmsformpage_body_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='menulink',
            index=models.Index(fields=['site', 'menu_order', 'id'], name='menulink_site_order_idx'),
        ),
        migrations.AddIndex(
            model_name='menulink',
            index=models.Index(fields=['parent', 'menu_order'], name='menulink_parent_order_idx'),
        ),
        migrations.AddIndex(
            model_name='menulink',
            index=models.Index(fields=['site', 'staff_only', 'menu_order'], name='menulink_site_staff_idx'),
        ),
        migrations.AddIndex(
            model_name='menulink',
            index=models.Index(fields=['site', 'parent'], name='menulink_site_parent_idx'),
        ),
    ]
