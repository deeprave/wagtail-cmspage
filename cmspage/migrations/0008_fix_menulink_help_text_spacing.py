from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cmspage", "0007_alter_cmsfooterpage_footer_alter_cmsformpage_body_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menulink",
            name="link_url",
            field=models.CharField(
                blank=True,
                help_text="Set a custom URL if not linking to a page or document. Title is required for this link type",
                verbose_name="External Link",
            ),
        ),
        migrations.AlterField(
            model_name="menulink",
            name="link_document",
            field=models.ForeignKey(
                blank=True,
                help_text="Select a document to link (leave blank for internal page or custom URL). Leave title blank to use this document's title",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtaildocs.document",
                verbose_name="Select Document",
            ),
        ),
        migrations.AlterField(
            model_name="menulink",
            name="link_page",
            field=models.ForeignKey(
                blank=True,
                help_text="Select an internal page to link (leave blank for custom URL or document). Leave title blank to use this page's title",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="menu_links",
                to="wagtailcore.page",
                verbose_name="Select Page",
            ),
        ),
    ]
